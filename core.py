import os
import subprocess
from shutil import rmtree

############################################################################
# EDIT THIS VARIABLES ONLY!
source_folder = "C:\\Users\\RongLiAdmin\\Desktop\\input"
destination_folder = "C:\\Users\\RongLiAdmin\\Desktop\\output"

imaris_file_converter = "C:\\Program Files\\Bitplane\\bpImarisDataService\\bisque-056\\bqenv\\Scripts\\ImarisConvert\\ImarisConvert.exe"
############################################################################

channel_renaming_dict = {
    "RFP" : '0',
    "GFP" : '1',
    "CFP" : '2',
    "YFP" : '3',
    "Cy5" : '4',
    'DAPI': '5',
}


def clean_up():
    for subdir in os.listdir(source_folder):
        if os.path.isdir(os.path.join(source_folder, subdir)):
            rmtree(os.path.join(source_folder, subdir))
        else:
            os.remove(os.path.join(source_folder, subdir))


def flatten_folders(directory):
    for exp_folder in os.listdir(directory):
        full_exp_folder = os.path.join(directory, exp_folder)
        for pos_folder in os.listdir(full_exp_folder):
            full_pos_folder = os.path.join(full_exp_folder, pos_folder)
            if os.path.isdir(full_pos_folder):
                # we found the position folder within experiment
                new_pos_name = os.path.join(directory, exp_folder + '__' + pos_folder)
                print "folder renaming: %s -> %s" % (full_pos_folder, new_pos_name)
                os.rename(full_pos_folder, new_pos_name)




def pattern_name(dir, time, color, slice):
    return "%s_T%s_C%s_Z%s.tif" % (dir.split('\\')[-1], time, channel_renaming_dict[color], slice)


def perform_renaming(position_directory):
    for img_name in os.listdir(position_directory):
        full_name = os.path.join(position_directory, img_name)
        if '.tif' in img_name and img_name.split('_')[0] == 'img':
            time, channel, z_slice = img_name.split('.')[0].split('_')[1:]
            new_name = pattern_name(position_directory, time, channel, z_slice)
            full_new_name = os.path.join(position_directory, new_name)
            os.rename(full_name, full_new_name)
            print "image renaming: %s -> %s" % (full_name, full_new_name)


def perform_conversion(source_directory):
    base_image = ''
    for img_name in os.listdir(source_directory):
        if '.tif' in img_name:
            base_image = os.path.join(source_directory, img_name)

    outfile = os.path.join(destination_folder, source_directory.split('\\')[-1]+'.ims')

    command_array = [imaris_file_converter,
                     '--input',
                     base_image,
                     '--outputformat',
                     'Imaris5',
                     '--output',
                     outfile
                    ]

    print subprocess.list2cmdline(command_array)
    subprocess.Popen(command_array)


def iterate_over_positions():
    for pos_dir in os.listdir(source_folder):
        full_name = os.path.join(source_folder, pos_dir)
        if os.path.isdir(full_name):
            perform_renaming(full_name)
            perform_conversion(full_name)


if __name__ == "__main__":
    flatten_folders(source_folder)
    iterate_over_positions()
    clean_up()