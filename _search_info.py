import os

def gen_info(path):
    list = []
    try:
        with open(path, 'r') as f:
            line=f.readline()
            while line:
                list.append(line)
                line=f.readline()
            return list

    except FileNotFoundError:
        print(path + " has lost")