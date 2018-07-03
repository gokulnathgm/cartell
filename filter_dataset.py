import os

index = {'mahindra_tuv': 1, 'honda_wrv': 2, 'toyota_yaris': 3, 'mahindra_xuv': 4, 'suzuki_alto': 5,
         'mahindra_scorpio': 6, 'tata_tiago': 7, 'tata_hexa': 8, 'suzuki_ciaz': 9, 'suzuki_baleno': 10,
         'ford_ecosport': 11, 'honda_amaze': 12, 'hyundai_creta': 13, 'volkswagen_vento': 14, 'toyota_innova': 15,
         'honda_city': 16, 'hyundai_verna': 17, 'suzuki_ignis': 18, 'tata_nexon': 19}

directory_path = os.getcwd() + '/training_images/'


def rename_dataset():
    renamed_count = 0
    for category in index.keys():
        category_path = directory_path + category
        print 'category_path: ', category_path, '\n\n\n'
        print os.listdir(category_path)
        count = 0
        for filename in os.listdir(category_path):
            if filename.startswith(category):
                continue
            while True:
                new_name = category + '_' + str(count)
                if new_name not in os.listdir(category_path):
                    count += 1
                    break
                count += 1
            filename = category_path + '/' + filename
            new_name = category_path + '/' + new_name + '.jpg'
            os.rename(filename, new_name)
            print 'Renamed', filename, 'to', new_name
            renamed_count += 1
    print '.\n.\nRenamed {count} files'.format(count=renamed_count)


rename_dataset()
