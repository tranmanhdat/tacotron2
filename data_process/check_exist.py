import os
with open('training.txt', 'r', encoding="utf8") as fd:
    for line in fd:
        elements = line.split("|")
        if os.path.isfile(elements[0]):
            continue
        else:
            print(elements[0])

with open('testing.txt', 'r', encoding="utf8") as fd:
    for line in fd:
        elements = line.split("|")
        if os.path.isfile(elements[0]):
            continue
        else:
            print(elements[0])