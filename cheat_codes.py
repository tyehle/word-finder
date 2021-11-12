#!/usr/bin/env python3

import argparse
from functools import partial
import itertools
import multiprocessing
import re
from typing import List, Tuple


def find_word(words: List[str], letters: List[str]) -> Tuple[List[str], List[str]]:
   reg = re.compile(f"^{''.join(letters)}$")
   return (letters, [w for w in words if reg.match(w)])


def parse_args() -> argparse.Namespace:
   p = argparse.ArgumentParser("Word Finder")

   p.add_argument("--word-list", default="words.txt", metavar="PATH")

   p.add_argument("--allow-skip", action="store_true")

   p.add_argument("letters", nargs="+", type=str, metavar="L")

   return p.parse_args()


def main() -> None:
   args = parse_args()

   with open(args.word_list, "r") as handle:
      words = [w.strip() for w in handle.readlines() if w.strip()]

   if args.allow_skip:
      patterns: List[str] = []
      for n in range(len(args.letters) + 1, 0, -1):
         patterns.extend(set(itertools.permutations(args.letters, n)))
   else:
      patterns = list(set(itertools.permutations(args.letters)))

   with multiprocessing.Pool() as pool:
      for (pattern, matches) in pool.imap_unordered(partial(find_word, words), patterns, chunksize=42):
         for match in matches:
            prefix = f"{' '.join(pattern)} -> " if args.allow_skip else ""
            print(prefix + match)


if __name__ == "__main__":
   main()
