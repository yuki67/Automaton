
class Automata(object):
    """ オートマトンの基底クラス """

    def __init__(self, states, alphabet, transitions, init_state, final_states):
        self.states = frozenset(states)
        self.alphabet = frozenset(alphabet)
        self.transitions = transitions
        self.init_state = init_state
        self.final_states = frozenset(final_states)

    def __eq__(self, other):
        return self.states == other.states and \
            self.alphabet == other.alphabet and \
            self.transitions == other.transitions and \
            self.init_state == other.init_state and \
            self.final_states == other.final_states

    def __repr__(self):
        str_trans = ""
        for key, val in self.transitions.items():
            str_trans += str(key).replace("\n", "") + " : " + str(val).replace("\n", "") + "\n                  "
        str_trans = str_trans[:-19]

        ans = """Automata
    states      : %s
    alphabet   : %s
    transitions : %s
    init_state  : %s
    final_states: %s""" % (str(self.states).replace("\n", ""),
                           str(self.alphabet).replace("\n", ""),
                           str_trans,
                           str(self.init_state).replace("\n", ""),
                           str(self.final_states).replace("\n", ""))
        ans = ans.replace("frozenset()", "frozenset({})")
        ans = ans.replace("frozenset({", "{")
        ans = ans.replace("})", "}")
        return ans


class DeterministicFiniteAutomata(Automata):
    """ 決定性有限オートマトン """

    def run(self, string):
        """ stringを認識するかチェックする """
        state = self.init_state
        for char in string:
            if char not in self.alphabet:
                print("ERROR : invalid character \"%s\"" % char)
                return False
            else:
                state = self.transitions[state][char]
        return state in self.final_states

    def flliped(self):
        """ 受理する言語がひっくり返ったDFAを返す """
        final_states = set([x for x in self.states if x not in self.final_states])
        return DeterministicFiniteAutomata(self.states, self.alphabet, self.transitions, self.init_state, final_states)

    def minimized(self):
        """ 最小化されたDFAを返す """

        # markedとunmarkedを初期化
        # markedは区別できるペアの集合
        # unmarkedは区別できないペアの集合
        marked = set()
        unmarked = set()
        checked = set()
        for p in self.states:
            for q in self.states:
                if frozenset({p, q}) in checked or p == q:
                    continue
                if (p in self.final_states and q not in self.final_states) or \
                        (q in self.final_states and p not in self.final_states):
                    marked.add(frozenset({p, q}))
                else:
                    unmarked.add(frozenset({p, q}))
                checked.add(frozenset({p, q}))
                checked.add(frozenset({q, p}))

        # markedを限界まで増やす
        flag = True
        while flag:
            flag = False
            for p, q in unmarked:
                for s in self.alphabet:
                    # (p,q)をsで遷移させてmarkedにはいるなら(p,q)もmarkedに入る
                    if frozenset({self.transitions[p][s], self.transitions[q][s]}) in marked:
                        flag = True
                        marked.add(frozenset({p, q}))
                        unmarked.remove(frozenset({p, q}))
                        break
                if flag:
                    break

        # まず最小DFAの状態がどうなるか計算する
        states_dict = {}
        for p in self.states:
            states_dict[p] = {p}
        for p in self.states:
            for q in self.states:
                if frozenset({p, q}) in unmarked:
                    states_dict[p].add(q)
                    states_dict[q].add(p)

        # 次にstates_dictからtransitions, init_state, final_statesを作る
        states = set()
        init_state = None
        final_states = set()
        transitions = {}
        for p in self.states:
            state = frozenset(states_dict[p])
            if state in states:
                continue
            states.add(state)
            transitions[state] = {}
            for s in self.alphabet:
                # next(iter(X))は「Xから適当に一つ取る」という意味
                transitions[state][s] = states_dict[self.transitions[next(iter(state))][s]]
            if self.init_state in state:
                init_state = state
            if len(self.final_states.intersection(state)) != 0:
                final_states.add(state)
        alphabet = self.alphabet
        return DeterministicFiniteAutomata(states, alphabet, transitions, init_state, final_states)


