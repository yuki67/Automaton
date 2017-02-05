from itertools import chain, combinations


class Automata(object):
    """ オートマトンの基底クラス """

    def __init__(self, states, alphabets, transitions, init_state, final_states):
        self.states = frozenset(states)
        self.alphabets = frozenset(alphabets)
        self.transitions = transitions
        self.init_state = init_state
        self.final_states = frozenset(final_states)


class DeterministicFiniteAutomata(Automata):
    """ 決定性有限オートマトン """

    def run(self, string):
        """ stringを認識するかチェックする """
        state = self.init_state
        for char in string:
            if char not in self.alphabets:
                print("ERROR : invalid character \"%s\"" % char)
                return False
            else:
                state = self.transitions[state][char]
        return state in self.final_states


class NondeterministicFiniteAutomata(Automata):
    """ 非決定性有限オートマトン """

    def run(self, string):
        """ stringを認識するかチェックする """
        states = {self.init_state}
        for char in string:
            if char not in self.alphabets:
                print("ERROR : invalid character \"%s\"" % char)
                return False
            else:
                new_states = frozenset()
                for state in states:
                    new_states = new_states.union(self.transitions[state].get(char, frozenset()))
                states = new_states
        return len(states.intersection(self.final_states)) != 0

    def convert_to_DFA(self):
        """ 等価なDFAに変換する """
        init_state = frozenset({self.init_state})
        states = {frozenset({self.init_state})}
        alphabets = self.alphabets
        transitions = {}
        final_states = set()

        to_search = {frozenset({self.init_state})}
        searched = set()
        while len(to_search) != 0:
            searching = to_search.pop()
            searched.add(searching)
            for char in self.alphabets:
                reachables = set()
                for state in searching:
                    reachables = reachables.union(self.transitions[state].get(char, set()))
                if len(reachables) != 0:
                    reachables = frozenset(reachables)
                    states.add(reachables)
                    if reachables not in searched:
                        to_search.add(reachables)
                    if len(self.final_states.intersection(reachables)) != 0:
                        final_states.add(reachables)
                    if not transitions.get(searching):
                        transitions[searching] = {}
                    transitions[searching][char] = frozenset(reachables)
        return DeterministicFiniteAutomata(states, alphabets, transitions, init_state, final_states)


class NFAWithEpsilonTransition(Automata):
    """ ε動作付き非決定性有限オートマトン """

    def reachables_with_a_epsilon_from(self, state):
        """ stateから一回のε遷移だけで到達可能な状態の集合を返す """
        return self.transitions[state].get(-1, frozenset())

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

    def run(self, string):
        """ stringを認識するかチェックする """
        states = self.reachables_with_epsilons_from(self.init_state)
        for char in string:
            if char not in self.alphabets:
                print("ERROR : invalid character \"%s\"" % char)
                return False
            else:
                new_states = frozenset()
                for state in states:
                    for reachable in self.transitions[state].get(char, frozenset()):
                        new_states = new_states.union(self.reachables_with_epsilons_from(reachable))
                states = new_states
        return len(states.intersection(self.final_states)) != 0
