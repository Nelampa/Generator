import re
import fileinput
import argparse
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("input", help="путь к директории, в которой лежит коллекция документов", default="stdin")
parser.add_argument("model", help="путь к файлу, в который сохраняется модель")
parser.add_argument("lc", help="lowercase", default=False)
args = parser.parse_args()

def func(line):
    global d
    if args.lc:
        line = line.lower()
    line = line.rstrip()
    words = re.split(r'[;,\s\.\?\!]', line)
    for i in range(len(words)):
        if words[i] not in d.keys():
            d[words[i]] = {}
        if i == 0:
            d['begin'] = {}
            if words[i] in d['begin'].keys():
                d['begin'][words[i]] += 1
            else:
                d['begin'][words[i]] = 1
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

if args.input != 'stdin':
    fin = open(args.input)
else:
    fin = fileinput.input()

#генерация словаря
for line in fin:
    func(line)

#сохранение модели в файл
model = open(args.model, 'wb')
pickle.dump(d, model, protocol=0)
