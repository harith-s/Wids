import random
import csv
l =[]
for i in range(4119):
    j = random.randint(<min>, <max>)
    l.append(j)

with open("data.csv", 'w', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['index', 'number'])
    for j in range(len(l)):
        csv_writer.writerow([j, l[j]])
    