from os import listdir
from os.path import isfile, join
import collections
from os.path import expanduser
import glob
import csv
directory_to_search_for_images = expanduser("~")
directory_to_search_for_images += "/retrain_shoes"
directory = listdir(directory_to_search_for_images)

csv_file_name_to_save = expanduser("~")
csv_file_name_to_save += "/retrain_shoes/image_csku_list.csv"

unique_id_file_name_to_save = expanduser("~")
unique_id_file_name_to_save += "/retrain_shoes/unique_id.csv"

dict = {}
dict = collections.OrderedDict()
unique_id=0
header=['image_path', 'csku']

#def all_data(): # wasn't in a mood to create a function

#open the csv file
with open(csv_file_name_to_save, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    print "Header of the file is {header}".format(header=header)

    #Get the list of csku folder
    for csku_folder in directory:

        # create an id for individual csku
        dict[csku_folder]= unique_id
        # Folder path of the image in the csku directory
        folder = ('{currentWorkingPath}/{directory}/*.jpg'.format(currentWorkingPath=directory_to_search_for_images,
                                                                  directory=csku_folder))
        for filename in glob.glob(folder):  # assuming jpg
            writer.writerow([filename, unique_id]) # writing it to the csv file
        unique_id = unique_id + 1
    print "File is saved in path:{file_name}".format(file_name=csv_file_name_to_save)


# Write the unique csku to unique number
with open(unique_id_file_name_to_save, 'wb') as unique_id_file:
    writer = csv.writer(unique_id_file, delimiter=' ')
    for dic in dict:
        writer.writerow([dic, dict[dic]])
print "Unique File is saved in path:{file_name}".format(file_name=unique_id_file_name_to_save)




#if __name__ == '__main__':
#    all_data()


