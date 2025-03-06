from operator import le
import subprocess
import os
import zlib
import base64
import glob


current_path = os.path.dirname(os.path.realpath(__file__))

robot_nss = [
    f for f in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, f))
]

# ZLIB decodification
def decode(time_instant, name_dest):
    file_log = 'state.log'
    os.chdir(current_path + '/' + time_instant)
    #file_path = path + file_log
    gazebo_log = '<xml>'  # for python conversion

    with open(file_log, 'r') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line.startswith('<![CDATA'):
                compressed = stripped_line.removeprefix('<![CDATA[')
                #compressed = stripped_line.removesuffix(']]>')
                # print(compressed)

                t = base64.b64decode(compressed)  # translation to base64
                e = zlib.decompress(t)  # decompressed and encoded text
                text = e.decode("utf8")
                gazebo_log += text

    gazebo_log += '</xml>'

    file = open(name_dest + ".xml", "w+")
    file.write(gazebo_log)
    file.close()


# DB to CSV conversion
def convert(time_instant):
    subprocess.run(
        ['bash', '-c', 'source  ~/dev_ws/install/setup.bash'])

    path_name = current_path + '/' + time_instant
    print(path_name)
    os.chdir(path_name)
    check = False

    n_directories = os.listdir(path_name)

    # check if the conversion has already been done
    for dir in n_directories:
        if dir.endswith("_0.db"):
            check = True

    if not check:
        file_name = time_instant + "_0.db"

        for i in range(len(robot_nss)):
            subprocess.run(["mkdir", "-p", (file_name + '/' + robot_nss[i])])

        subprocess.run(["ros2bag-convert", (file_name + '3')])


def main():
    l = glob.glob(current_path + '/2022-*', recursive=True)
    for i in l:
        i = i.split('/')
        i = i[len(i)-1]
        convert(i)
        if i.endswith('_macro'):
            decode(i, 'world_state')


if __name__ == '__main__':
    main()
