# -*- coding: utf-8 -*-
#
# writes yaml front matter for image_map pages
#

import yaml

#
# generates yaml front matter if it doesn't exist
#
def write_image_map(flight_map, payload_title, config, image_map_path):

    try:
        open(image_map_path, 'r')
    except:
        post_yaml = {
            "layout": "image-map",
            "flight_map": flight_map,
            "payload_title": payload_title,
            "title": payload_title + " Image Map",
            "categories": "hab image-map",
            "image_map": config
        }

        yaml_str = yaml.dump(post_yaml, default_flow_style=False)
        markdown = "---\n{}---\n".format(yaml_str)

        # Write out to file
        print("Writing {}...".format(image_map_path))
        print("NOTICE: You need to set the 'root' and 'page' parameters!!")
        print("")
        with open(image_map_path, 'w') as outfile:
            outfile.write(markdown)
