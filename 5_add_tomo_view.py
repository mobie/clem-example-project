import json
import os
from concurrent import futures

import mobie
import numpy as np
import pandas as pd
from elf.io import open_file


def get_clims(tomograms, name):

    path = f"clims_{name}.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)

    def _clims(tomo):
        tomo_path = f"./data/yeast/images/local/{tomo}.n5"
        with open_file(tomo_path, "r") as f:
            data = f["setup0/timepoint0/s2"][:]
        return data.min(), data.max()

    with futures.ThreadPoolExecutor(8) as tp:
        min_max = list(tp.map(_clims, tomograms))
    cmin = min(int(mima[0]) for mima in min_max)
    cmax = max(int(mima[1]) for mima in min_max)
    clims = [1.1 * cmin, 0.9 * cmax]
    with open(path, "w") as f:
        json.dump(clims, f)
    return clims


# refactor into mobie-utils function
def get_tomo_view(name, tomograms, table_data):
    sources = {ii: [tomo] for ii, tomo in enumerate(tomograms)}
    annotation_display = mobie.metadata.view_metadata.get_source_annotation_display(
        name, sources, table_data, tables=["default.tsv"]
    )

    clims = get_clims(tomograms, name)
    image_display = mobie.metadata.view_metadata.get_image_display(
        name, tomograms, color="white",
        blendingMode="sumOccluding",
        contrastLimits=clims
    )

    view = {
        "sourceDisplays": [
            image_display,
            annotation_display
        ],
        "isExclusive": False,
        "uiSelectionGroup": "bookmarks"
    }
    return view


def create_source_annotation_table(tomos, name, ds_folder):
    annotation_ids = np.arange(len(tomos))
    source_names = np.array(tomos)
    table = np.concatenate([
        annotation_ids[:, None], source_names[:, None]
    ], axis=1)
    table = pd.DataFrame(table, columns=["annotation_id", "source"])

    table_path = os.path.join(ds_folder, "tables", name, "default.tsv")
    os.makedirs(os.path.join(ds_folder, "tables", name), exist_ok=True)
    table.to_csv(table_path, sep="\t", index=False)

    rel_path = f"tables/{name}"
    return {
        "tsv": {"relativePath": rel_path}
    }


def add_tomo_view():
    ds_folder = "./data/yeast"

    metadata = mobie.metadata.read_dataset_metadata(ds_folder)
    sources = metadata["sources"]
    tomograms = [src for src in sources if "tomo" in src]

    name = "hm_tomograms"
    hm_tomograms = [tomo for tomo in tomograms if tomo.endswith("hm")]
    table_data = create_source_annotation_table(hm_tomograms, name, ds_folder)
    hm_view = get_tomo_view(name, hm_tomograms, table_data)
    metadata["views"][name] = hm_view

    name = "lm_tomograms"
    lm_tomograms = [tomo for tomo in tomograms if tomo.endswith("lm")]
    table_data = create_source_annotation_table(lm_tomograms, name, ds_folder)
    lm_view = get_tomo_view(name, lm_tomograms, table_data)
    metadata["views"][name] = lm_view

    mobie.metadata.write_dataset_metadata(ds_folder, metadata)
    mobie.validation.validate_project("./data")


if __name__ == '__main__':
    add_tomo_view()
