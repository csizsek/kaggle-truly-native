import datetime
import os
import re
import sys
from bs4 import BeautifulSoup as bs

exception_action = 'PRINT'

def handle_exception(e):
    if exception_action == 'NOTHING':
        return
    elif exception_action == 'PRINT':
        print(e)
    elif exception_action == 'RAISE':
        raise e

def clean_text(s):
    try:
        s = re.sub(r'[^A-Za-z]+', ' ', s)
        s = re.sub(r'\s{2,}', ' ', s)
        s = s.strip()
        s = s.lower()
        return s
    except Exception as e:
        handle_exception(e)
        return ''

def parse_text(soup):
    texts = []
    try:
        for text in soup.find_all('p'):
            try:
                texts.append(text.text.encode('ascii','ignore'))
            except Exception as e:
                handle_exception(e)
    except Exception as e:
        handle_exception(e)
    return filter(None,texts)

def parse_title(soup):
    title = ''
    try:
        t = soup.title
        title = clean_text(str(t))
    except Exception as e:
        handle_exception(e)
    return title

def parse_links(soup):
    links = []
    for link in soup.find_all('a'):
        try:
            link_url = link.get('href')
            if link_url:
                links.append(str(link_url.encode('ascii','ignore')))
        except Exception as e:
            handle_exception(e)
    return filter(None,links)

def parse_images(soup):
    images = []
    for image in soup.findAll('img'):
        try:
            if hasattr(image, 'src') and image.src:
                images.append("%(src)s"%image)
            else:
                images.append('')
        except Exception as e:
            handle_exception(e)
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
    ctext = clean_text(text)
    words = re.split('\s+', ctext)
    n_words = len(words)
    avg_word_length = 0.0
    for w in words:
        avg_word_length += len(w)
    avg_word_length /= n_words

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
        n_words,
        avg_word_length
    ]

    for feature in values.keys():
        ret.append(values[feature])
        feature_per_words = 0.0
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
