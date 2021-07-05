import re
from num2words import num2words
from unicodedata import normalize
import os

def vi_num2words(num):
   return num2words(num, lang='vi')

def convert_time_to_text(time_string):
   # Support only hh:mm format
   try:
       h, m = time_string.split(":")
       time_string = vi_num2words(int(h)) + " giờ " + vi_num2words(int(m)) + " phút"
       return time_string
   except:
       return None

def replace_time(text):
   # Define regex to time hh:mm
   result = re.findall(r'\d{1,2}:\d{1,2}|', text)
   match_list = list(filter(lambda x : len(x), result))

   for match in match_list:
       if convert_time_to_text(match):
           text = text.replace(match, convert_time_to_text(match))
   return text

def replace_number(text):
   return re.sub('(?P<id>\d+)', lambda m: vi_num2words(int(m.group('id'))), text)

def normalize_text(text):
   text = normalize("NFC", text)
   text = text.lower()
   text = text.replace(".", " ").replace("!", "").replace("?", "").replace(":", "").replace("\"", " ").replace("-", " ").replace(",", " ")
   text = " ".join(text.split())
   text = replace_time(text)
   text = replace_number(text)
   if len(text)==0:
       print("err")
   return text

import pandas as pd

data = pd.read_csv('meta_data.tsv', sep='\t', header=None)
# Suffle
data = data.sample(frac=1)
train_ratio = 0.8
train_index = int(train_ratio * len(data))
with open('training.txt', 'w') as fd:
    for i, fname in enumerate(data[0][:train_index]):
        text = normalize_text(data[1][i])
        fd.write('{}|{}\n'.format(os.path.join("/root/src/data/speech_data", fname), text))

with open('testing.txt', 'w') as fd:
    for i, fname in enumerate(data[0][train_index:]):
        text = normalize_text(data[1][i])
        fd.write('{}|{}\n'.format(os.path.join("/root/src/data/speech_data", fname), text))