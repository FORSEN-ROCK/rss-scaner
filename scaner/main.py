import exeptions
import data_stream
import analitics


if __name__ == '__main__':

    file_out = open(r'C:\projects\rss-scaner\out\load_data.csv', 'wb')
    items = data_stream.stream(r'C:\projects\rss-scaner\rss-links\links.txt')

    for item in items:
        for article in items[item]:
            prefix = item + ';'
            file_out.write(prefix.encode('utf-8') + str(article).encode('utf-8'))

    file_out.close()

    analitics.count_word(items)
    