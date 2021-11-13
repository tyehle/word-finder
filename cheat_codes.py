#!/usr/bin/env python3

import argparse
import collections
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


@dataclass
class Trie:
    word: Optional[str]
    children: Dict[str, "Trie"]


def trie_from_list(words: Iterable[str]) -> Trie:
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
    """Return a copy of a bag with one element removed.

    Args:
        bag: The bag to copy
        e: The element to remove

    Raises:
        ValueError: If the element is not in the bag
    """
    if e not in bag:
        raise ValueError(f"Cannot remove {e} from {bag}")
    out = bag.copy()
    if out[e] == 1:
        out.pop(e)
    else:
        out[e] -= 1
    return out


def find_trie(words: Iterable[str], letters: Iterable[str]) -> List[str]:
    def rec(trie: Trie, chosen: str, remaining: Dict[str, int]) -> List[str]:
        """Recursively search for words in a trie.

        Args:
            trie: The trie to search
            chosen: Letters to traverse in the trie before expanding the search
                from the remaining set
            remaining: Bag of remaining letters to search over

        Returns:
            The list of all words that matched
        """
        if chosen:
            if chosen[0] == ".":
                return [
                    word
                    for child in trie.children.values()
                    for word in rec(child, chosen[1:], remaining)
                ]
            elif chosen[0] in trie.children:
                return rec(trie.children[chosen[0]], chosen[1:], remaining)
            else:
                return []

        out = []

        if trie.word is not None:
            out.append(trie.word)

        if remaining:
            for letters in remaining:
                out.extend(rec(trie, letters, remove_bag(remaining, letters)))

        return out

    trie = trie_from_list(words)
    return rec(trie, "", dict(collections.Counter(letters)))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()

    p.add_argument(
        "--word-list",
        default="words.txt",
        metavar="PATH",
        help="Alternative path to a word list.",
    )

    p.add_argument(
        "parts",
        nargs="*",
        type=str,
        metavar="S",
        help=(
            "Substrings to combine to form words. The period character (.) is "
            "treated as a wildcard."
        ),
    )

    return p.parse_args()


def main() -> None:
    args = parse_args()

    with open(args.word_list, "r") as handle:
        words = [w.strip().lower() for w in handle.readlines() if w.strip()]

    letters = map(str.lower, args.parts)
    results = set(find_trie(words, letters))
    for word in sorted(results, key=len):
        print(word)


if __name__ == "__main__":
    main()
