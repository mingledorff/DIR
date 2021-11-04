import os
import csv
from collections import Counter

total_words = Counter()
total_keywords = Counter()
total_jobs = 0

for file in os.listdir('data/states/'):
    if file.endswith(".csv") and "total" not in file:
        print(file)

        with open('data/states/' + file, mode='r') as csvfile:
            reader = csv.reader(csvfile)
            row = next(reader)

            if "keywords" in file:
                num_jobs = int(row[0].rpartition(' ')[0].partition('(')[2])
                #print(num_jobs)
                total_jobs += num_jobs

            dict_from_csv = {rows[0]: int(rows[1]) for rows in reader}

        count = Counter(dict_from_csv)
        #print(count)

        if "keywords" in file:
            total_keywords += count
        else:
            total_words += count

top_words = total_words.most_common()
top_keywords = total_keywords.most_common()

with open('data/total_states.csv', mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    fieldnames = ['TOP WORDS OVERALL (' + str(total_jobs) + ' JOBS)', 'COUNT']
    writer.writerow(fieldnames)
    for key, value in top_words:
        writer.writerow([key] + [value])

with open('data/total_keywords_states.csv', mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    fieldnames = ['TOP KEYWORDS OVERALL (' + str(total_jobs) + ' JOBS)', 'COUNT']
    writer.writerow(fieldnames)
    for key, value in top_keywords:
        writer.writerow([key] + [value])
