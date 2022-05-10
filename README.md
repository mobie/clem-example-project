# Clem Example Project

MoBIE project with two clem example datasets.

## Hela dataset
On-section CLEM data according to the protocol published in [Correlated fluorescence and 3D electron microscopy with high sensitivity and spatial precision](https://doi.org/10.1083/jcb.201009037).
  Cells are HeLa_Kyoto_H2B - mCherry and GalT - GFP cell line as published in [CellCognition: time-resolved phenotype annotation in high-throughput live cell imaging](https://doi.org/10.1038/nmeth.1486).
The data was acquired and shared by Giulia Mizzon from the Electron Microscopy Core Facility at EMBL Heidelberg.

The dataset `hela` contains the following image sources:
- EM-overview Single EM overview stitched montage.
- em-detail, stitched montages covering individual grid squares
- fluorescence-overview: GFP fluorescence channel registered to the em
- low magnitude tomograms: EM tomograms at 5 nm isotropic resolution
- high magnitude tomograms: EM tomograms at 1.5 nm isotropic resolution

## Yeast dataset 
On-section CLEM data according to the protocol published in [Correlated fluorescence and 3D electron microscopy with high sensitivity and spatial precision](https://doi.org/10.1083/jcb.201009037).
From the publication [Seipin and Nem1 establish discrete ER subdomains to initiate yeast lipid droplet biogenesis](https://doi.org/10.1083/jcb.201910177).
The data was acquired and shared by Giulia Mizzon from the Electron Microscopy Core Facility at EMBL Heidelberg.

The dataset `yeast` contains the following image sources:

- EM-overview Single EM overview slices
- fluorescence-overview: GFP fluorescence channel registered to the em
- low magnitude tomograms: EM tomograms at 5 nm isotropic resolution
- high magnitude tomograms: EM tomograms at 1.25 nm isotropic resolution
