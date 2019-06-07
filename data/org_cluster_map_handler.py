import os
import json

import logging

import getorg

from data.models import Contributor


def handle(output_dir='cluster_map'):
    """
    Creates a organization cluster map using the contributors location
    stored in the database
    :param output_dir: Directory where all the required CSS and JS files
    are copied by 'getorg' package
    """
    logger = logging.getLogger(__name__)
    logger.info("'cluster_map/' is the default directory for storing"
                " organization map related files. If arg 'output_dir'"
                ' not provided it will be used as a default directory by'
                " 'getorg' package.")

    # For creating the organization map, the 'getorg' uses a 'Nominatim' named
    # package which geocodes the contributor location and then uses that class
    # to create the map. Since, we're not dealing with that function which use
    # that 'Nominatim' package because we're fetching a JSON data and storing
    # it in our db. Therefore, defining our own simple class that can aid us
    # to create a cluster map.
    class Location:

        def __init__(self, longitude, latitude):
            self.longitude = longitude
            self.latitude = latitude

    org_location_dict = {}

    for contrib in Contributor.objects.all():
        if contrib.location:
            user_location = json.loads(contrib.location)
            location = Location(user_location['longitude'],
                                user_location['latitude'])
            org_location_dict[contrib.login] = location
            logger.debug(f'{contrib.login} location {user_location}'
                         f' added on map')
    getorg.orgmap.output_html_cluster_map(org_location_dict,
                                          folder_name=output_dir)

    move_and_make_changes_in_files(output_dir)


def move_and_make_changes_in_files(output_dir):
    """
    Move static files from 'output_dir' to django static folder and
    the 'map.html' file to django templates directory to get it displayed
    on the homepage with the needed django syntax and CSS in the html file.
    :param output_dir: Directory from where the files have to be moved
    """

    move_leaflet_dist_folder(output_dir)

    move_file(source=get_file_path(os.getcwd(), output_dir,
                                   'org-locations.js'),
              destination=get_file_path(os.getcwd(), 'static',
                                        'org-locations.js'))

    # Make changes in map.html to support django syntax with needed CSS
    change_and_write_html_map_file(output_dir=output_dir,
                                   destination=get_file_path(os.getcwd(),
                                                             'templates',
                                                             'map.html'))

    os.remove(get_file_path(os.getcwd(), output_dir, 'map.html'))


def move_leaflet_dist_folder(output_dir):
    source_path = get_file_path(os.getcwd(), output_dir, 'leaflet_dist')
    destination_path = get_file_path(os.getcwd(), 'static', 'leaflet_dist')

    # Remove existing leaflet_dir if exists
    for root, dirs, files in os.walk(destination_path):
        for file in files:
            os.remove(os.path.join(destination_path, file))
        os.rmdir(root)

    os.renames(source_path, destination_path)


def get_file_path(*args):
    return '/'.join(args)


def move_file(source, destination):
    os.rename(source, destination)


def replace(line, content):
    changed_line = line
    for old, new in content:
        changed_line = changed_line.replace(old, new)
    return changed_line


def change_and_write_html_map_file(output_dir, destination):
    with open(destination, 'w+') as new_file:
        with open(f'{output_dir}/map.html') as old_file:
            for html_line in old_file:
                line = html_line.strip()
                if line.__contains__('<html>'):
                    new_file.write('{% load staticfiles %}\n')

                elif line.__contains__('<title>'):
                    meta_charset = '<meta charset="utf-8">'
                    new_file.write(meta_charset + '\n')

                elif line.__contains__('</head>'):
                    adjust_prop = get_map_style_properties()
                    new_file.write(adjust_prop.replace('    ', '') + '\n')

                elif line.__contains__('https://'):
                    line = replace(line=line,
                                   content=[('https:', ''), (' />', '>')])

                elif line.__contains__('<link '):
                    line = replace(line=line,
                                   content=[('href="', 'href="{% static \''),
                                            ('.css', '.css\' %}'),
                                            (' />', '>')])

                elif line.__contains__('<script '):
                    line = replace(line=line,
                                   content=[('src="', 'src="{% static \''),
                                            ('.js', '.js\' %}')])
                    if line.__contains__(' type="text/javascript"'):
                        line = line.replace(' type="text/javascript"', '')

                elif line.__contains__('Mouse over') or len(line) == 0:
                    continue

                new_file.write(line + '\n')


def get_map_style_properties():
    return '''
    <style>
        #map {
        width: 60%;
        height: 300px;
        margin: auto;
        box-shadow: 0px 0px 25px 2px;
        }
        @media only screen and (max-width:750px){
            #map {
                width: 90%
            }
        }
    </style>
    '''
