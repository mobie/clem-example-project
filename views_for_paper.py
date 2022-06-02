import os
from copy import deepcopy
import mobie

DS_FOLDER = "./data/hela"


def panel_a():
    metadata = mobie.metadata.read_dataset_metadata(DS_FOLDER)
    views = metadata["views"]
    new_view = deepcopy(views["all_sources_with_table"])

    # add the annotation display for em-detail
    em_detail_sources = ["em-detail-a1-A", "em-detail-a2-A", "em-detail-a3-A"]
    table_folder = os.path.join(DS_FOLDER, "tables", "em-detail")
    os.makedirs(table_folder, exist_ok=True)
    table_path = os.path.join(table_folder, "default.tsv")
    mobie.tables.compute_source_annotation_table(em_detail_sources, table_path)
    table_data = {"tsv": {"relativePath": "tables/em-detail"}}
    annotation_display = mobie.metadata.get_source_annotation_display(
        "em-detail-annotations", {str(ii): [source] for ii, source in enumerate(em_detail_sources)},
        table_data, ["default.tsv"], showAsBoundaries=True, boundaryThickness=1.0
    )
    new_view["sourceDisplays"].append(annotation_display)

    # add the annotation display for fluo
    fluo_sources = [[f"fluorescence-a2-c{i}" for i in range(3)],
                    [f"fluorescence-a3-c{i}" for i in range(3)]]
    table_folder = os.path.join(DS_FOLDER, "tables", "fluorescence")
    os.makedirs(table_folder, exist_ok=True)
    table_path = os.path.join(table_folder, "default.tsv")
    mobie.tables.compute_source_annotation_table(fluo_sources, table_path)
    table_data = {"tsv": {"relativePath": "tables/fluorescence"}}
    annotation_display = mobie.metadata.get_source_annotation_display(
        "fluorescence-annotations", {str(ii): sources for ii, sources in enumerate(fluo_sources)},
        table_data, ["default.tsv"], showAsBoundaries=True, boundaryThickness=1.0
    )
    new_view["sourceDisplays"].append(annotation_display)

    new_view["uiSelectionGroup"] = "paper"
    views["Fig2_a"] = new_view
    metadata["views"] = views
    mobie.metadata.write_dataset_metadata(DS_FOLDER, metadata)


def panel_b():
    metadata = mobie.metadata.read_dataset_metadata(DS_FOLDER)
    views = metadata["views"]
    new_view = deepcopy(views["area3_tomos_37_38_40_41_54"])

    # add the annotation display for fluo
    fluo_sources = [f"fluorescence-a3-c{i}" for i in range(3)]
    # note: table can have a superset of the sources in the annotation!
    table_data = {"tsv": {"relativePath": "tables/fluorescence"}}
    annotation_display = mobie.metadata.get_source_annotation_display(
        "fluorescence-annotations", {1: fluo_sources},
        table_data, ["default.tsv"], showAsBoundaries=True, boundaryThickness=1.0
    )
    new_view["sourceDisplays"].append(annotation_display)

    # add the annotation display for lm-tomos (only select tomo38 lm)
    tomo_sources = ["tomo_37_lm", "tomo_38_lm", "tomo_40_lm", "tomo_41_lm", "tomo_54_lm"]
    # note: table can have a superset of the sources in the annotation!
    table_data = {"tsv": {"relativePath": "tables/lm-tomogram-table"}}
    annotation_display = mobie.metadata.get_source_annotation_display(
        "lm-tomo-annotations", {str(ii): [source] for ii, source in enumerate(tomo_sources)},
        table_data, ["default.tsv"], showAsBoundaries=True, boundaryThickness=1.0,
        selectedAnnotationIds=["0;1"]  # tomo_38_lm has annotation_id 1
    )
    new_view["sourceDisplays"].append(annotation_display)

    new_view["uiSelectionGroup"] = "paper"
    views["Fig2_b"] = new_view
    metadata["views"] = views
    mobie.metadata.write_dataset_metadata(DS_FOLDER, metadata)


