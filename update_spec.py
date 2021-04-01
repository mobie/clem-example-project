from mobie.migration.migrate_v2 import migrate_project


def parse_menu_name(source_type, source_name):
    if source_name.startswith('em'):
        return 'em'
    else:
        return 'lm'


migrate_project('./data', parse_menu_name)
