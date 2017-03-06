import unittest
from Automata import DeterministicFiniteAutomata as DFA
from Automata import NondeterministicFiniteAutomata as NFA
from Automata import NFAWithEpsilonTransition as eNFA


class IsLengthEven(DFA):
    """ 長さが偶数の文字列を認識 """
    tests = (("0111", True),
             ("1", False),
             ("", True),
             ("0011011", False))

    def __init__(self):
        a, b = range(2)
        states = {a, b}
        alphabet = {"0", "1"}
        transitions = {
            a: {"0": b, "1": b},
            b: {"0": a, "1": a},
        }
        init_state = a
        final_states = {a}
        super().__init__(states, alphabet, transitions, init_state, final_states)


class IsDivisibleBy3(DFA):
    """ 二進表記で3の倍数の文字列を認識 """
    tests = (("00000", True),       # 0
             ("0011", True),        # 3
             ("01110", False),      # 14
             ("1001", True),        # 9
             ("1110101110", True))  # 942

    def __init__(self):
        a, b, c = range(3)
        states = {a, b, c}
        alphabet = {"0", "1"}
        transitions = {
            a: {"0": a, "1": b},
            b: {"0": c, "1": a},
            c: {"0": b, "1": c},
        }

        init_state = a
        final_states = {a}
        super().__init__(states, alphabet, transitions, init_state, final_states)


class IsEnd0XXX(NFA):
    """ 最後から四文字目が0である文字列を認識 """
    tests = (("00000000", True),
             ("000110", True),
             ("1110", False),
             ("01", False),
             ("1110100110", True))

    def __init__(self):
        a, b, c, d, e = range(5)
        states = {a, b, c, d, e}
        alphabet = {"0", "1"}
        transitions = {
            a: {"0": {a, b}, "1": {a}},
            b: {"0": {c}, "1": {c}},
            c: {"0": {d}, "1": {d}},
            d: {"0": {e}, "1": {e}},
            e: {},
        }
        init_state = a
        final_states = {e}
        super().__init__(states, alphabet, transitions, init_state, final_states)


class Has010(NFA):
    """ 010を部分列に持つ文字列を認識 """
    tests = (("010", True),
             ("000110", False),
             ("111111001010", True),
             ("111101", False),
             ("1110100110", True))

    def __init__(self):
        a, b, c, d = range(4)
        states = {a, b, c, d}
        alphabet = {"0", "1"}
        transitions = {
            a: {"0": {a, b}, "1": {a}},
            b: {"1": {c}},
            c: {"0": {d}},
            d: {"0": {d}, "1": {d}},
        }
        init_state = a
        final_states = {d}
        super().__init__(states, alphabet, transitions, init_state, final_states)


class IsIncreasingSequence(eNFA):
    """ 広義単調増加な文字列を認識 """
    tests = (("01234", True),
             ("01122334444", True),
             ("01234231", False),
             ("1111", True),
             ("1133344", True))

    def __init__(self):
        a, b, c, d, e = range(5)
        states = {a, b, c, d, e}
        alphabet = {"0", "1", "2", "3", "4"}
        transitions = {
            a: {"0": {a}, -1: {b}},
            b: {"1": {b}, -1: {c}},
            c: {"2": {c}, -1: {d}},
            d: {"3": {d}, -1: {e}},
            e: {"4": {e}}
        }
        init_state = a
        final_states = {e}
        super().__init__(states, alphabet, transitions, init_state, final_states)


class IsEnd0XXX_DFA(DFA):
    """ 最後から四文字目が0である文字列を認識 """
    tests = (("00000000", True),
             ("000110", True),
             ("1110", False),
             ("01", False),
             ("1110100110", True))

    def __init__(self):
        a, b, c, d, e = range(5)
        states = {a, b, c, d, e}
        alphabet = {"0", "1"}
        transitions = {
            a: {"0": {a, b}, "1": {a}},
            b: {"0": {c}, "1": {c}},
            c: {"0": {d}, "1": {d}},
            d: {"0": {e}, "1": {e}},
            e: {},
        }
        init_state = a
        final_states = {e}
        temp = NFA(states, alphabet, transitions, init_state, final_states).convert_to_DFA()
        super().__init__(temp.states, temp.alphabet, temp.transitions, temp.init_state, temp.final_states)


