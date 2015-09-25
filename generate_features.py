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
                texts.append(text.text.encode('ascii','ignore'))
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

    values = {}

    title = parse_title(soup)
    n_title_chars = len(title)
    n_title_words = len(title.split(' '))

    links = parse_links(soup)
    values['n_links'] = len(links)

    images = parse_images(soup)
    values['n_images'] = len(links)

    texts = parse_text(soup)
    n_paragraphs = len(texts)
    text = ' '.join(texts)
    n_chars = len(text)
    n_words = len(re.split('\s+', text))

    values['n_lines'] = text.count('\n')
    values['n_spaces'] = text.count(' ')
    values['n_tabs'] = text.count('\t')
    values['n_braces'] = text.count('{')
    values['n_brackets'] = text.count('[')
    values['n_dashes'] = text.count('-')
    values['n_dots'] = text.count('.')
    values['n_bangs'] = text.count('!')
    values['n_eqs'] = text.count('=')
    values['n_pluses'] = text.count('+')

    ret =  [
        file_name,
        n_title_chars,
        n_title_words,
        n_paragraphs,
        n_chars,
        n_words
    ]

    for feature in values.keys():
        ret.append(values[feature])
        feature_per_words = 0
        if n_words > 10:
            feature_per_words = 1.0 * values[feature] / n_words
            ret.append(feature_per_words)

    return ret

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
        if i % 100 == 0:
            with open(output_file_name, 'a') as output_file:
                for row in rows:
                    output_file.write(row + '\n')
                    rows = []
            print '#{i:06d} {file_name:>25} {time}'.format(
                i=i,
                file_name=file_name,
                time=date.strftime('%Y-%m-%d %H:%M:%S'))
