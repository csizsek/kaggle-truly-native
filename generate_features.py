import datetime
import os
import re
import sys
import urlparse
from bs4 import BeautifulSoup as bs


def handle_exception(e):
    #return
    print(e)
    #raise e

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
    return links

def parse_images(soup):
    images = []
    for image in soup.findAll('img'):
        try:
            images.append(image['src'])
        except Exception as e:
            pass
    return images

def get_soup(input_dir, file_name):
    with open(input_dir + os.sep + file_name, 'r') as file:
        soup = bs(file, 'html.parser')
        return soup

def get_raw(input_dir, file_name):
    with open(input_dir + os.sep + file_name, 'r') as file:
        raw = file.read()
        return raw

def extract_features(input_dir, file_name):
    soup = get_soup(input_dir, file_name)
    raw = get_raw(input_dir, file_name)

    # title related features
    title = parse_title(soup)
    n_title_chars = len(title)
    n_title_words = len(title.split(' '))

    # link related features
    links = parse_links(soup)
    n_links = len(links)
    n_links_rel = 0
    n_links_abs = 0
    n_links_domain_com = 0
    n_links_domain_org = 0
    n_links_scheme_none = 0
    n_links_scheme_http = 0
    n_links_scheme_https = 0
    n_links_path_nonempty = 0
    n_links_ad = 0
    n_links_utm = 0
    for l in links:
        try:
            pl = urlparse.urlparse(l)

            if pl.netloc == '':
                n_links_rel += 1
            else:
                n_links_abs += 1

            domain = pl.netloc.split('.')[-1]
            if domain == 'com':
                n_links_domain_com += 1
            elif domain == 'org':
                n_links_domain_org += 1

            if pl.scheme == '':
                n_links_scheme_none += 1
            elif pl.scheme == 'http':
                n_links_scheme_http += 1
            elif pl.scheme == 'https':
                n_links_scheme_https += 1

            if pl.path != '':
                n_links_path_nonempty += 1

            n_links_ad += re.split('\W', l).count('ad')

            if 'utm_' in l:
                n_links_utm += 1
        except Exception as e:
            handle_exception(e)

    # image related features
    images = parse_images(soup)
    n_imgs = len(images)
    n_imgs_rel = 0
    n_imgs_abs = 0
    n_imgs_fmt_jpg = 0
    n_imgs_fmt_gif = 0
    n_imgs_fmt_png = 0
    n_imgs_ad = 0
    n_imgs_utm = 0
    for i in images:
        try:
            pl = urlparse.urlparse(i)

            if pl.netloc == '':
                n_imgs_rel += 1
            else:
                n_imgs_abs += 1

            fmt = pl.path.split('.')[-1]
            if fmt == 'jpg':
                n_imgs_fmt_jpg += 1
            elif fmt == 'gif':
                n_imgs_fmt_gif += 1
            elif fmt == 'png':
                n_imgs_fmt_png += 1

            n_imgs_ad += re.split('\W', i).count('ad')

            if 'utm_' in i:
                n_imgs_utm += 1
        except Exception as e:
            handle_exception(e)

    # body related features
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

    # spec character related features
    n_lines = raw.count('\n')
    n_spaces = raw.count(' ')
    n_tabs = raw.count('\t')
    n_braces = raw.count('{')
    n_brackets = raw.count('[')
    n_dashes = raw.count('-')
    n_dots = raw.count('.')
    n_bangs = raw.count('!')
    n_eqs = raw.count('=')
    n_pluses = raw.count('+')
    n_x_pars = raw.count('(x)')
    n_x_pars += raw.count('(X)')
    n_x_pars += raw.count('[x]')
    n_x_pars += raw.count('[X]')

    ret =  [
        file_name,

        n_title_chars,
        n_title_words,

        n_links,
        n_links_rel,
        n_links_abs,
        n_links_domain_com,
        n_links_domain_org,
        n_links_scheme_none,
        n_links_scheme_http,
        n_links_scheme_https,
        n_links_path_nonempty,
        n_links_ad,
        n_links_utm,

        n_imgs,
        n_imgs_rel,
        n_imgs_abs,
        n_imgs_fmt_jpg,
        n_imgs_fmt_gif,
        n_imgs_fmt_png,
        n_imgs_ad,
        n_imgs_utm,

        n_paragraphs,
        n_chars,
        n_words,
        avg_word_length,

        n_lines,
        n_spaces,
        n_tabs,
        n_braces,
        n_brackets,
        n_dashes,
        n_dots,
        n_bangs,
        n_eqs,
        n_pluses,
        n_x_pars
    ]

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
