import csv
import glob
import os
import shutil
from generate_mrs_log import csv_to_xes, merge_xes
from spatial_info import spatial_info

current_path = os.path.dirname(os.path.realpath(__file__))
# Destination path
destination = current_path + '/converted'


def correlate():
    # GET all folders that ends with _logs
    list_macro = glob.glob(current_path + '/*_logs/*.db', recursive=True)

    global_list = []
    robots = []

    for el in list_macro:
        robots_list_paths = glob.glob(el + '/*', recursive=True)
        for rob in robots_list_paths:
            global_list.append(rob)
            rob = rob.split('/')
            robot_name = rob[len(rob) - 1]
            if not robot_name in robots:
                robots.append(robot_name)

    for robot in robots:
        list_r_paths = [x for x in global_list if x.endswith(robot)]
        output_file = current_path + '/robotic_log/' + robot + '_merged.csv'
        index = 1
        line_count = 0

        # checks if the merge has already been done
        if os.path.exists(output_file):
            with open(output_file, 'r') as scraped:
                final_line = scraped.readlines()[-1]
                index = int(final_line.split(',')[-1]) + 1

        for r in list_r_paths:
            line_index = 0
            csv_file = glob.glob(r + "/merged.csv", recursive=True)[0]
            with open(csv_file, 'r') as fileR, open(output_file, 'a') as fileW:
                csv_reader = csv.reader(fileR, delimiter=',')  # csv reader
                csv_writer = csv.writer(fileW, delimiter=',')  # csv writer
                for row in csv_reader:
                    if line_index != 0:
                        # update file
                        row.append(index)
                        csv_writer.writerow(row)
                    else:  # update the header row
                        if index == 1:  # only the first time
                            row.append('Case_ID')
                            csv_writer.writerow(row)
                    line_index += 1
                    line_count += 1
            index += 1
            

def merging():
    rob_logs = glob.glob(current_path + '/robotic_log', recursive=True)
    for rob in rob_logs:
        csv_to_xes(rob)
    
    merge_xes(rob_logs)

def main():
    l = glob.glob(current_path + '/2022-*', recursive=True)
    
    ### ENRICHMENT ###
    # enrich odometry info with macro activities
    for i in l:
        i = i.split('/')
        i = i[len(i)-1]
        spatial_info(i)

    ### CORRELATION ###
    correlate()
    
    ### MERGING ###
    merging()

    # move merged files into another folder
    for i in l:
        shutil.move(i, destination)


if __name__ == '__main__':
    main()
