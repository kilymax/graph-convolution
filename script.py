import csv

count = 0

with open('test.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile, dialect='excel' , delimiter=' ', quotechar='|')
    for row in reader:
        print(row)
        count += 1


print(type(reader))
print(count)