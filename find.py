import itertools
import re

def find(words, ps):
 out = []
 for p in ps:
  for w in words:
   m = re.match('^' + ''.join(p) + '$', w)
   if m:
    print(w)
    out.append(w)
 return out


words = [w.strip() for w in open("words.txt", "r").readlines()]
perms = set(itertools.permutations(['n', 'n', 'a', '.', '.', 'es', 'it']))

find(words, perms)

