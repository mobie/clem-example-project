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


# add a view that shows raw data and all lm tomograms
def add_lm_view():
    lm_tomos = get_lm_tomos()

    display_names = ["em-overview", "lm-tomograms"]
    source_types = ["image", "image"]
    sources = [["em-overview"], lm_tomos]
    settings = [{}, {}]

    overview = mobie.metadata.read_dataset_metadata(DS_FOLDER)["views"]["em-overview"]
    overview_trafo = overview["sourceTransforms"]

    annotation_sources = {ii: [source] for ii, source in enumerate(lm_tomos)}
    annotation_displays = mobie.metadata.create_source_annotation_display(
        "lm-tomogram-table", annotation_sources, DS_FOLDER
    )

    view = mobie.metadata.get_view(display_names, source_types, sources, settings,
                                   is_exclusive=True, menu_name="composite", source_transforms=overview_trafo,
                                   source_annotation_displays=annotation_displays)
    mobie.metadata.add_view_to_dataset(DS_FOLDER, "lm-tomograms", view)



if __name__ == "__main__":
    add_lm_view()
