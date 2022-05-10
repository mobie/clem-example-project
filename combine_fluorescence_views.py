import mobie
import numpy as np


def combine_fluorescence_views():
    dataset_folder = "./data/hela"
    metadata = mobie.metadata.read_dataset_metadata(dataset_folder)
    views = metadata["views"]
    fluo_views = [name for name in views if name.startswith("fluo")]
    if len(fluo_views) == 2:
        return
    print(fluo_views)
    fluo_images = np.unique(["-".join(fluo.split("-")[:-1]) for fluo in fluo_views])
    print(fluo_images)

    for im in fluo_images:
        fluo_channels = [name for name in fluo_views if name.startswith(im)]
        fluo_channels.sort()
        print("Combining", fluo_channels, "to", im)
        mobie.combine_views(dataset_folder, fluo_channels, im, "fluorescence", keep_original_views=False)


if __name__ == "__main__":
    combine_fluorescence_views()
