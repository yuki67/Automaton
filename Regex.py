from Automata import NFAWithEpsilonTransition as eNFA


def is_any(string):
    """ stringが任意の一文字を表す記号"."ならTrue """
    return string == "."


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
    >>> concat_split("(abc)*(a+b+c)(cba)*abc")
    ['(abc)*', '(a+b+c)', '(cba)*', 'a', 'b', 'c']
    >>> concat_split("...")
    ['.', '.', '.']
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


def union_split(string):
    """
    和の正規表現stringを分割して返す
    >>> union_split("(a+b+c)")
    ['a', 'b', 'c']
    >>> union_split("(a+ab+(b)*)")
    ['a', 'ab', '(b)*']
    """
    return string[1:-1].split("+")


def single_regex_to_eNFA(string, alphabet):
    """ 一項からなる正規表現stringを認識するeNFAを返す """
    if is_any(string):
        return eNFA.any_word(alphabet)
    if is_atom(string):
        return eNFA.one_word(string, alphabet)
    elif is_repeat(string):
        return eNFA.repeat(regex_to_eNFA(string[:-1], alphabet))
    elif is_union(string):
        return eNFA.parallel_connect([regex_to_eNFA(sub_regex, alphabet) for sub_regex in union_split(string)])
    else:
        assert False, "invalid regular expression: %s" % string


def regex_to_eNFA(string, alphabet):
    """ 正規表現stringを認識するeNFAを返す """
    return eNFA.serial_connect([single_regex_to_eNFA(single_regex, alphabet) for single_regex in concat_split(string)])

if __name__ == "__main__":
    import doctest
    import RegexTest
    doctest.testmod()
    RegexTest.run()
