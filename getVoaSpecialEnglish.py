import requests
import lxml.html
import json
import re

def fetchHtml(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise
    return response.text

def readHtml(url):
    with open("VOA_Special_English_Word_Book.html", "r") as f:
        html = f.read()
    return html

def getItemTypeA(w, t):
    words = []
    result = re.findall('([a-z]+\.) (.+?)(?=; [a-z]+\.|$)', t)
    if result:
        for r1, r2 in result:
            word = {}
            word['word'] = w
            word['pos'] = r1
            word['define'] = r2
            words.append(word)
        return words

    result = re.match(' – (.+?)$', t)
    if result:
        word = {}
        word['word'] = w
        word['pos'] = 'science programs'
        word['define'] = result.group(1)
        return [word]

    return words

def getItemTypeB(w, t):
    word = {}
    result = re.match(' : (.*)$', t)
    if result:
        word['word'] = w
        word['pos'] = 'common prefix'
        word['define'] = result.group(1)
    return [word]

def getItemTypeC(t):
    word = {}
    result = re.match('(.*) – (.*)$', t)
    if result:
        word['word'] = result.group(1)
        word['pos'] = 'common expression'
        word['define'] = result.group(2)
    return [word]

def getItem(item_html):
    item = lxml.html.fromstring(item_html)
    if(len(item.xpath('//li/a/text()'))):
        w = item.xpath('//li/a/text()')[0]
        t = item.xpath('//li/text()')[0]
        word = getItemTypeA(w, t)
    elif(len(item.xpath('//li/span/text()'))):
        w = item.xpath('//li/span/text()')[0]
        t = item.xpath('//li/text()')[0]
        word = getItemTypeB(w, t)
    elif(len(item.xpath('//li/text()'))):
        t = item.xpath('//li/text()')[0]
        word = getItemTypeC(t)

    return word

def parseHtml(html):
    element = lxml.html.fromstring(html)
    collect = element.xpath('//div[@id="mw-content-text"]/div[@class="mw-parser-output"]/div/ul/li')
    ox_words = []
    for item in collect:
        item_string = lxml.html.tostring(item)
        word = getItem(item_string)
        ox_words.extend(word)
    return ox_words

def convertToJson(words):
    # json_words = json.dumps(words)
    # json_words = json.dump(words, ensure_ascii=False, indent=4, separators=(',', ': '))
    with open('specialenglish_words.json', 'w') as f:
        json.dump(words, f, ensure_ascii=False, indent=4, separators=(',', ': '))

def main():
    # fetch html
    url = 'https://simple.m.wikipedia.org/wiki/Wikipedia:VOA_Special_English_Word_Book'
    html = fetchHtml(url)
    # html = readHtml(url)

    # parse html
    words = parseHtml(html)

    # save json
    convertToJson(words)

    print('{} words\n'.format(len(words)))


if __name__ == '__main__':
    main()
