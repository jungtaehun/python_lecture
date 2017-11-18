import string
from urllib import request
import pickle


stopword = []
num = 0
with open('stopword.txt', 'r') as f:
    for line in f:
        if (line != "\n"):
            stopword.append(line.strip())
stopword.append("nbsp")
stopword.append("lt")
stopword.append("gt")
stopword.append("amp")
stopword.append("quot")
stopword.append("pm")
stopword.append("et")
stopword.append("est")

with open('print.txt', 'w') as p:
    # urls = ['http://edition.cnn.com/', 'https://www.nytimes.com/', 'http://abcnews.go.com/', 'http://www.reuters.com/','https://www.washingtonpost.com/','https://techcrunch.com/', 'https://www.bloomberg.com/asia', 'https://thenextweb.com/','https://www.theverge.com/', 'http://fortune.com/']
    urls = ['www.cnn.com', 'www.nytimes.com', 'abcnews.go.com', 'www.reuters.com',
            'www.theverge.com']

    for url in urls:
        total_word = 0
        words = []
        dic = {}
        javascript_check = False
        css_check = False

        f = request.urlopen('http://' + url)
        source_bytes = f.read()
        source = source_bytes.decode('utf-8')
        with open(str(url) + '.html', "w") as html:
            html.write(source)

        for i in source.split("<"):
            m = i.split(">")
            print(m)
            p.write(str(m))
            p.write("\n")

            if len(m) > 1:
                check = m[0].split()
                if len(check) > 0:
                    # if('script' in m[0] and m[0].find("description") == -1 and m[0].find("subscription") == -1 and m[0].find("transcript") == -1 and m[0].find(" javascript:void();") == -1): javascript_check = True
                    if ('script' == check[0]): javascript_check = True
                    if ('/script' in m[0]): javascript_check = False
                    # if(m[0].find('style') != -1 and m[0].find('style=') == -1 and m[0].find('stylesheet') == -1and m[0].find('Lifestyle') == -1): css_check = True
                    if ('style' == check[0]): css_check = True
                    if ('/style' in m[0]): css_check = False
                    print(javascript_check, css_check)
                    p.write(str(javascript_check) + " " + str(css_check))
                    p.write("\n")
                    m = m[1].strip().lower()
                    if (m != "" and not javascript_check and not css_check):
                        rep = ["//", "--", '\'', '$', '©', '&', '%', '"', '^', 'ⓒ', '·', '…', '—', '~', '–', '»', '!',
                               '”', '㈜', '-', '/', ':', '(', ')', '[', ']', '_', '“', '‘', '’', '.', ',']
                        rep = rep + list(string.punctuation)
                        rep = list(set(rep))
                        for r in rep:
                            m = m.replace(r, ' ')
                        m = m.split()
                        # print(m)
                        for n in m:
                            if (n != ''):
                                if (n.isdigit()):
                                    continue
                                else:
                                    if (n not in stopword):
                                        total_word += 1
                                        words.append(n.strip())
                                        # print(n.strip())
        for i in words:
            if (i not in dic):
                dic[i] = 1
            else:
                dic[i] = dic[i] + 1


        items = list(dic.items())
        items.sort(key=lambda d: d[1], reverse=True)

        with open(str(url) + '.words.frequency', 'wb') as plk:
            pickle.dump(items, plk)
        num = num + 1

        for k, v in items:
            print(k, v)
            p.write(str(k) + " " + str(v))
            p.write("\n")
        print()
        p.write("\n")
        p.write("\n")