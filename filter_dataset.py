import numpy as np
import os
import re

import cv2

index = {'mahindra_tuv': 1, 'honda_wrv': 2, 'toyota_yaris': 3, 'mahindra_xuv': 4, 'suzuki_alto': 5,
         'mahindra_scorpio': 6, 'tata_tiago': 7, 'tata_hexa': 8, 'suzuki_ciaz': 9, 'suzuki_baleno': 10,
         'ford_ecosport': 11, 'honda_amaze': 12, 'hyundai_creta': 13, 'volkswagen_vento': 14, 'toyota_innova': 15,
         'honda_city': 16, 'hyundai_verna': 17, 'suzuki_ignis': 18, 'tata_nexon': 19, 'toyota_etios': 20}

directory_path = os.getcwd() + '/training_images/'

_nsre = re.compile('([0-9]+)')


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


def find_last_count(string):
    digit = ''
    for char in string:
        if char.isdigit():
            digit += char
    return int(digit) + 1


def rename_dataset():
    renamed_count = 0
    for category in index.keys():
        category_path = directory_path + category
        files = os.listdir(category_path)
        files.sort(key=natural_sort_key)
        last_name = files[-1]
        count = find_last_count(last_name)
        name = category.split('_')[1]
        maxlen = len(name) + 8
        for filename in files:
            if filename.startswith(name) and len(filename) < maxlen:
                continue
            while True:
                new_name = name + str(count)
                if new_name not in files:
                    count += 1
                    break
                count += 1
            filename = category_path + '/' + filename
            new_name = category_path + '/' + new_name + '.jpg'
            os.rename(filename, new_name)
            print 'Renamed', filename, 'to', new_name
            renamed_count += 1
    print '.\n.\nRenamed {count} files'.format(count=renamed_count)


def is_similar(image1, image2):
    return image1.shape == image2.shape and not (np.bitwise_xor(image1, image2).any())


def remove_duplicates():
    duplicate_list = []
    for category in index.keys():
        print category, '...'
        visited = []
        cat_path = directory_path + category
        files = os.listdir(cat_path)
        for image1 in files:
            filein = cat_path + '/' + image1
            im1 = cv2.imread(filein)
            visited.append(filein)
            for image2 in files:
                filecmp = cat_path + '/' + image2
                if filecmp == filein or filecmp in visited:
                    continue
                visited.append(filecmp)
                im2 = cv2.imread(filecmp)
                if is_similar(im1, im2):
                    print filein, '\n', filecmp, '\n'
                    duplicate_list.append()

                    # for duplicate in duplicate_list:
                    #     os.remove(duplicate)
                    # print 'Deleted {} duplicates!!!'.format(len(duplicate_list))


rename_dataset()

# remove_duplicates()
