from datetime import datetime
import glob
import csv


def spatial_info(path):
    # GET all folders that ends with db
    list_macro = glob.glob(path + '/*.db/*', recursive=True)

    for folder in list_macro:
        merge_data(folder)


def find_nearest(odom_file, time: datetime):
    with open(odom_file, 'r') as file_odomR:
        csv_reader_odom = csv.reader(file_odomR, delimiter=',')
        line_index = 0
        result = ''
        for row in csv_reader_odom:
            if line_index != 0:
                odom_time = row[0]
                if odom_time <= time:
                    result = row
                else:
                    break
            line_index += 1
        return result


def json_converter(row):
    x_val = row[1]
    y_val = row[2]
    z_val = row[3]
    json = x_val + ', ' + y_val + ', ' + z_val

    return json



def merge_data(folder_path):
    output_file = folder_path + '/merged.csv'
    macro_file = glob.glob(folder_path + '*/macro.csv', recursive=True)[0]
    odom_file = glob.glob(folder_path + '*/odom.csv', recursive=True)[0]
    line_index = 0

    with open(macro_file, 'r') as fileR, open(output_file, 'a') as fileW:
        csv_reader = csv.reader(fileR, delimiter=',')  # csv reader
        csv_writer = csv.writer(fileW, delimiter=',')  # csv writer
        for row in csv_reader:
            if line_index == 0:  # update the header row
                row.append('x')
                row.append('y')
                row.append('z')

                csv_writer.writerow(row)
            else:
                time = row[0]
                row_nearest = find_nearest(odom_file, time)
                # save position as json
                row.append(row_nearest[1])
                row.append(row_nearest[2])
                row.append(row_nearest[3])
                csv_writer.writerow(row)
            line_index += 1
