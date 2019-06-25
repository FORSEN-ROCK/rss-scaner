import re

import exeptions
import data_stream
#import analitics


if __name__ == '__main__':

    file_out = open(r'C:\projects\rss-scaner\out\load_data.csv', 'wb')
    items = data_stream.stream(r'C:\projects\rss-scaner\rss-links\links.txt')

    for item in items:
        for article in items[item]:
            prefix = item + ';'
            file_out.write(prefix.encode('utf-8') + str(article).encode('utf-8'))

    file_out.close()

    word_count = {}

    for artical in items['https://lenta.ru/rss']:
        for word in artical.description.split(' '):

            normal_word = word.lower()
            normal_word = re.findall(
                            #'[^#\d+\s][А-ЯЁа-яё.\d\-\_\:]+',
                            '\S+',
                             normal_word
            )
            normal_word = str('').join(normal_word)

            if not word_count.get(normal_word):
                word_count[normal_word] = 1
            else:
                word_count[normal_word] += 1

    print(word_count)
    