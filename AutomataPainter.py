import tkinter
from math import cos, sin, pi
from Automata import DeterministicFiniteAutomata as DFA


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
        alphabets = {"0", "1"}
        transitions = {
            a: {"0": a, "1": b},
            b: {"0": c, "1": a},
            c: {"0": b, "1": c},
        }

        init_state = a
        final_states = {a}
        super().__init__(states, alphabets, transitions, init_state, final_states)


class AutomataPainter():

    def __init__(self, automata, width=512, height=512):
        self.width = width
        self.height = height
        self.automata = automata
        n = len(automata.states)
        self.states_positions = [(self.width / 2.3 * cos(2 * pi * i / n) + self.width / 2,
                                  self.height / 2.3 * sin(2 * pi * i / n) + self.height / 2) for i in range(n)]
        self.tk_root = self.setup_tk()
        self.tk_canvas = self.setup_canvas()

        self.place_circle()
        self.place_arrow()
        self.tk_canvas.place(x=5, y=5)
        self.tk_root.mainloop()

    def setup_tk(self):
        root = tkinter.Tk()
        root.title("Automata Painter")
        root.geometry("%dx%d+%d+%d" % (self.width + 10, self.height + 10, 256, 0))
        return root

    def setup_canvas(self):
        return tkinter.Canvas(self.tk_root, width=self.width, height=self.height)

    def place_circle(self):
        rad = 15
        for pos in self.states_positions:
            self.tk_canvas.create_oval(pos[0] - rad, pos[1] - rad,
                                       pos[0] + rad, pos[1] + rad,
                                       fill="red")

    def place_arrow(self):
        for first in self.states_positions:
            for last in self.states_positions:
                self.tk_canvas.create_line(first[0], first[1], last[0], last[1], arrow=tkinter.LAST)


if __name__ == "__main__":
    AutomataPainter(IsDivisibleBy3())
