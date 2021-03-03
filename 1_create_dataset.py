import os
import mobie

ROOT = '/g/schwab/Kimberly/From_Giulia'


def create_dataset():
    mobie.initialize_dataset(input_path=os.path.join(ROOT, 'em_overview.tif'),
                             input_key='',
                             root='./data',
                             dataset_name='yeast',
                             raw_name='em-raw-overview',
                             resolution=(2., 0.01, 0.01),  # artificially thick plane
                             chunks=(1, 512, 512),
                             scale_factors=4 * [[1, 2, 2]],
                             is_default=True,
                             target='local',
                             max_jobs=16,
                             unit='micrometer')


if __name__ == '__main__':
    create_dataset()
