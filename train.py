#данные, на которых строилась модель
#python train.py input.txt model.txt True https://www.mushroom-ebooks.com/authors/angers_renee/samplers/ANGERSGarden%28Sampler%29.html

import re
import fileinput
import argparse
import pickle
import requests
from bs4 import BeautifulSoup

#получение данных из консоли
parser = argparse.ArgumentParser()
parser.add_argument("input", nargs='?', help="путь к директории, в которой лежит коллекция документов", default="stdin")
parser.add_argument("model", help="путь к файлу, в который сохраняется модель")
parser.add_argument("lc", nargs='?', help="lowercase", default=False)
parser.add_argument("url", nargs='?', help="адрес сайта")
args = parser.parse_args()

def workWithSite():
    #взятие текста с сайта
    r = requests.get(args.url, 'r')
    # получение html кода страницы
    htmlcode = BeautifulSoup(r.text, "html.parser")
    #извлечение текстовых данных из html
    textonly = ''.join([e for e in htmlcode.recursiveChildGenerator()
             if isinstance(e, str)])
    #запись в файл, из которого берутся данные
    with open(args.input, 'wb') as f:
        f.write(textonly.encode())


def first(word):
    global d
    d['begin'] = {}
    if word in d['begin'].keys():
        d['begin'][word] += 1
    else:
        d['begin'][word] = 1

def func(d, line):
    line = line.decode()
    if args.lc:
        line = line.lower()
    line = line.rstrip()
    words = re.split(r'[;,\s\.\?\!\'\"`\* ]', line)

    for i in range(len(words)):
        #new word
        if words[i] not in d.keys():
            d[words[i]] = {}

        #first word
        if i == 0:
            first(words[0])

        #last word
        if i == len(words) - 1:
            d[words[i]]['end'] = 1
            continue

        twd = d[words[i]] #this word dict
        nextword = words[i + 1]
        if nextword in twd.keys():
            twd[nextword] += 1
        else:
            twd[nextword] = 1
        d['*'] += 1


d = dict()
d['*'] = 0
workWithSite()
#генерация словаря
if args.input != 'stdin':
    with open(args.input, 'rb') as fin:
        for line in fin:
            func(d, line)
else:

    for line in fileinput.input():
        func(d, line)

#сохранение модели в файл
with open(args.model, 'wb') as model:
    pickle.dump(d, model, protocol=0)
