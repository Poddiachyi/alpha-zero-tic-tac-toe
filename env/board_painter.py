class BoardPainter:

    def __init__(self):
        self.x = "-"
        self.y = "|"
        self.z = "  "
        self.zz = ""

    def draw_with_numbers(self):
        print(self.z * 16, 0, self.zz, self.y, 1, self.zz, self.y, 2, self.zz, self.y, 3)
        print(self.z * 16, self.x * 17)
        print(self.z * 16, 4, self.zz, self.y, 5, self.zz, self.y, 6, self.zz, self.y, 7)
        print(self.z * 16, self.x * 17)
        print(self.z * 16, 8, self.zz, self.y, 9, self.zz, self.y, 10, self.y, 11)
        print(self.z * 16, self.x * 17)
        print(self.z * 16, 12, self.y, 13, self.y, 14, self.y, 15)
        print()

    def draw_state(self, state):
        print(self.z * 16, state[0], self.y, state[1], self.y, state[2], self.y, state[3])
        print(self.z * 16, self.x * 14)
        print(self.z * 16, state[4], self.y, state[5], self.y, state[6], self.y, state[7])
        print(self.z * 16, self.x * 14)
        print(self.z * 16, state[8], self.y, state[9], self.y, state[10], self.y, state[11])
        print(self.z * 16, self.x * 14)
        print(self.z * 16, state[12], self.y, state[13], self.y, state[14], self.y,state[15])
        print()
