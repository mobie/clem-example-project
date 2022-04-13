import os
import mobie

# google sheet with additional information:
# https://docs.google.com/spreadsheets/d/12a4-xcPqJzGReId5vqkCx6NSn1VojsvY_vf0qOZHnhk/edit#gid=0

DS_FOLDER = "./data/hela"


def get_hm_tomos():
    sources = list(mobie.metadata.read_dataset_metadata(DS_FOLDER)["sources"].keys())
    hm_tomos = [source for source in sources if (source.startswith("tomo") and source.endswith("hm"))]
    return hm_tomos


def get_lm_tomos():
    sources = list(mobie.metadata.read_dataset_metadata(DS_FOLDER)["sources"].keys())
    lm_tomos = [source for source in sources if (source.startswith("tomo") and source.endswith("lm"))]
    return lm_tomos


def _get_contrast_limits(source_names, views):
    cmin, cmax = None, None
    for name in source_names:
        tmin, tmax = views[name]["sourceDisplays"][0]["imageDisplay"]["contrastLimits"]
        if cmin is None or tmin < cmin:
            cmin = tmin
        if cmax is None or tmax > cmax:
            cmax = tmax
    return [cmin, cmax]


# add a view that shows raw data and all lm tomograms
def add_lm_view():
    lm_tomos = get_lm_tomos()

    display_names = ["em-overview", "lm-tomograms"]
    source_types = ["image", "image"]
    sources = [["em-overview"], lm_tomos]

    views = mobie.metadata.read_dataset_metadata(DS_FOLDER)["views"]
    em_overview = views["em-overview"]
    overview_trafo = em_overview["sourceTransforms"]
    em_overview = em_overview["sourceDisplays"][0]["imageDisplay"]

    tomo_contrasts = _get_contrast_limits(lm_tomos, views)

    settings = [
        {"color": em_overview["color"], "contrastLimits": em_overview["contrastLimits"]},
        {"color": "white", "contrastLimits": tomo_contrasts}
    ]

    annotation_sources = {ii: [source] for ii, source in enumerate(lm_tomos)}
    annotation_displays = mobie.metadata.create_source_annotation_display(
        "lm-tomogram-table", annotation_sources, DS_FOLDER
    )

    view = mobie.metadata.get_view(display_names, source_types, sources, settings,
                                   is_exclusive=True, menu_name="composite",
                                   source_transforms=overview_trafo,
                                   source_annotation_displays=annotation_displays)
    mobie.metadata.add_view_to_dataset(DS_FOLDER, "lm-tomograms", view)


def add_grid(view_name="grid1", source_names=[[]], dataset=DS_FOLDER):
    """Add a grid view using the 'grid' sourceTransform.
    """

    # make sure that the table is not there, otherwise this creates issues
    table_path = f"./data/tomo/tables/{view_name}/default.tsv"
    if os.path.exists(table_path):
        os.remove(table_path)

    view = mobie.metadata.get_grid_view(
        dataset,
        view_name,
        source_names,
        center_at_origin=True,
        menu_name="composite",
    )
    mobie.validation.validate_view_metadata(view)
    mobie.metadata.add_view_to_dataset(dataset, view_name, view, overwrite=True)


def grid1():
    add_grid(
        source_names=[[item] for item in get_hm_tomos()],
        view_name="highmag_tomos",
        dataset=DS_FOLDER
    )


if __name__ == "__main__":
    # grid1()
    add_lm_view()
