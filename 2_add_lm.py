import os
import mobie

ROOT = '/g/schwab/Kimberly/From_Giulia'


def add_lm():
    mobie.add_image_data(input_path=os.path.join(ROOT, 'fluorescence.tif'),
                         input_key='',
                         root='./data',
                         dataset_name='yeast',
                         image_name='lm-fluorescence-overview',
                         resolution=(10., 0.01, 0.01),  # artificially thick plane
                         chunks=(1, 512, 512),
                         scale_factors=4 * [[1, 2, 2]],
                         settings={'Color': 'Green'},
                         target='local',
                         max_jobs=16,
                         unit='micrometer')


if __name__ == '__main__':
    add_lm()
