import csv

# Initialization of DataFrame variables
rows = []

# @@@ create pandas frame and add items except for the first time
# Load extracted output file
with open("/home/pafr/repos/personal_finance_tracker/transform/sample_output.csv", "r") as f:
    reader = csv.reader(f, delimiter="|")
    for current_line_list in reader:
        # removing 
        stripped_line = [line.strip() for line in current_line_list]
        rows.append()

# ---> @@@ : create DataFrame at beginning and instantly append to the frame isntead of making more lists
        

# @ cluster table into proper format
# -> Remove first 2 lines
# -> Delimiter: Pipe

# @ assign expense to corresponding category