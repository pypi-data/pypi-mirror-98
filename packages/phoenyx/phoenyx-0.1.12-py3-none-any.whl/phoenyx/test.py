from phoenyx import *
import math
import numpy

from renderer import *  # type: ignore
from menu import *  # type: ignore
from slider import *  # type: ignore
from button import *  # type: ignore

renderer: Renderer = Renderer(600, 600, "rotation")
angle = 0
points: list[Vector] = []
for t in numpy.arange(0, 2 * math.pi, math.pi / 4):
    points.append(Vector(300 + 100 * math.cos(t), 300 + 100 * math.sin(t)))


def setup():
    renderer.text_size = 15
    renderer.text_color = 255

    renderer.no_stroke()
    renderer.fill = "cyan"


def draw():
    global angle
    angle += 0.01
    renderer.background(51)

    renderer.polygon(*points)
    renderer.rotate_display(angle)

    renderer.text(10, 10, f"fps : {round(renderer.fps)}")
    renderer.text(10, 20, f"angle in degrees : {round(math.degrees(angle), 1)}")


renderer.run(draw, setup=setup)
