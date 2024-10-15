# import os
# # print (os.getcwd())

# load output file
import csv
with open("./sample_output.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):
        print("line[{}] = {}".format(i, line))

# cluster table in proper format

# assign expense to corresponding category