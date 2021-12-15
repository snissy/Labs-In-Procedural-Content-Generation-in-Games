"""
5.7 Lab exercise: Create plants with L-systems
In this lab exercise, you will implement a simple bracketed L-system to generate
plants. Use an L-system to generate your plants and a turtle graphics program to
draw them. You will be given a software package that contains three main classes:
LSystem, State and Canvas. Your main work will be to implement the two main

methods in the LSystem class:
'public void expand(int depth)'
'public void interpret(String expression)'

The L-system has an alphabet, axioms, production rules, a starting point, a start-
ing angle, a turning angle and a length for each step. The expand method is used to
96 Julian Togelius, Noor Shaker, and Joris Dormans

expand the axiom of the L-system a number of times specified by the depth param-
eter. After expansion, the system processes the expansion and visualises it through
the interpret method. The result of each step is drawn on the canvas. Since the L-
system will be in a number of different states during expansion, a State class is
defined to represent each state. An instance of this class is made for each state of
the L-system and the variables required for defining the state are passed on from the
L-system to the state; these include the x and y coordinates, the starting and turning
angles and the length of the step. The L-system is visualised by gradually drawing
each of its states.
The State and the Canvas classes are helpers, and therefore there is no need
to modify them. The Canvas class has the methods required for simple drawing
on the canvas and it contains the main method to run your program. In the main
method, you can instantiate your L-system, define your axiom and production rules
and the number of expansions. Figure 5.23 presents example L-systems generated
using the following rules: (F,F,F → FF−[−F +F +F]+[+F −F −F]) (left) and
(F, f,(F → FF, f → F − [[ f] + f] + F[+F f ] − f)) (right). Note that the rules are
written in the form G = ( A,S,P), where A is the alphabet, S is the axiom or starting
point and P is the set of production rules.
You can use the same software to draw fractal-like forms such as the ones pre-
sented in Figure 5.24. Some simple example rules that can be used to create rel-
atively complex shapes are the following: (F,F + F + F + F,(F + F + F + F →
F +F +F +F,F → F +F −F −FF+F +F −F)) (left), (F,F ++F ++F,F →
F −F ++F −F) (middle) and (F, f,(f → F − f −F,F → f +F + f)) (right).

"""

from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm

"""
alphabet:F,
axiom: F,
rules: F → FF−[−F +F +F]+[+F −F −F]

alphabet:F,
axiom: f,
rules:  F → FF
        f → F − [[ f] + f] + F[+F f ] − f

"""


def drawLine(p1, p2):
    x_values = [p1[0], p2[0]]
    y_values = [p1[1], p2[1]]
    plt.plot(x_values, y_values, 'black')


class LSystem:
    sigma = (30/360)*2*np.pi
    alphabet = set("F")
    productionRules = {"F": "FF-[-F+F+F]+[+F-F-F]"}

    def __init__(self, axiom, iterations):
        self.word = axiom
        self.iter = iterations

    def GetWord(self):
        return self.word

    def GenerateString(self):

        newString = []

        for i in range(self.iter):

            for c in self.word:

                if c in self.alphabet:
                    newString.append(self.productionRules[c])
                else:
                    newString.append(c)

            self.word = "".join(newString)
            newString.clear()

        print("Have generated string")

    def ShowCanvasInterpret(self):

        """
        import matplotlib.pyplot as plt
        x1, y1 = [-1, 12], [1, 4]
        x2, y2 = [1, 10], [3, 2]
        plt.plot(x1, y1, x2, y2, marker = 'o')
        plt.show()

        plt.axline((0, 0), (1, 1), linewidth=1, color='b')
        :return:
        """

        plusRot = np.array([[np.cos(self.sigma), -np.sin(self.sigma)],
                            [np.sin(self.sigma), np.cos(self.sigma)]])

        minusRot = np.array([[np.cos(-self.sigma), -np.sin(-self.sigma)],
                             [np.sin(-self.sigma), np.cos(-self.sigma)]])

        forwardFactor = 10
        currentPos = np.array([0, 0])
        currentDir = np.array([np.cos(np.pi/4), np.sin(np.pi/4)])
        stack = []

        print("Drawing tree to matplotlib")

        for c in tqdm(self.word):

            if c == "F":
                # Forward some pixel based on depth on stack I guess.
                forwardStep = forwardFactor - 5.5*(np.log(1+len(stack)))
                newPos = currentPos + forwardStep * currentDir
                drawLine(currentPos, newPos)
                currentPos = newPos

            elif c == "+":
                currentDir = plusRot.dot(currentDir)

            elif c == '-':
                currentDir = minusRot.dot(currentDir)
            elif c == '[':
                # New Stack !
                stack.append((currentPos, currentDir))
                pass
            elif c == ']':
                # close stack
                currentPos, currentDir = stack.pop()

        plt.show()


if __name__ == '__main__':
    testSystem = LSystem("F", 4)  # This corresponds to the book example.
    testSystem.GenerateString()
    testSystem.ShowCanvasInterpret()
