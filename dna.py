import sys
import csv
import collections

# check number of command-line arguments and remind user of usage if incorrect
if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")

# get files from command-line arguments
database_file = sys.argv[1]
sequence_file = sys.argv[2]

# initialise empty database (list)
database = []

# open database file and import each row into the database as an OrderedDict
with open(database_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        database.append(row)

# get columns from database (name + STRs)
columns = list(database[0].keys())

# convert database STR repeat counts to integers
for person in database:
    # for each column except name
    for i in range(1, len(columns)):
        # convert value to integer
        person[columns[i]] = int(person[columns[i]])

# set up ordered dictionary to hold sequence's STR repeat counts - values are null/none by default
strep_repeat_counts = collections.OrderedDict.fromkeys(columns)

# get sequence
with open(sequence_file, 'r') as file:
    sequence = file.read().replace('\n', '')

# get max repeats for each STR in sequence
# from first STR to last STR (column 0 would be name)
for i in range(1, len(columns)):
    strep = columns[i]
    length = len(strep)
    max_repeats = 0

    # iterate over characters in sequence
    for character in range(len(sequence)):
        repeats = 0
        keep_checking = True
        check_from = character
        while keep_checking == True:
            if sequence[check_from:check_from + length] == strep:
                repeats += 1
                check_from += length
            else:
                keep_checking = False
        if repeats > max_repeats:
            max_repeats = repeats

    # save max_repeats to STR repeat counts dictionary
    strep_repeat_counts[strep] = max_repeats

# check sequence repeat counts against database repeat counts
keep_checking = True
person = 0

while keep_checking == True:
    unmatched_streps = 0

    # from first STR to last STR (column 0 would be name)
    for i in range(1, len(columns)):
        key = columns[i]
        if database[person][key] != strep_repeat_counts[key]:
            unmatched_streps += 1

    # if there are no mismatches in the max repeats
    if unmatched_streps == 0:
        keep_checking = False
        print(database[person]['name'])
    # else if it's not a match and there are no more people to check
    elif person == len(database) - 1:
        print("No match")
        keep_checking = False
    # else move to next person
    else:
        person += 1