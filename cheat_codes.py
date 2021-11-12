#!/usr/bin/env python3

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Trie:
   word: Optional[str]
   children: Dict[str, "Trie"]


def trie_from_list(words: List[str]) -> Trie:
   out = Trie(None, dict())
   for word in words:
      current = out
      for letter in word:
         if letter not in current.children:
            current.children[letter] = Trie(None, dict())
         current = current.children[letter]
      current.word = word
   return out


def remove_bag(bag: Dict[str, int], e: str) -> Dict[str, int]:
   if e not in bag:
      raise ValueError(f"Cannot remove {e} from {bag}")
   out = bag.copy()
   if out[e] == 1:
      out.pop(e)
   else:
      out[e] -= 1
   return out


def find_trie(words: List[str], letters: List[str]) -> List[str]:

   def rec(trie: Trie, chosen: str, remaining: Dict[str, int]) -> List[str]:
      if chosen:
         if chosen[0] == ".":
            return [word for child in trie.children.values() for word in rec(child, chosen[1:], remaining)]
         elif chosen[0] in trie.children:
            return rec(trie.children[chosen[0]], chosen[1:], remaining)
         else:
            return []

      if not remaining:
         return [trie.word] if trie.word is not None else []

      out = []
      if trie.word is not None:
         out.append(trie.word)
      for letters in remaining:
         out.extend(rec(trie, letters, remove_bag(remaining, letters)))
      return out

   trie = trie_from_list(words)
   return rec(trie, "", dict(Counter(letters)))


def parse_args() -> argparse.Namespace:
   p = argparse.ArgumentParser("Word Finder")

   p.add_argument("--word-list", default="words.txt", metavar="PATH")

   p.add_argument("letters", nargs="+", type=str, metavar="L")

   return p.parse_args()


def main() -> None:
   args = parse_args()

   with open(args.word_list, "r") as handle:
      words = [w.strip() for w in handle.readlines() if w.strip()]

   results = set(find_trie(words, args.letters))
   for word in sorted(results, key=len):
      print(word)


if __name__ == "__main__":
   main()
