from Automata import NFAWithEpsilonTransition as eNFA


def is_dot(string):
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
    return True if len(string) == 1 and string not in "()|*." else False


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


def remove_outer_branket(string):
    """
    一番外側のカッコが外せるなら外して、外せないならそのまま返す

    >>> remove_outer_branket("(abc)")
    'abc'
    >>> remove_outer_branket("(a|b)(c|d)")
    '(a|b)(c|d)'
    """
    if not (string[0] == "(" and string[-1] == ")"):
        return string

    blanket_count = 0
    for char in string[:-1]:
        if char == "(":
            blanket_count += 1
        elif char == ")":
            blanket_count -= 1
        if blanket_count == 0:
            return string
        if blanket_count == 1 and char == "|":
            return string
    return string[1:-1]


def concat_split(string):
    """
    正規表現の連結stringを正規表現一つづつに切って返す

    >>> concat_split("ab")
    ['a', 'b']
    >>> concat_split("a*")
    ['a*']
    >>> concat_split("(abc)*(a|b|c)(cba)*abc")
    ['(abc)*', '(a|b|c)', '(cba)*', 'a', 'b', 'c']
    >>> concat_split("...")
    ['.', '.', '.']
    >>> concat_split("((a|A)(b|B)(c|C))")
    ['(a|A)', '(b|B)', '(c|C)']
    >>> concat_split("((a|A)(b|B)(c|C))*")
    ['((a|A)(b|B)(c|C))*']
    """
    ans = []
    right = left = 0
    string = remove_outer_branket(string)
    while left < len(string):
        if string[left] == "(":
            blanket_count = 1
            while blanket_count > 0:
                left += 1
                if string[left] == "(":
                    blanket_count += 1
                elif string[left] == ")":
                    blanket_count -= 1
        if left + 1 < len(string) and string[left + 1] == "*":
            left += 1
        ans.append(string[right:left + 1])
        right, left = left + 1, left + 1
    return ans


def union_split(string):
    """
    和の正規表現stringを分割して返す
    >>> union_split("(a|b|c)")
    ['a', 'b', 'c']
    >>> union_split("(a|ab|(b)*)")
    ['a', 'ab', '(b)*']
    """
    return string[1:-1].split("|")


def single_regex_to_eNFA(string, alphabet):
    """ 一項からなる正規表現stringを認識するeNFAを返す """
    if is_dot(string):
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
