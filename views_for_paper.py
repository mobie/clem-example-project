import os
from copy import deepcopy
import mobie

DS_FOLDER = "./data/hela"


def panel_a():
    metadata = mobie.metadata.read_dataset_metadata(DS_FOLDER)
    views = metadata["views"]
    new_view = deepcopy(views["all_sources_with_table"])

    # add the annotation display for em-detail
    em_detail_sources = ["em-detail-a1", "em-detail-a2", "em-detail-a3"]
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
    fluo_sources = [[f"fluorescence-a3-c{i}" for i in range(3)]]
    # note: table can have a superset of the sources in the annotation!
    table_data = {"tsv": {"relativePath": "tables/fluorescence"}}
    annotation_display = mobie.metadata.get_source_annotation_display(
        "fluorescence-annotations", {str(ii): sources for ii, sources in enumerate(fluo_sources)},
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


if __name__ == "__main__":
    # panel_a()
    panel_b()
    mobie.validation.validate_dataset(DS_FOLDER, require_data=False)
