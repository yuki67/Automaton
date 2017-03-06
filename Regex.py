from Automata import NFAWithEpsilonTransition as eNFA


def is_atom(string):
    """
    >>> is_atom("a")
    True
    >>> is_atom("*")
    False
    """
    return True if len(string) == 1 and string not in "()+*" else False


def is_repeat(string):
    return False


def is_concat(string):
    """
    >>> is_concat("a")
    False
    >>> is_concat("ab")
    True
    """
    return len(string) > 1


def is_union(string):
    return False


def concat_split(string):
    """
    >>> concat_split("ab")
    ['a', 'b']
    """
    return [x for x in string]


def regex_to_eNFA(string, alphabet):
    if is_concat(string):
        return eNFA.serial_connect([regex_to_eNFA(sub_regex, alphabet) for sub_regex in concat_split(string)])
    elif is_atom(string):
        return eNFA_one_word(string, alphabet)
    elif is_repeat(string):
        return Repeat(string)
    elif is_union(string):
        return eNFA.parallel_connect([regex_to_eNFA(sub_regex, alphabet) for sub_regex in union_split(string)])
    else:
        assert False, "invalid regular expression: %s" % string


def eNFA_one_word(char, alphabet):
    """ char一文字だけ認識するeNFAを返す """
    states = {0, 1}
    alphabet = alphabet
    transitions = {
        0: {char: {1}},
        1: {}
    }
    init_state = 0
    final_states = {1}
    return eNFA(states, alphabet, transitions, init_state, final_states)
