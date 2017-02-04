class DeterministicFiniteAutomata(object):
    """ 決定性有限オートマトン """

    def __init__(self, states, alphabets, transitions, init_state, final_states):
        self.states = states
        self.alphabets = alphabets
        self.transitions = transitions
        self.init_state = init_state
        self.final_states = final_states

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


class NondeterministicFiniteAutomata(object):
    """ 非決定性有限オートマトン """

    def __init__(self, states, alphabets, transitions, init_state, final_states):
        self.states = states
        self.alphabets = alphabets
        self.transitions = transitions
        self.init_state = init_state
        self.final_states = final_states

    def run(self, string):
        """ stringを認識するかチェックする """
        states = {self.init_state}
        for char in string:
            if char not in self.alphabets:
                print("ERROR : invalid character \"%s\"" % char)
                return False
            else:
                new_states = set()
                for state in states:
                    new_states = new_states.union(self.transitions[state].get(char, set()))
                states = new_states
        return len(states.intersection(self.final_states)) != 0


class NFAWithEpsilonTransition(object):
    """ ε動作付き非決定性有限オートマトン """

    def __init__(self, states, alphabets, transitions, init_state, final_states):
        self.states = states
        self.alphabets = alphabets
        self.transitions = transitions
        self.init_state = init_state
        self.final_states = final_states

    def reachables_with_a_epsilon_from(self, state):
        """ stateから一回のε遷移だけで到達可能な状態の集合を返す """
        return self.transitions[state].get(-1, set())

    def reachables_with_epsilons_from(self, state):
        """ stateからε遷移だけで到達可能な状態の集合を返す """
        ans = set([state])
        reachables = self.reachables_with_a_epsilon_from(state)
        while not reachables.issubset(ans):
            ans = ans.union(reachables)
            new_reachables = set()
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
                new_states = set()
                for state in states:
                    for reachable in self.transitions[state].get(char, set()):
                        new_states = new_states.union(self.reachables_with_epsilons_from(reachable))
                states = new_states
        return len(states.intersection(self.final_states)) != 0
