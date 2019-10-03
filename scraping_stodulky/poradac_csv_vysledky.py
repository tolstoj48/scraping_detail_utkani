import csv

with open('items.csv','r') as csvinput:
    with open('final.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        row.append('Tým')
        all.append(row)
        listy=["A-tým", "B-tým", "C-tým", "Starší dorost", "Mladší dorost", "Starší žáci", "Mladší žáci A", "Mladší žáci B", "Mladší žáci C"]
        i=0
        for row in reader:
            row.append(listy[i])
            all.append(row)
            i+=1

        writer.writerows(all)

import time
now = time.strftime("%d-%m-%Y")
now=str(now)+".csv"

with open('final.csv', 'r') as infile, open(now, 'w') as outfile:
    # output dict needs a list for new column ordering
    fieldnames = ["Tým", "Soutěž", "Kolo", "Datum_a_čas_utkání", "Soupeři", "Výsledek_utkání", 'Sestava', 'Náhradníci', 'Góly_Sokola']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)

import os
os.remove("final.csv")
os.remove("items.csv")
print("Files Removed!")
