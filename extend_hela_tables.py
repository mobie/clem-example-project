# adding the information about organelles per tomogram to the hela tables
# https://docs.google.com/spreadsheets/d/12a4-xcPqJzGReId5vqkCx6NSn1VojsvY_vf0qOZHnhk/edit#gid=0

import pandas as pd

TOMOGRAMS = {
    "tomo_37": ["ribosomes", "golgi", "microtubule", "endo/lysosome"],
    "tomo_38": ["ribosomes", "golgi", "filaments bundle", "endo/lysosome", "autophagosome", "endoplasmic reticulum"],
    "tomo_40": ["ribosomes", "endo/lysosome", "golgi"],
    "tomo_41": ["ribosomes", "endo/lysosome", "golgi", "filaments bundle"],
    "tomo_53": ["golgi", "endo/lysosome", "autophagosome", "filaments bundle", "microtubule"],
    "tomo_54": ["mitochondrion", "endoplasmic reticulum", "microtubule", "filaments bundle"],
}


def extend_hela_table(table):
    all_organelles = list(set(
        [organelle for organelles in TOMOGRAMS.values() for organelle in organelles]
    ))
    all_organelles.sort()
    print(all_organelles)
    tab = pd.read_csv(table, sep="\t")
    tomo_names = ["_".join(name.split("_")[:2]) for name in tab["source"]]
    print(tomo_names)
    for organelle in all_organelles:
        new_col = [int(organelle in TOMOGRAMS[name]) for name in tomo_names]
        tab[organelle] = new_col
    tab.to_csv(table, index=False, sep="\t")


def update_hela_table(table):
    all_organelles = list(set(
        [organelle for organelles in TOMOGRAMS.values() for organelle in organelles]
    ))
    all_organelles.sort()
    print(all_organelles)
    tab = pd.read_csv(table, sep="\t")[["region_id", "source"]]
    tomo_names = ["_".join(name.split("_")[:2]) for name in tab["source"]]
    print(tomo_names)
    for organelle in all_organelles:
        new_col = ["yes" if organelle in TOMOGRAMS[name] else "no" for name in tomo_names]
        tab[organelle] = new_col
    tab.to_csv(table, index=False, sep="\t")


# extend_hela_table("./data/hela/tables/highmag_tomos/default.tsv")
# extend_hela_table("./data/hela/tables/lm-tomogram-table/default.tsv")
update_hela_table("./data/hela/tables/highmag_tomos/default.tsv")
update_hela_table("./data/hela/tables/lm-tomogram-table/default.tsv")
