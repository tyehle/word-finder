function trie_from_list(words) {
    let out = {word: null, children: new Map()};
    for (let word of words) {
        let current = out;
        for (let letter of word) {
            if (!current.children.has(letter)) {
                current.children.set(letter, {word: null, children: new Map()});
            }
            current = current.children.get(letter);
        }
        current.word = word;
    }
    return out;
}


function remove_bag(bag, elem) {
    if (!bag.has(elem)) {
        throw `Cannot remove ${elem} from ${JSON.stringify(bag)}`
    }
    let out = new Map(bag);
    if (out.get(elem) === 1) {
        out.delete(elem);
    } else {
        out.set(elem, out.get(elem) - 1);
    }
    return out;
}


function bag_from_list(elements) {
    let out = new Map();
    for (let elem of elements) {
        if (!out.has(elem)) {
            out.set(elem, 1);
        } else {
            out.set(elem, out.get(elem) + 1);
        }
    }
    return out;
}


function find_words(words, letters) {
    function rec(trie, chosen, remaining) {
        if (chosen) {
            if (chosen[0] === ".") {
                let result = [];
                for (let child of trie.children.values()) {
                    for (let word of rec(child, chosen.slice(1), remaining)) {
                        result.push(word);
                    }
                }
                return result;
            } else if (trie.children.has(chosen[0])) {
                return rec(trie.children.get(chosen[0]), chosen.slice(1), remaining);
            } else {
                return [];
            }
        }

        let out = [];

        if (trie.word !== null) {
            out.push(trie.word);
        }

        if(remaining.size !== 0) {
            for (let letters of remaining.keys()) {
                out.push(...rec(trie, letters, remove_bag(remaining, letters)));
            }
        }

        return out;
    }

    let trie = trie_from_list(words);
    return rec(trie, "", bag_from_list(letters));
}
