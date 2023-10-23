function trie_from_list(words) {
    // do you even trie bruh?
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
    // words is a list of valid words
    // letters is a list of strings
    //     (they don't have to be length one)
    //     (the letter . is treated as a wildcard)

    const stack = [];
    const result = [];
    const trie = trie_from_list(words);
    const initialNode = {
        node: trie,
        chosen: "",
        remaining: bag_from_list(letters)
    };

    stack.push(initialNode);

    while (stack.length > 0) {
        const { node, chosen, remaining } = stack.pop();

        if (chosen) {
            // we have chosen some letters. Traverse the trie
            if (chosen[0] === ".") {
                for (const child of node.children.values()) {
                    stack.push({
                        node: child,
                        chosen: chosen.slice(1),
                        remaining
                    });
                }
            } else if (node.children.has(chosen[0])) {
                stack.push({
                    node: node.children.get(chosen[0]),
                    chosen: chosen.slice(1),
                    remaining
                });
            }
            continue;
        }

        if (node.word !== null) {
            result.push(node.word);
        }

        if (remaining.size !== 0) {
            // there are still remaining letters, choose one
            for (const letters of remaining.keys()) {
                stack.push({
                    node: node,
                    chosen: letters,
                    remaining: remove_bag(remaining, letters)
                });
            }
        }
    }

    result.reverse();
    return result;
}
