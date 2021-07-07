from copy import deepcopy
import mobie


def update_blending_modes():
    ds = './data/yeast'
    meta = mobie.metadata.read_dataset_metadata(ds)
    views = meta['views']
    new_views = {}
    for name, view in views.items():
        if 'tomo' in name:
            new_view = deepcopy(view)
            new_view['sourceDisplays'][0]['imageDisplay']['blendingMode'] = 'sumOccluding'
            new_views[name] = new_view
        else:
            new_views[name] = view

    meta['views'] = new_views
    mobie.metadata.write_dataset_metadata(ds, meta)
    mobie.validation.validate_project('./data')


update_blending_modes()
