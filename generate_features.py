import datetime
import os
import sys

from bs4 import BeautifulSoup as bs

def parse_text(soup):
    texts = ['']
    for text in soup.find_all('p'):
        try:
            texts.append(text.text.encode('ascii','ignore').strip())
        except Exception:
            continue
    return filter(None,texts)

def parse_title(soup):
    title = ['']
    try:
        title.append(soup.title.string.encode('ascii','ignore').strip())
    except Exception:
        return title
    return filter(None,title)

def parse_links(soup):
    links = ['']
    for link in soup.find_all('a'):
        try:
            links.append(str(link.get('href').encode('ascii','ignore')))
        except Exception:
            continue
    return filter(None,links)

def parse_images(soup):
    images = ['']
    for image in soup.findAll("img"):
        try:
            images.append("%(src)s"%image)
        except Exception:
            continue
    return filter(None,images)

def extract_features(input_dir, file_name):
    with open(input_dir + os.sep + file_name, 'r') as file:
        soup = bs(file, 'html.parser')
    texts = parse_text(soup)
    title = parse_title(soup)
    links = parse_links(soup)
    images = parse_links(soup)
    return [file_name, 0.1]

if __name__ == '__main__':
    input_dir_name = sys.argv[1]
    output_file_name = sys.argv[2]

    if not os.path.exists(input_dir_name):
        print "input dir does not exist"
        sys.exit()

    i = 0
    rows = []
    for file_name in os.listdir(input_dir_name):
        i += 1
        row = ','.join([str(f) for f in extract_features(input_dir_name, file_name)])
        rows.append(row)
        date = datetime.datetime.now()
        if i % 10 == 0:
            with open(output_file_name, 'a') as output_file:
                for row in rows:
                    output_file.write(row + '\n')
                    rows = []
            print '#{i:06d} {file_name:>25} {time}'.format(
                i=i,
                file_name=file_name,
                time=date.strftime('%Y-%m-%d %H:%M:%S'))
