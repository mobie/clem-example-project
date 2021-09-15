import os
import mobie
from elf.io import open_file
from pybdv.metadata import get_data_path, get_setup_ids

# google sheet with additional information:
# https://docs.google.com/spreadsheets/d/12a4-xcPqJzGReId5vqkCx6NSn1VojsvY_vf0qOZHnhk/edit#gid=0

ROOT = "/g/emcf/Mizzon/projects/2021/CLEM_course_2021/MoBIE/clem"
OUT = "./data"
DS_NAME = "hela"


def _get_sources():
    meta = mobie.metadata.read_dataset_metadata(ROOT)
    sources = meta["sources"]
    return sources


def _to_path(source, xml=False):
    rel_path = source[list(source.keys())[0]]["imageData"]["bdv.n5"]["relativePath"]
    path = os.path.join(ROOT, rel_path)
    assert os.path.exists(path), path
    if xml:
        return path
    path = get_data_path(path, return_absolute_path=True)
    assert os.path.exists(path), path
    return path


def add_em_overview(source):
    xml_path = _to_path(source, xml=True)
    scale_factors = 5 * [[1, 2, 2]]
    mobie.add_bdv_image(xml_path, OUT, DS_NAME, image_name="em-overview", menu_name="em",
                        trafos_for_mobie=["Translation"], scale_factors=scale_factors)


def add_em_detail(input_sources, added_sources, names):
    scale_factors = 5 * [[1, 2, 2]]
    for name in names:
        im_name = f"em-detail-{name}"
        if im_name in added_sources:
            continue
        xml_path = _to_path(input_sources[name], xml=True)
        mobie.add_bdv_image(xml_path, OUT, DS_NAME, image_name=im_name, menu_name="em",
                            trafos_for_mobie=["Translation"], scale_factors=scale_factors)


def add_fm(input_sources, added_sources, names):
    scale_factors = 3 * [[1, 2, 2]]
    for name in names:
        xml_path = _to_path(input_sources[name], xml=True)
        setup_ids = get_setup_ids(xml_path)
        im_names = [f"fluorescence-{name}-c{i}" for i in setup_ids]
        if all(nn in added_sources for nn in im_names):
            continue
        mobie.add_bdv_image(xml_path, OUT, DS_NAME, image_name=im_names, menu_name="fluorescence",
                            trafos_for_mobie=None, scale_factors=scale_factors)


def add_tomos(input_sources, added_sources):
    for name, source in input_sources.items():
        if name in added_sources or not name.startswith("tomo"):
            continue
        xml_path = _to_path(input_sources[name], xml=True)
        mobie.add_bdv_image(xml_path, OUT, DS_NAME, menu_name="tomograms")


def check_sources():
    import napari
    sources = _get_sources()
    for name, source in sources.items():
        path = _to_path(source)
        with open_file(path, "r") as f:
            ds = f["setup0/timepoint0/s0"]
            ds.n_threads = 8
            print(name, ":", ds.shape)
            if name.startswith("tomo"):
                print(name, "is tomogram")
            else:
                print("inspecting", name)
                v = napari.Viewer()
                im = ds[:]
                v.add_image(im)
                napari.run()


def add_new_dataset():
    # add all the sources from the existing, but not valid, mobie project
    input_sources = _get_sources()
    added_sources = mobie.metadata.read_dataset_metadata(os.path.join(OUT, DS_NAME)).get("sources", {})

    if "em-overview" not in added_sources:
        add_em_overview(input_sources["1-A"])

    em_detail_names = ["a1-A", "a2-A", "a3-A"]
    add_em_detail(input_sources, added_sources, em_detail_names)

    fm_names = ["a2-FMR", "a3-FMR"]
    add_fm(input_sources, added_sources, fm_names)

    # TODO: wait till Martin converts to uint8
    # add_tomos(input_sources, added_sources)


if __name__ == '__main__':
    # check_sources()
    add_new_dataset()
