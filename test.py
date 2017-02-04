from Automata import DeterministicFiniteAutomata as DFA


def is_length_even():
    """ 長さが偶数の文字列を認識 """
    print("is_length_even".center(50, "-"))
    a = hash("a")
    b = hash("b")
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
            print("length even : \"%s\"" % test)
        else:
            print("length odd  : \"%s\"" % test)


def is_mod_three():
    """ 二進表記で3の倍数の文字列を認識 """
    print("is_mod_three".center(50, "-"))
    a = hash("a")
    b = hash("b")
    c = hash("c")
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
            print("mod 3 in binary     : \"%s\"" % test)
        else:
            print("not mod 3 in binary : \"%s\"" % test)


is_length_even()
is_mod_three()
print("program ended.")
