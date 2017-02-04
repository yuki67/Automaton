from Automata import DeterministicFiniteAutomata as DFA
from Automata import NondeterministicFiniteAutomata as NFA


def is_length_even():
    """ 長さが偶数の文字列を認識 """
    print("is_length_even".center(50, "-"))
    a, b = range(2)
    states = [a, b]
    alphabets = "01"
    transitions = {
        a: {"0": b, "1": b},
        b: {"0": a, "1": a},
    }

    init_state = a
    final_states = {a}
    automata = DFA(states, alphabets, transitions, init_state, final_states)

    tests = ["0111", "1", "", "0011011"]

    for test in tests:
        if automata.run(test):
            print("accept : \"%s\"" % test)
        else:
            print("reject : \"%s\"" % test)


def is_divisible_by_3():
    """ 二進表記で3の倍数の文字列を認識 """
    print("is_divisible_by_3".center(50, "-"))
    a, b, c = range(3)
    states = [a, b, c]
    alphabets = "01"
    transitions = {
        a: {"0": a, "1": b},
        b: {"0": c, "1": a},
        c: {"0": b, "1": c},
    }

    init_state = a
    final_states = {a}
    automata = DFA(states, alphabets, transitions, init_state, final_states)

    # 0, 3, 14, 9, 942
    tests = ["00000", "0011", "01110", "1001", "1110101110"]
    for test in tests:
        if automata.run(test):
            print("accept : \"%s\"" % test)
        else:
            print("reject : \"%s\"" % test)


def is_end_0XXX():
    """ 最後から四文字目が0である文字列を認識 """
    print("is_end_0XXX".center(50, "-"))
    a, b, c, d, e = range(5)
    states = [a, b, c, d, e]
    alphabets = "01"
    transitions = {
        a: {"0": {a, b}, "1": {a}},
        b: {"0": {c}, "1": {c}},
        c: {"0": {d}, "1": {d}},
        d: {"0": {e}, "1": {e}},
        e: {},
    }
    init_state = a
    final_states = {e}
    automata = NFA(states, alphabets, transitions, init_state, final_states)

    tests = ["00000000", "000110", "1110", "01", "1110100110"]
    for test in tests:
        if automata.run(test):
            print("accept : \"%s\"" % test)
        else:
            print("reject : \"%s\"" % test)


def has_010():
    """ 010を部分列に持つ文字列を認識 """
    print("has_010".center(50, "-"))
    a, b, c, d = range(4)
    states = [a, b, c, d]
    alphabets = "01"
    transitions = {
        a: {"0": {a, b}, "1": {a}},
        b: {"1": {c}},
        c: {"0": {d}},
        d: {"0": {d}, "1": {d}},
    }
    init_state = a
    final_states = {d}
    automata = NFA(states, alphabets, transitions, init_state, final_states)

    tests = ["010", "000110", "111111001010", "111101", "1110100110"]
    for test in tests:
        if automata.run(test):
            print("accept : \"%s\"" % test)
        else:
            print("reject : \"%s\"" % test)

is_length_even()
is_divisible_by_3()
is_end_0XXX()
has_010()
print("program ended.")
