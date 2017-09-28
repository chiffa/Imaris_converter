import os
import subprocess
from shutil import rmtree
import time

############################################################################
# EDIT THIS VARIABLES ONLY!
source_folder = "Z:\\Imaris Converter\\input"
destination_folder = "Z:\\Imaris Converter\\output"
Imaris_install_directory = "C:\\Program Files\\Bitplane"
############################################################################


def find_converter_path():
    likely_folders = [f for f in os.listdir(Imaris_install_directory) if os.path.isdir(os.path.join(Imaris_install_directory, f))]
    likely_folders = [f for f in likely_folders if "ImarisFileConverter" in f]

    if len(likely_folders) == 0:
        raise Exception("Imaris file converter not found in default install directory, please make sure that Imaris is installed or change the Imaris install directory")

    if len(likely_folders) > 1:
        print "Multiple Imaris versions installed . Choose which one you would like to use among the following:"
        for i, full_folder_name in enumerate(likely_folders):
            print 'option', i+1, '\t', full_folder_name
        chosen_option = raw_input('Please type the number of the option corresponding to the version you would like to use\n>')
        likely_folders = [likely_folders[int(chosen_option)-1]]

        # raise Exception("Imaris file converter not found or too many potential converters found. Here are the top-direcories %s", likely_folders)

    imaris_file_converter = os.path.join(os.path.join(Imaris_install_directory,
                                                      likely_folders[0]),
                                         "ImarisConvert.exe")

    print 'using file converter located at %s' % imaris_file_converter

    return imaris_file_converter

imaris_file_converter = find_converter_path()

channel_renaming_dict = {
    "Cy5" : '0',
    "GFP" : '1',
    "RFP" : '2',
    "YFP" : '3',
    "CFP" : '4',
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
            # print "image renaming: %s -> %s" % (full_name, full_new_name)


def perform_conversion(source_directory):
    base_image = ''
    for img_name in os.listdir(source_directory):
        if '.tif' in img_name:
            base_image = os.path.join(source_directory, img_name)
            break

    if base_image:
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
        subprocess.call(command_array)

    else:
        print 'Nothing found to in folder %s' % source_directory


def iterate_over_positions():
    for pos_dir in os.listdir(source_folder):
        full_name = os.path.join(source_folder, pos_dir)
        if os.path.isdir(full_name):
            perform_renaming(full_name)
            perform_conversion(full_name)


def main():
    message = "DO NOT CONVERT RAW OR UNDUPLICATED DATA: AFTER CONVERSION INPUT FOLDER CONTENTS WILL BE DELETED.\n Do you agree with it? (Y)es/(N)o\n"
    confirm = raw_input(message)
    if confirm.lower() in ['y', 'yes']:
        flatten_folders(source_folder)
        iterate_over_positions()
        clean_up()
        raw_input('Processing is now finished. Press enter to close.')
    else:
        raw_input('Aborted. Please enter to close.')


if __name__ == "__main__":
    main()