class NondeterministicFiniteAutomata(Automata):
    """ 非決定性有限オートマトン """

    def run(self, string):
        """ stringを認識するかチェックする """
        states = {self.init_state}
        for char in string:
            if char not in self.alphabet:
                print("ERROR : invalid character \"%s\"" % char)
                return False
            else:
                states = self.next_states(states, char)
        return len(states.intersection(self.final_states)) != 0

    def next_states(self, states, char):
        """ statesからcharを読んだ時の次の状態集合を返す """
        next_states = set()
        for state in states:
            next_states = next_states.union(self.transitions[state].get(char, frozenset()))
        return frozenset(next_states)

    def convert_to_DFA(self):
        """ 等価なDFAに変換する """
        # 状態と遷移関数を作る
        states = {frozenset({self.init_state})}
        transitions = {}
        to_search = {frozenset({self.init_state})}
        searched = set()
        while len(to_search) != 0:
            searching = to_search.pop()
            searched.add(searching)
            for char in self.alphabet:
                reachables = self.next_states(searching, char)
                states.add(reachables)
                if reachables not in searched:
                    # 遷移させた先がまだ調べていない状態だったらさらに調べる必要がある
                    to_search.add(reachables)
                if not transitions.get(searching):
                    # 二重辞書の要素を一気に作ることはできないので注意
                    transitions[searching] = {}
                transitions[searching][char] = frozenset(reachables)

        # DFAの終了状態は終了状態を一つでも含む状態全体からなる集合
        final_states = set([x for x in states if len(self.final_states.intersection(x)) != 0])
        # DFAの始状態はNFAの始状態だけからなる集合
        init_state = frozenset({self.init_state})
        # DFAのアルファベットはNFAと同じ
        alphabet = self.alphabet
        return DeterministicFiniteAutomata(states, alphabet, transitions, init_state, final_states)


