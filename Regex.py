from Automata import NFAWithEpsilonTransition as eNFA


def is_atom(string):
    """
    stringが通常の文字一つならTrue、それ以外はFalse
    >>> is_atom("a")
    True
    >>> is_atom("a*")
    False
    >>> is_atom("(ab)")
    False
    """
    return True if len(string) == 1 and string not in "()+*" else False


def is_repeat(string):
    """
    stringが"X*"ならTrue、それ以外はFalse

    >>> is_repeat("a*")
    True
    >>> is_repeat("(ab)*")
    True
    >>> is_repeat("abc")
    False
    """
    return len(string) > 1 and string[-1] == "*"


def is_concat(string):
    """
    stringが複数の要素の連結ならTrue、一つの要素だけからなるならFalse

    >>> is_concat("a")
    False
    >>> is_concat("ab")
    True
    """
    return len(string) > 1


def is_union(string):
    """
    stringが文字の集合を表す正規表現ならTrue

    >>> is_union("(abcd)")
    True
    >>> is_union("(a(bc)d)")
    True
    >>> is_union("ab(cd)")
    False
    """
    return string[0] == "(" and string[-1] == ")"


def concat_split(string):
    """
    正規表現の連結stringを正規表現一つづつに切って返す

    >>> concat_split("ab")
    ['a', 'b']
    >>> concat_split("a*")
    ['a*']
    """
    ans = []
    index = 0
    while index < len(string):
        buf = string[index]
        index += 1
        if buf == "(":
            while string[index] != ")":
                buf += string[index]
                index += 1
            buf += ")"
            index += 1
        if index < len(string) and string[index] == "*":
            buf += "*"
            index += 1

        ans.append(buf)
    return ans


def regex_to_eNFA(string, alphabet):
    print("regex_to_eNFA :", string)
    if is_atom(string):
        return eNFA.one_word(string, alphabet)
    elif is_repeat(string):
        return eNFA.repeat(regex_to_eNFA(string[:-1], alphabet))
    elif is_union(string):
        return eNFA.parallel_connect([regex_to_eNFA(sub_regex, alphabet) for sub_regex in union_split(string)])
    if is_concat(string):
        return eNFA.serial_connect([regex_to_eNFA(sub_regex, alphabet) for sub_regex in concat_split(string)])
    else:
        assert False, "invalid regular expression: %s" % string


if __name__ == "__main__":
    import doctest
    import RegexTest
    doctest.testmod()
    RegexTest.run()
