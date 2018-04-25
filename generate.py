#данные, на которых строилась модель
#python generate.py model.txt 30 output.txt

import argparse
import random
import pickle
import fileinput

parser = argparse.ArgumentParser()
parser.add_argument("model", help="путь к файлу, из которого загружается модель")
parser.add_argument("length", help="длина генерируемой последовательности", type=int)
parser.add_argument("output", nargs='?', help="файл, в который будет записан результат", default='stdout')
parser.add_argument("seed", nargs='?', help="начальное слово", default='')

args = parser.parse_args()
seed = args.seed
length = int(args.length)
with open(args.model, 'rb') as model:
    d = pickle.load(model)

if args.output != 'stdout':
    output = open(args.output, 'w')
else:
    output = fileinput.output()

if seed == '':
    seed = random.choice(list(d.keys()))
output.write(seed + ' ') #write

for i in range(length - 1):
    seed = random.choice([k for k in d[seed] for dummy in range(int(d[seed][k]))])
    if seed == 'end':
        seed = random.choice([k for k in d['begin'] for dummy in range(int(d['begin'][k]))])
    output.write(seed + ' ')
