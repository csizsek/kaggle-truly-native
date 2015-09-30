from collections import defaultdict
import re
import sys

dict_file_name = sys.argv[1]
"""
0 http 1158892 178949
1 will 1002788 209766
2 post 950947 196638
3 comment 939302 192085
4 time 893742 200203
"""

docs_file_name = sys.argv[2]
"""
1000188_raw_html.txt | impact:1  shadow:1  | sector:4 bigger:1 aspect:1 har:1 intellig:1
1000326_raw_html.txt | short:1  timeless:1  guid:1  overcom:1  failur:1  | mistak:9 inner:3 piec:1 shape:1 min
1000542_raw_html.txt | mexican:1  drug:1  cartel:1  truthdig:1  dea:1  launder:1  money:1  | sacrific:1
1000638_raw_html.txt | illustr:1  kristin:1  vestgrd:1  | litchfield:1 held:1 facebook:1 rss:3 birodesign:1
1000662_raw_html.txt | mommi:1  | gluten:1  free:1  play:1  dough:1
"""

output_file_name = sys.argv[3]

top_set_sizes = [
    100,
    300,
    1000,
    3000,
    10000,
    30000
]

top_sets = {}

for n in top_set_sizes:
    top_sets[n] = set()

i = 0
with open(dict_file_name) as dict_file:
    for line in dict_file.readlines():
        word =  line.strip().split(' ')[1].strip()
        i += 1
        for n in top_set_sizes:
            if i <= n:
                top_sets[n].add(word)

re_wss = re.compile('\s+')
with open(docs_file_name) as docs_file:
    with open(output_file_name, 'w') as output_file:
        for line in docs_file.readlines():
            line = line.strip()
            doc_name = line.split('|')[0].strip()
            word_counts = line.split('|')[2].strip()
            n_words = 0
            prec = defaultdict(int)
            rec = defaultdict(set)
            for word_count in re_wss.split(word_counts):
                if not word_count:
                    continue
                word = word_count.split(':')[0]
                count = int(word_count.split(':')[1])
                n_words += int(count)
                for n in top_set_sizes:
                    if word in top_sets[n]:
                        prec[n] += count
                        rec[n].add(word)
            ret = [doc_name]
            for n in top_set_sizes:
                if n_words > 0:
                    ret.append(1.0 * prec[n] / n_words)
                else:
                    ret.append(0)
                ret.append(1.0 * len(rec[n]) / n)
            output_file.write(','.join(str(x) for x in ret))
            output_file.write('\n')
