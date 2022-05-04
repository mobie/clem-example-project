import mobie
import os

transforming_sources = [
    ["em-overview"],
    ["em-detail-a1-A"],
    ["em-detail-a2-A",
     "tomo_53_lm",
     "tomo_53_hm",
     "fluorescence-a2-c0",
     "fluorescence-a2-c1",
     "fluorescence-a2-c2"
     ]
]
trafo_names = ["manual_shift_a3", "manual_shift_a1", "manual_trafo_a2"]
transforms = [
    [
        1.0,
        0.0,
        0.0,
        1.7940359100750243,
        0.0,
        1.0,
        0.0,
        -6.6635619517072655,
        0.0,
        0.0,
        1.0,
        0.0
    ],
    [
        1.0,
        0.0,
        0.0,
        -2.4988357318902317,
        0.0,
        1.0,
        0.0,
        -7.688725328893014,
        0.0,
        0.0,
        1.0,
        0.0
    ],
    [
        0.9998476951563912,
        0.01745240643728351,
        0.0,
        0.4546800322595175,
        -0.01745240643728351,
        0.9998476951563912,
        0.0,
        -3.527570751462804,
        0.0,
        0.0,
        1.0,
        0.0
    ]
]

root = os.getcwd()
data = 'data/hela'
ds = mobie.metadata.read_dataset_metadata(os.path.join(root, data))

views = ds['views']


def add_transforms():
    for tf_sources, trafo, name in zip(transforming_sources, transforms, trafo_names):
        for view in views.values():
            for tf_source in tf_sources:
                if [tf_source] in [sD['imageDisplay']['sources'] for sD in view['sourceDisplays'] if 'imageDisplay' in sD]:
                    view['sourceTransforms'].append(
                        mobie.metadata.get_affine_source_transform([tf_source], trafo, name=name))

    mobie.metadata.write_dataset_metadata(data,ds)


if __name__ == "__main__":
    add_transforms()