class NFAWithEpsilonTransition(Automata):
    """ ε動作付き非決定性有限オートマトン """

    def reachables_with_a_epsilon_from(self, state):
        """ stateから一回のε遷移だけで到達可能な状態の集合を返す """
        return frozenset(self.transitions[state].get(-1, {}))

    def reachables_with_epsilons_from(self, state):
        """ stateからε遷移だけで到達可能な状態の集合を返す """
        ans = frozenset([state])
        reachables = self.reachables_with_a_epsilon_from(state)
        while not reachables.issubset(ans):
            ans = ans.union(reachables)
            new_reachables = frozenset()
            for reachable in reachables:
                new_reachables = new_reachables.union(self.reachables_with_a_epsilon_from(reachable))
            reachables = new_reachables
        return ans

    def next_states(self, states, char):
        """ statesからcharを読んだ時の次の状態集合を返す """
        next_states = frozenset()
        for state in states:
            for reachable in self.transitions[state].get(char, frozenset()):
                next_states = next_states.union(self.reachables_with_epsilons_from(reachable))
        return frozenset(next_states)

    def run(self, string):
        """ stringを認識するかチェックする """
        states = self.reachables_with_epsilons_from(self.init_state)
        for char in string:
            if char not in self.alphabet:
                print("ERROR : invalid character \"%s\"" % char)
                return False
            else:
                states = self.next_states(states, char)
        return len(states.intersection(self.final_states)) != 0

    def convert_to_DFA(self):
        """ 等価なDFAに変換する """
        # 状態と遷移関数を作る
        states = {self.reachables_with_epsilons_from(self.init_state)}
        transitions = {}
        to_search = {self.reachables_with_epsilons_from(self.init_state)}
        searched = set()
        while len(to_search) != 0:
            searching = to_search.pop()
            searched.add(searching)
            for char in self.alphabet:
                reachables = self.next_states(searching, char)
                states.add(reachables)
                if reachables not in searched:
                    # 遷移させた先がまだ調べていない状態だったらさらに調べる必要がある
                    to_search.add(reachables)
                if not transitions.get(searching):
                    # 二重辞書の要素を一気に作ることはできないので注意
                    transitions[searching] = {}
                transitions[searching][char] = frozenset(reachables)

        # DFAの終了状態は終了状態を一つでも含む状態全体からなる集合
        final_states = set([x for x in states if len(self.final_states.intersection(x)) != 0])
        # DFAの始状態はNFAの始状態からイプシロン遷移で到達できる状態の集合
        init_state = self.reachables_with_epsilons_from(self.init_state)
        # DFAのアルファベットはNFAと同じ
        alphabet = self.alphabet
        return DeterministicFiniteAutomata(states, alphabet, transitions, init_state, final_states)

    @staticmethod
    def serial_connect(automaton):
        """ 複数のオートマトンを横並びに一つにまとめる """
        alphabet = set()
        states = set()
        transitions = {}
        for i, automata in enumerate(automaton):
            # alphabetを更新
            alphabet = alphabet.union(automata.alphabet)

            # statesを更新
            # 状態とautomataのインデックスを組にすることで唯一性を確保
            states = states.union(set([(i, state) for state in automata.states]))

            # automata内部の遷移をtransitionsに追加
            for final_state in automata.final_states:
                transitions[(i, final_state)] = {}
            for state, trans_dict in automata.transitions.items():
                transitions[(i, state)] = {}
                for char, states_transit_to in trans_dict.items():
                    transitions[(i, state)][char] = frozenset([(i, state) for state in states_transit_to])

            # 一つ前のautomataからのイプシロン遷移を追加
            if i == 0:
                continue
            for pre_final_state in automaton[i - 1].final_states:
                transitions[(i - 1, pre_final_state)][-1] = frozenset([(i, automata.init_state)])

        # 始状態と終状態を作る
        init_state = (0, automaton[0].init_state)
        final_states = set([(len(automaton) - 1, f) for f in automaton[-1].final_states])
        return NFAWithEpsilonTransition(states, alphabet, transitions, init_state, final_states)

    @staticmethod
    def parallel_connect(automaton):
        """ 複数のオートマトンを並列につなげる """
        # 新しい始状態は定数1
        init_state = 1
        alphabet = set()
        states = {init_state}
        transitions = {}
        final_states = set()
        for i, automata in enumerate(automaton):
            # alphabetを更新
            alphabet = alphabet.union(automata.alphabet)

            # statesを更新
            # 状態とautomataのインデックスを組にすることで唯一性を確保
            states = states.union(set([(i, state) for state in automata.states]))

            # automata内部の遷移をtransitionsに追加
            for state, trans_dict in automata.transitions.items():
                transitions[(i, state)] = {}
                for char, states_transit_to in trans_dict.items():
                    transitions[(i, state)][char] = frozenset([(i, state) for state in states_transit_to])

            # 終了状態にautomata.finalstatesを追加
            final_states = final_states.union(set([(i, final_state) for final_state in automata.final_states]))

        # 最初のイプシロン遷移を追加
        transitions[init_state] = {}
        transitions[init_state][-1] = frozenset([(i, automata.init_state) for i, automata in enumerate(automaton)])

        return NFAWithEpsilonTransition(states, alphabet, transitions, init_state, final_states)

    @staticmethod
    def repeat(automata):
        """ automataが受理する文字列をn回並べた文字列をすべて受理するeNFAを返す(n=0,1,2...) """
        # init_stateとfinal_stateをautomataのstatesとかぶらないように決める
        i = 1
        while i in automata.states:
            i += 1
        init_state = i

        j = -1
        while j in automata.states:
            j -= 1
        final_state = j

        # 状態は元の状態に始状態と終状態を追加したもの
        states = automata.states.union({init_state, final_state})

        # 遷移を追加する
        transitions = automata.transitions
        transitions[init_state] = {}
        transitions[init_state][-1] = {automata.init_state, final_state}
        transitions[final_state] = {}
        for final in automata.final_states:
            transitions[final][-1] = {automata.init_state, final_state}

        return NFAWithEpsilonTransition(states, automata.alphabet, transitions, init_state, {final_state})

    @staticmethod
    def one_word(char, alphabet):
        """ char一文字だけ認識するeNFAを返す """
        states = {0, 1}
        alphabet = alphabet
        transitions = {
            0: {char: {1}},
            1: {}
        }
        init_state = 0
        final_states = {1}
        return NFAWithEpsilonTransition(states, alphabet, transitions, init_state, final_states)

    @staticmethod
    def any_word(alphabet):
        """ 任意の文字一文字を認識するeNFAを返す """
        states = {0, 1, 2}
        alphabet = alphabet
        transitions = {0: {}, 1: {}, 2: {}}
        for char in alphabet:
            transitions[0][char] = {1}
            transitions[1][char] = {2}
            transitions[2][char] = {2}
        init_state = 0
        final_states = {1}
        return NFAWithEpsilonTransition(states, alphabet, transitions, init_state, final_states)
