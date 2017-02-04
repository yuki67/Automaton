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
