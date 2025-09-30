import os
import xml.etree.ElementTree as ET
import argparse

# construct argument parser & parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--orig_dir", required=True, help="path to original/old directory")
ap.add_argument("-n", "--new_dir", required=True, help="path to new/updated directory")
args = vars(ap.parse_args())

# utility function - return a list of all the .xml files in a given directory
def get_xml_filenames(dir_path):
    filenames = []
    try:
        # get all entries in diretory - includes sub-directories too
        all_entries = os.listdir(dir_path)

        # filter out only xml files
        for entry in all_entries:
            full_path = os.path.join(dir_path, entry)
            if os.path.isfile(full_path):
                extension = full_path[-3:]
                if extension == 'xml':
                    filenames.append(entry)
    except FileNotFoundError:
        print(f"Error: Directory not found at '{dir_path}'")
        quit()
    except Exception as e:
        print(f"An error occured: {e}")
        quit()
    return filenames

# stand class - contains all characteristics set in studio
class Stand:
    def __init__(self, filename=str):
        self.name = filename
        self.params = {}
        self.mapParams(filename)

    # create a dictionary of parameter tags within the stand to compare later
    def mapParams(self, filename=str):
        tree = ET.parse(filename)
        root = tree.getroot()
        params = root.findall('./detectionParams/*')
        for param in params:
            self.params[param.tag] = param.text

# get all the xml files from both directories
orig_dir = args["orig_dir"]
orig_file_list = get_xml_filenames(orig_dir)
new_dir = args["new_dir"]
new_file_list = get_xml_filenames(new_dir)

# create stand objects for all stands in the original directory
orig_stands = {}
for stand_file in orig_file_list:
    origStand = Stand(os.path.join(orig_dir, stand_file))
    # if file doesn't have 'detectionParams' - isn't a reflective stand - ignore it
    if len(origStand.params) > 0:
        orig_stands[stand_file] = origStand

# create stand objects for all stands in the new directory
new_stands = {}
for stand_file in new_file_list:
    newStand = Stand(os.path.join(new_dir, stand_file))
    # if file doesn't have 'detectionParams' - isn't a reflective stand - ignore it
    if len(newStand.params) > 0:
        new_stands[stand_file] = newStand

added_stands = {}
removed_stands = {}
edited_stands = {}

for stand in new_stands:
    if stand not in orig_stands:
        # stand doesn't exist in original list => stand has been added
        added_stands[stand] = new_stands[stand]
    else:
        # stand exists in both lists - check for updates
        if (orig_stands[stand].params != new_stands[stand].params):
            edited_stands[stand] = new_stands[stand]

for stand in orig_stands:
    if stand not in new_stands:
        # stand doesn't exist in new list => stand has been removed
        removed_stands[stand] = orig_stands[stand]

print('')

# output changes made
if(len(added_stands) > 0):
    print('Stands Added:')
    for s in added_stands:
        print(f'\t{s}')
else:
    print('No Stands Added.')

if(len(removed_stands) > 0):
    print('Stands Removed:')
    for s in removed_stands:
        print(f'\t{s}')
else:
    print('No Stands Removed.')

if(len(edited_stands) > 0):
    print('Stands Edited:')
    for s in edited_stands:
        print(f'\t{s}')
        # loop through each parameter in original & new, print any that have changed
        for key in orig_stands[s].params:
            if orig_stands[s].params[key] != new_stands[s].params[key]:
                print(f'\t\t{key}: {orig_stands[s].params[key]} => {new_stands[s].params[key]}')
else:
    print('No Stands Edited.')

print('Comparison Complete.')