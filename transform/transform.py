# os
import os
print(os.getcwd())

# load extracted output file
import csv
with open("/home/pafr/repos/personal_finance_tracker/transform/sample_output.csv", "r") as f:
    reader = csv.reader(f, delimiter="|")
    for i, line_list in enumerate(reader):
        removed_space_list = [line.strip() for line in line_list]
        print(removed_space_list)

# cluster table into proper format
# -> Remove first 2 lines
# -> Delimiter: Pipe

# assign expense to corresponding category