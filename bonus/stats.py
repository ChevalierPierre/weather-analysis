#!/bin/python3

from math import sqrt
import matplotlib.pyplot as plt

class Stats:
    def __init__(self, graphical = False):
        self.kept_values = []
        self.weird_values = []
        self.tmp = 0
        self.length = 0
        self.g_val = []
        self.r_val = []
        self.s_val = []
        self.nb_switches = 0
        self.switched = False
        self.period = 0
        self.graphical = graphical
        if graphical == True:
            self.data = []
            self.fig = plt.gcf()
            self.fig.show()
            self.fig.canvas.draw()

    def display(self):
        print("g=%.2f" % self.g_val[-1], end='\t\t')
        print("r=%.0f%%" % self.r_val[-1], end='\t\t')
        print("s=%.2f" % self.s_val[-1], end='')
        if self.switched == True:
            print("\t\ta switch occurs")
            self.switched = False
        else:
            print("")
        if self.graphical == True:
            self.data.append(self.kept_values[-1])
            plt.clf()
            if self.length <= self.period:
                plt.plot([i for i in range(0, self.length)], self.data, 'r--')
            else:
                plt.plot([i for i in range(0, self.length)], self.data, 'r--', [i for i in range(0, self.length)], self.s_val, 'bs', [i for i in range(0, self.length)], self.g_val, 'g^', [i for i in range(0, self.length)], self.r_val, ':')
            self.fig.canvas.draw()

    def setPeriod(self, period):
        if period <= 0:
            raise Exception()
        self.period = period

    def update_g(self):
        total = float(0)
        for i in range(self.period, 0, -1):
            tmp = (self.kept_values[self.length - i] - self.kept_values[self.length - i - 1])
            total += tmp
        total /= self.period
        if total < 0:
            total = 0
        self.g_val.append(total)

    def update_r(self):
        r = float('nan')
        if self.kept_values[-1 - self.period] != 0:
            r = 100 * (self.kept_values[-1] - self.kept_values[-1 - self.period]) / self.kept_values[-1 - self.period]
        self.r_val.append(r)
        if self.length > self.period + 1 and self.r_val[-1] != float('nan') and self.r_val[-2] != float('nan'):
            if (self.r_val[-1] < 0 and self.r_val[-2] > 0) or (self.r_val[-1] > 0 and self.r_val[-2] < 0):
                self.switched = True
                self.nb_switches += 1

    def compute_delta(self, val):
        if self.length < self.period + 1:
            return 0
        mean = sum(self.kept_values[-1 - self.period:-1]) / self.period
        return abs(val - mean)

    def update(self):
        if self.length > self.period:
            self.update_r()
            self.update_g()
        else:
            self.r_val.append(float('nan'))
            self.g_val.append(float('nan'))
        s = float('nan')
        if self.length >= self.period:
            mean = sum(self.kept_values[-self.period:]) / self.period
            s = sqrt(sum([((self.kept_values[i] - mean) ** 2)
                               for i in range(-self.period, 0)]) / self.period)
        self.s_val.append(s)

        delta = self.compute_delta(self.kept_values[-1])
        if self.length < 6:
            self.weird_values.append({'delta': delta, 'value': self.kept_values[-1]})
        elif delta > self.weird_values[-1]['delta']:
            for i in range(0, 5):
                if self.weird_values[i]['delta'] < delta:
                    self.weird_values.insert(i, {'delta': delta, 'value': self.kept_values[-1]})
                    self.weird_values.pop(-1)
                    break

    def end(self):
        val = min(5, self.length)
        print("Global tendency switched %d times" % self.nb_switches)
        print("{} weirdest values are {}".format(val, [self.weird_values[i]['value'] for i in range(0, val)]))

    def start(self):
        while True:
            val = input()
            if val == "STOP":
                self.end()
                if self.graphical is True:
                    plt.show()
                return
            try:
                self.kept_values.append(float(val))
            except EOFError:
                exit(0)
            except:
                print("please enter a correct number")
                continue
            self.length += 1
            self.update()
            self.display()
