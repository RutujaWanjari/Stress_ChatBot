import nltk
from nltk.corpus import sentiwordnet as swn
nltk.download('sentiwordnet')

try:
    print("Please wait for 5 mins till I process your query.")
    list(swn.senti_synsets('slow'))
    happy = swn.senti_synsets('happy', 'a')
    happy0 = list(happy)[0]
    print(happy0.pos_score())
    print(happy0.neg_score())
    print(happy0.obj_score())
except Exception as e:
    print(str(e))