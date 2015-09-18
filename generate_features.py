import datetime
import os
import re
import sys
from bs4 import BeautifulSoup as bs

def clean_text(s):
    try:
        s = re.sub(r'[\n\t,.:;()\-\/_]+', ' ', s)
        s = re.sub(r'\s{2,}', ' ', s)
        s = s.strip()
        s = s.lower()
        return s
    except Exception as e:
        #print 'failed to clean up text: {0}'.format(e)
        return ''

def parse_text(soup):
    texts = []
    try:
        for text in soup.find_all('p'):
            try:
                texts.append(clean_text(text.text.encode('ascii','ignore')))
            except Exception as e:
                #print 'failed to parse paragraph: {0}'.format(e)
                pass
    except Exception as e:
        #print 'failed to parse text: {0}'.format(e)
        pass
    return filter(None,texts)

def parse_title(soup):
    title = ''
    try:
        title = clean_text(soup.title.string.encode('ascii','ignore'))
    except Exception as e:
        #print 'failed to parse title: {0}'.format(e)
        pass
    return title

def parse_links(soup):
    links = []
    for link in soup.find_all('a'):
        try:
            links.append(str(link.get('href').encode('ascii','ignore')))
        except Exception as e:
            #print 'failed to parse link: {0}'.format(e)
            pass
    return filter(None,links)

def parse_images(soup):
    images = []
    for image in soup.findAll("img"):
        try:
            images.append("%(src)s"%image)
        except Exception as e:
            #print 'failed to parse image: {0}'.format(e)
            pass
    return filter(None,images)

def extract_features(input_dir, file_name):
    with open(input_dir + os.sep + file_name, 'r') as file:
        soup = bs(file, 'html.parser')

    title = parse_title(soup)
    n_title_chars = len(title)
    n_title_words = len(title.split(' '))

    links = parse_links(soup)
    n_links = len(links)

    images = parse_images(soup)
    n_images = len(links)

    texts = ''.join(parse_text(soup))
    n_paragraphs = len(texts)
    text = ' '.join(texts)
    n_chars = len(text)
    n_words = len(text.split(' '))

    links_per_words = 0
    if n_words > 10:
        links_per_words = 1.0 * n_links / n_words

    images_per_words = 0
    if n_words > 10:
        images_per_words = 1.0 * n_images / n_words

    return [
        file_name,
        n_title_chars,
        n_title_words,
        n_links,
        n_images,
        n_paragraphs,
        n_chars,
        n_words,
        links_per_words,
        images_per_words
    ]

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
