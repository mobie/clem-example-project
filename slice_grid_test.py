import mobie.metadata as meta
from mobie.metadata.slice_grid_view import create_slice_grid


def simple_slice_grid():
    ds_folder = "./data/hela"
    ds_meta = meta.read_dataset_metadata(ds_folder)
    source_name = "tomo_38_hm"

    # we only need the contrast limits
    ref_view = ds_meta["views"][source_name]
    contrast_limits = ref_view["sourceDisplays"][0]["imageDisplay"]["contrastLimits"]

    create_slice_grid(
        ds_folder,
        source_name,
        n_slices=8,
        view_name="slice-grid-tomo38",
        menu_name="slice-grid",
        initial_transforms=None,
        display_settings={"contrastLimits": contrast_limits},
        overwrite=True,
        view_file=None,
        is_exclusive=True,
    )


if __name__ == "__main__":
    simple_slice_grid()
