import csv
import requests
import re
from collections import Counter
from bs4 import BeautifulSoup

# TODO
# Write data to CSV
# Finalize keywords / skip words

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

start_page = 1
num_pages = 1

jobs_scraped = dict()
word_frequencies = dict()
keyword_frequencies = dict()

total_jobs_scraped = 0
total_word_frequencies = Counter()
total_keyword_frequencies = Counter()

#locations = ['USA']
locations = ['Nashville', 'Los Angeles', 'San Francisco']

skip_words = ['and', 'to', 'the', 'of', 'in', 'with', 'a', 'for', 'on', 'or', 'is', 'as', 'be', '', 'we', 'an', 'you',
            'are', 'our', 'will', 'that', 'have', 'from', 'this', 'at', 'all', 'this', 'you', 'are', '/', 'your', 'not',
            'who', 'it', '2', 'any', 'well', 'by', 'do', 'if', 'can', 'what', 'has', '-', 'their', 'us']

keywords = ['.net', 'c#', 'sql', 'c++', 'java', 'c', 'python', 'nodejs', 'node.js', 'css', 'css3', 'html', 'html5', 
            'javascript', 'jquery', 'php', 'r', 'ruby', 'rust', 'vhdl', 'verilog', 'typescript' 'perl', 'assembly',
            'asm', 'lua', 'fortran', 'apex', 'salesforce', 'aws', 'bash', 'shell', 'powershell', 'swift', 'scala',
            'vba', 'objective-c', 'kotlin', 'rest', 'api', 'apis', 'js', 'mysql', 'postgressql', 'mongodb', 'git',
            'ssis', 'ssrs', 'powerbi', 'power', 'bi', 'devops', 'react.js', 'reactjs', 'node', 'react', 'angular',
            'angularjs', 'docker']

for location in locations:

    jobs_scraped[location] = 0
    word_frequencies[location] = Counter()
    keyword_frequencies[location] = Counter()

    for page in range(start_page, start_page + num_pages):

        url_loc = location.replace(' ', '+')

        url = 'https://www.careerjet.com/developer-jobs.html?p=' + str(page) + '&l=' + url_loc + '&radius=25'
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, 'html.parser')

        if 'No results' in soup.find('h1').text:
            print(location + ': No results found on page ' + str(page) + '. Moving to next location...')
            break

        print(location + ': scraping page ' + str(page) + ' (' + str(page - start_page + 1) + '/' + str(num_pages) + ')')

        soup = soup.find_all('article', attrs={'data-url': True})

        # print(soup[0]['data-url'])
        #for i in soup:
            #print(i['data-url'])

        for job in soup:
            job_url = 'https://www.careerjet.com/' + job['data-url']
            req = requests.get(job_url, headers=headers)
            job_soup = BeautifulSoup(req.content, 'html.parser')

            job_soup = job_soup.find('section', class_='content').text

            # Remove punctuation from text except periods (we want to keep those in node.js or .net for example)
            job_soup = re.sub(r"[,:;@?!&$/]+\ *", " ", job_soup)

            # Remove periods with whitespace after it and at end of string
            job_soup = re.sub(r"[.]+\s", " ", job_soup)
            job_soup = re.sub(r"[.]+$", " ", job_soup)

            # Remove parentheses
            job_soup = re.sub(r'[()]', " ", job_soup)

            # Make text all lowercase and split text into array of individual words
            words_list = job_soup.lower().split()
            #print(words_list)

            for word in words_list:

                if word in keywords:
                    keyword_frequencies[location][word] += 1
                
                if word not in skip_words:
                    word_frequencies[location][word] += 1

            jobs_scraped[location] += 1

for location in locations:
    top_words = word_frequencies[location].most_common(100)

    print('\n' + location.upper() + '\n# jobs scraped: ' + str(jobs_scraped[location]))
    print('\n' + location + ' Top Words: ')
    print(top_words)
    print('\n' + location + ' Keywords: ')
    print(keyword_frequencies[location])
    print('\n')

    total_jobs_scraped += jobs_scraped[location]
    total_word_frequencies += word_frequencies[location]
    total_keyword_frequencies += keyword_frequencies[location]

top_words = total_word_frequencies.most_common(100)
top_keywords = total_keyword_frequencies.most_common()

print('\nTOTAL # JOBS SCRAPED: ' + str(total_jobs_scraped))
print('\nTOP WORDS: ')
print(top_words)
print('\nTOP KEYWORDS: ')
print(total_keyword_frequencies)

with open('data/total.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    fieldnames = ['TOP 100 WORDS OVERALL', 'COUNT']
    writer.writerow(fieldnames)
    for key, value in top_words:
        writer.writerow([key] + [value])

with open('data/total_keywords.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    fieldnames = ['TOP KEYWORDS OVERALL', 'COUNT']
    writer.writerow(fieldnames)
    for key, value in top_keywords:
        writer.writerow([key] + [value])

for location in locations:

    with open('data/' + location.replace(" ", "") + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        top_words = word_frequencies[location].most_common(50)

        fieldnames = [location.upper() + ' TOP 50 WORDS', 'COUNT']
        writer.writerow(fieldnames)
        for key, value in top_words:
            writer.writerow([key] + [value])

    with open('data/' + location.replace(" ", "") + '_keywords.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        top_keywords = keyword_frequencies[location].most_common()

        fieldnames = [location.upper() + ' TOP KEYWORDS', 'COUNT']
        writer.writerow(fieldnames)
        for key, value in top_keywords:
            writer.writerow([key] + [value])