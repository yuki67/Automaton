import tkinter
from math import cos, sin, pi, atan
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
    """ オートマトンを描画する """

    def __init__(self, automata, width=512, height=512):
        self.width = width
        self.height = height
        self.automata = automata
        n = len(automata.states)
        self.states_positions = [(self.width / 2.3 * cos(2 * pi * i / n) + self.width / 2,
                                  self.height / 2.3 * sin(2 * pi * i / n) + self.height / 2) for i in range(n)]
        self.tk_root = self.setup_tk()
        self.tk_canvas = self.setup_canvas()

        self.place_arrow()
        self.place_circle()
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
        for x, y in self.states_positions:
            self.tk_canvas.create_oval(x - rad, y - rad,
                                       x + rad, y + rad,
                                       fill="red")

    def place_arrow(self):
        for a, b in self.states_positions:
            for c, d in self.states_positions:
                if a == c and b == d:
                    continue
                else:
                    self.draw_arc(a, b, c, d)

    def draw_arc(self, a, b, c, d):
        distance = 2
        center = [(a + c) / 2 + distance * (d - b), (b + d) / 2 - distance * (c - a)]
        r = ((a - center[0])**2 + (b - center[1])**2)**0.5

        theta = (atan((center[1] - b) / (center[0] - a)) * 180 / pi) % 360
        phi = (atan((center[1] - d) / (center[0] - c)) * 180 / pi) % 360
        if a < center[0]:
            theta = (180 + theta) % 360
        if c < center[0]:
            phi = (180 + phi) % 360

        extent = abs(phi - theta) if abs(phi - theta) < 180 else 360 - (phi - theta)
        start = min(phi, theta) if abs(phi - theta) < 180 else max(phi, theta)
        self.tk_canvas.create_arc(center[0] - r, center[1] - r,
                                  center[0] + r, center[1] + r,
                                  style=tkinter.ARC,
                                  start=-start - extent,
                                  extent=extent)


if __name__ == "__main__":
    AutomataPainter(IsDivisibleBy3())
