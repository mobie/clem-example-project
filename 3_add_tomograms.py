import os
from glob import glob

import imageio
import h5py
import mobie
from elf.transformation import bdv_to_native, compute_affine_matrix, native_to_bdv

ROOT = '/g/schwab/Kimberly/From_Giulia'


def scale_affine(affine):
    scale = compute_affine_matrix(scale=3*(1e3,))
    trafo = bdv_to_native(affine)
    trafo = trafo @ scale
    return native_to_bdv(trafo)


def load_affines():
    affines = {}
    trafo_file = os.path.join(ROOT, 'tomogram_affines.txt')

    tomo_name = None

    with open(trafo_file, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            if len(line) == 5:
                tomo_name = line
            elif len(line) > 10:
                affine = line.split()
                affine = list(map(float, affine))
                affine = scale_affine(affine)
                affines[tomo_name] = affine
            else:
                tomo_name = None
    return affines


def add_tomograms():
    tomo_paths = glob(os.path.join(ROOT, '*_lm.*')) + glob(os.path.join(ROOT, '*_hm.*'))
    affines = load_affines()

    chunks = (32, 128, 128)
    scale_factors = [[1, 2, 2],
                     [1, 2, 2],
                     [1, 2, 2],
                     [1, 2, 2],
                     [2, 2, 2]]

    for tomo in tomo_paths:
        im = imageio.volread(tomo).astype('uint16')
        settings = {
            'contrastLimits': [im.min(), im.max()],
            'blendingMode': 'sumOccluding'
        }
        tomo_name = os.path.splitext(os.path.split(tomo)[1])[0]
        affine = affines[tomo_name]

        # low mag tomograms are at 5nm, high mac ones at 1.25 nm
        if 'lm' in tomo_name:
            resolution = (0.005, 0.005, 0.005)
        else:
            resolution = (0.00125, 0.00125, 0.00125)

        tmp_folder = f'tmp_{tomo_name}'
        os.makedirs(tmp_folder, exist_ok=True)
        tmp_path = os.path.join(tmp_folder, 'vol.h5')
        with h5py.File(tmp_path, 'w') as f:
            f.create_dataset('data', data=im, chunks=chunks)

        tomo_name = f'em-tomogram-{tomo_name}'
        mobie.add_image_data(input_path=tmp_path,
                             input_key='data',
                             root='./data',
                             dataset_name='yeast',
                             image_name=tomo_name,
                             resolution=resolution,
                             chunks=chunks,
                             scale_factors=scale_factors,
                             transformation=affine,
                             settings=settings,
                             tmp_folder=tmp_folder,
                             target='local',
                             max_jobs=16,
                             unit='micrometer')


if __name__ == '__main__':
    add_tomograms()