def panel_c():
    metadata = mobie.metadata.read_dataset_metadata(DS_FOLDER)
    views = metadata["views"]
    new_view = deepcopy(views["area3_tomos_37_38_40_41_54"])

    # only set the fluorescence display to visible
    displays = new_view["sourceDisplays"]
    new_displays = []
    for dp in displays:
        key = list(dp.keys())[0]
        display = dp[key]
        display["visible"] = display["name"].startswith("fluo")
        new_displays.append({key: display})

    # add the annotation display for the lm-tomos
    tomo_sources = ["tomo_37_lm", "tomo_38_lm", "tomo_40_lm", "tomo_41_lm", "tomo_54_lm"]
    # note: table can have a superset of the sources in the annotation!
    table_data = {"tsv": {"relativePath": "tables/lm-tomogram-table"}}
    annotation_display = mobie.metadata.get_source_annotation_display(
        "lm-tomo-annotations", {str(ii): [source] for ii, source in enumerate(tomo_sources)},
        table_data, ["default.tsv"], showAsBoundaries=True, boundaryThickness=1.0
    )
    new_view["sourceDisplays"].append(annotation_display)

    new_view["uiSelectionGroup"] = "paper"
    views["Fig2_c"] = new_view
    metadata["views"] = views
    mobie.metadata.write_dataset_metadata(DS_FOLDER, metadata)


def panel_d():
    metadata = mobie.metadata.read_dataset_metadata(DS_FOLDER)
    views = metadata["views"]
    new_view = deepcopy(views["tomo_38_hm"])

    new_view["isExclusive"] = True
    new_view["uiSelectionGroup"] = "paper"
    views["Fig2_d"] = new_view
    metadata["views"] = views
    mobie.metadata.write_dataset_metadata(DS_FOLDER, metadata)


def panel_e():
    metadata = mobie.metadata.read_dataset_metadata(DS_FOLDER)
    views = metadata["views"]
    new_view = deepcopy(views["tomo_38_lm"])

    # add (non-visible) tomo-38-hm source for the sourceAnnotation
    new_view["sourceDisplays"].append(
        mobie.metadata.get_image_display("tomo_38_hm", ["tomo_38_hm"], visible=False)
    )

    # add the source annotation display to generate boundary for the HM tomo
    tomo_sources = ["tomo_38_hm"]
    # note: table can have a superset of the sources in the annotation!
    table_data = {"tsv": {"relativePath": "tables/highmag_tomos"}}
    annotation_display = mobie.metadata.get_source_annotation_display(
        "hm-tomo-annotations", {1: tomo_sources},
        table_data, ["default.tsv"], showAsBoundaries=True, boundaryThickness=1.0
    )
    new_view["sourceDisplays"].append(annotation_display)
    new_view["isExclusive"] = True

    new_view["uiSelectionGroup"] = "paper"
    views["Fig2_e"] = new_view
    metadata["views"] = views
    mobie.metadata.write_dataset_metadata(DS_FOLDER, metadata)


def panel_f():
    metadata = mobie.metadata.read_dataset_metadata(DS_FOLDER)
    views = metadata["views"]
    new_view = deepcopy(views["highmag_tomos"])

    new_view["uiSelectionGroup"] = "paper"
    views["Fig2_f"] = new_view
    metadata["views"] = views
    mobie.metadata.write_dataset_metadata(DS_FOLDER, metadata)


# tomo 53 is the one not in the field of view
def panel_e_intiial():
    sources = [["tomo_37_lm"], ["tomo_38_lm"], ["tomo_40_lm"], ["tomo_41_lm"], ["tomo_54_lm"]]
    positions = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]
    mobie.create_grid_view(
        "./data/hela", view_name="Fig2_e", sources=sources,
        table_folder="tables/lm-tomogram-table", menu_name="mobie-paper",
        positions=positions, overwrite=True)


# tomo 38 should get the blue border
def panel_e_update():
    ds = "./data/hela"
    meta = mobie.metadata.read_dataset_metadata(ds)
    views = meta["views"]
    view = views["Figure2e"]
    sources = {"1": ["tomo_38_lm"]}

    table_data = {"tsv": {"relativePath": "tables/lm-tomogram-table"}}
    tables = ["default.tsv"]

    new_region_dp = mobie.metadata.get_region_display(
        name="tomo38-highlight", sources=sources, table_data=table_data, tables=tables,
        colorByColumn="annotationColor", lut="argbColumn"
    )
    view["sourceDisplays"] = [new_region_dp] + view["sourceDisplays"]

    views["Figure2e"] = view
    meta["views"] = views
    mobie.metadata.write_dataset_metadata(ds, meta)


def main():
    # panel_a()
    # panel_b()
    # panel_c()
    # panel_d()
    # panel_e()
    # panel_f()
    # panel_e_initial()
    panel_e_update()
    mobie.validation.validate_dataset(DS_FOLDER, require_local_data=False)


if __name__ == "__main__":
    main()
