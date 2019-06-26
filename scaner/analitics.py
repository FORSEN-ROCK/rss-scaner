import re


def count_word(sources_of_data):
    articals = []
    all_words = []

    for artical in sources_of_data['http://www.kommersant.ru/RSS/news.xml']:
        word_count = {}
        words = re.findall('[А-ЯЁа-яё0-9A-Za-z\-]+',
                           artical.description)

        for word in words:

            normal_word = word.lower()

            if normal_word not in all_words:
                all_words.append(normal_word)

            if not word_count.get(normal_word):
                word_count[normal_word] = 1
            else:
                word_count[normal_word] += 1

        articals.append(word_count)

    ##print(articals)
    print(len(all_words))