class Has010_DFA(DFA):
    """ 010を部分列に持つ文字列を認識 """
    tests = (("010", True),
             ("000110", False),
             ("111111001010", True),
             ("111101", False),
             ("1110100110", True))

    def __init__(self):
        a, b, c, d = range(4)
        states = {a, b, c, d}
        alphabet = {"0", "1"}
        transitions = {
            a: {"0": {a, b}, "1": {a}},
            b: {"1": {c}},
            c: {"0": {d}},
            d: {"0": {d}, "1": {d}},
        }
        init_state = a
        final_states = {d}
        temp = NFA(states, alphabet, transitions, init_state, final_states).convert_to_DFA()
        super().__init__(temp.states, temp.alphabet, temp.transitions, temp.init_state, temp.final_states)


class IsIncreasingSequence_DFA(DFA):
    """ 広義単調増加な文字列を認識 """
    tests = (("01234", True),
             ("01122334444", True),
             ("01234231", False),
             ("1111", True),
             ("1133344", True))

    def __init__(self):
        a, b, c, d, e = range(5)
        states = {a, b, c, d, e}
        alphabet = {"0", "1", "2", "3", "4"}
        transitions = {
            a: {"0": {a}, -1: {b}},
            b: {"1": {b}, -1: {c}},
            c: {"2": {c}, -1: {d}},
            d: {"3": {d}, -1: {e}},
            e: {"4": {e}}
        }
        init_state = a
        final_states = {e}
        temp = eNFA(states, alphabet, transitions, init_state, final_states).convert_to_DFA()
        super().__init__(temp.states, temp.alphabet, temp.transitions, temp.init_state, temp.final_states)


class MinimizeTest(DFA):
    """ DFAの最小化のテスト """
    tests = {}

    def __init__(self):
        a, b, c, d, e, f, g, h, = range(8)
        states = {a, b, c, d, e, f, g, h}
        alphabet = {"0", "1"}
        transitions = {
            a: {"0": b, "1": f},
            b: {"0": g, "1": c},
            c: {"0": a, "1": c},
            d: {"0": c, "1": g},
            e: {"0": h, "1": f},
            f: {"0": c, "1": g},
            g: {"0": g, "1": e},
            h: {"0": g, "1": c}
        }
        init_state = a
        final_states = {c}
        temp = DFA(states, alphabet, transitions, init_state, final_states)
        print(temp)
        temp = temp.minimized()
        super().__init__(temp.states, temp.alphabet, temp.transitions, temp.init_state, temp.final_states)


class IsNotDivisibleBy3(DFA):
    """ 二進表記で3の倍数でない文字列を認識 """
    tests = (("00000", not True),       # 0
             ("0011", not True),        # 3
             ("01110", not False),      # 14
             ("1001", not True),        # 9
             ("1110101110", not True))  # 942

    def __init__(self):
        a, b, c = range(3)
        states = {a, b, c}
        alphabet = {"0", "1"}
        transitions = {
            a: {"0": a, "1": b},
            b: {"0": c, "1": a},
            c: {"0": b, "1": c},
        }

        init_state = a
        final_states = {a}
        temp = DFA(states, alphabet, transitions, init_state, final_states).flliped()
        super().__init__(temp.states, temp.alphabet, temp.transitions, temp.init_state, temp.final_states)


class IsDoubleIncreasingSequence(eNFA):

    tests = (("0013", True),
             ("10311", False),
             ("0130112", True),
             ("13230001", False),
             ("22223344012344", True))

    def __init__(self):
        inc = IsIncreasingSequence()
        temp = eNFA.serial_connect([inc, inc])
        super().__init__(temp.states, temp.alphabet, temp.transitions, temp.init_state, temp.final_states)


class Has010OrEnd0XXX(eNFA):

    tests = (("0010", True),
             ("00111", True),
             ("011111", False),
             ("00010001111", True),
             ("0001111001111", False))

    def __init__(self):
        zero10 = Has010()
        zeroxxx = IsEnd0XXX()
        temp = eNFA.parallel_connect([zero10, zeroxxx])
        super().__init__(temp.states, temp.alphabet, temp.transitions, temp.init_state, temp.final_states)


class AutomatonTest(unittest.TestCase):
    """ オートマトンの動作確認 """
    automaton = [
        IsLengthEven,
        IsDivisibleBy3,
        IsEnd0XXX,
        Has010,
        IsIncreasingSequence,
        Has010_DFA,
        IsEnd0XXX_DFA,
        IsIncreasingSequence_DFA,
        MinimizeTest,
        IsNotDivisibleBy3,
        IsDoubleIncreasingSequence,
        Has010OrEnd0XXX,
    ]

    def test_automaton(self):
        """ テスト本体 """
        for automata in self.automaton:
            print(str(automata)[17:-2].center(70, "-"))
            instance = automata()
            print(instance)
            for string, expected in instance.tests:
                result = instance.run(string)
                print("%s: \"%s\"" % (str(result).ljust(5), string))
                self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
