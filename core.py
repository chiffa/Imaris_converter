import os
import subprocess

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
    "YFP" : '3'
}


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
            print "%s -> %s" % (full_name, full_new_name)


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
    iterate_over_positions()