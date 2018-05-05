import nltk, json, re
from nltk.tokenize import TweetTokenizer
from collections import Counter

tokenizer = TweetTokenizer()


file = r'C:\Users\Austin\Desktop\Reddit 2015-05\Reddit 2015-05'
alpha = re.compile('^[A-Za-z]+$')
output = r'C:\Users\Austin\Desktop\reddit\data.txt'
output2 = r'C:\Users\Austin\Desktop\reddit\types.txt'

types = Counter()
pos_per_type = {}
tokens = 0

with open(file, 'r', encoding='utf8') as f:
    with open(output, 'w+', encoding='utf8') as out:
        for n,line in enumerate(f):
            try:
                data = json.loads(line, encoding='utf8')
                sent = tokenizer.tokenize(data['body'])
                tokens += len(sent)
                for i, tok in enumerate(sent):
                    if not alpha.match(tok):
                        continue
                    if i!=0 and sent[i-1] == tok:
                        continue
                    j=0
                    while i+j+1 < len(sent) and tok == sent[i+j+1]:
                        j+=1
                    if j > 0:
                        pos = nltk.pos_tag(sent[:i+1]+sent[i+j+1:])[i][-1]
                        tok = tok.lower()
                        types[tok] += 1
                        size = j+1
                        if not tok in pos_per_type:
                            pos_per_type[tok] = Counter()
                        pos_per_type[tok][pos]+=1

                        print(j,tok,pos)
                        out.write(str(n)+'\t'+' '.join(sent[i:i+j+1])+'\t'+pos+'\t'+' '.join(sent)+'\n')
            except json.decoder.JSONDecodeError:
                'error'
            except UnicodeEncodeError:
                'error 2'
with open(output2, 'w+', encoding='utf8') as out:
    for type,value in sorted(types.items(), key=lambda x: x[1], reverse=True):
        out.write(type+'\t'+str(value)+'\t'+str([(x,pos_per_type[type][x]) for x in pos_per_type[type]])+'\n')
print('Tokens: ',tokens)




