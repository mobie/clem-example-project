import os
import mobie

ROOT = '/g/emcf/Mizzon/projects/2021/CLEM_course_2021/F30/g4_CLEMcourse/'


def add_em_ov():
    mobie.add_image(input_path=os.path.join(ROOT, '350x_ov_merged_s0.mrc'),
                         input_key='data',
                         root='./data',
                         dataset_name='hela',
                         image_name='em-overview1',
                         resolution=(0.03412,0.03412),
                         chunks=(512, 512),
                         scale_factors=4 * [[2, 2]],
                         target='local',
                         max_jobs=4,
                         file_format='ome.zarr',
                         unit='micrometer')


if __name__ == '__main__':
    add_em_ov()
