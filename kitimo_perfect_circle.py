#!/usr/bin/env python
# coding=utf-8
# MIT 2023 github.com/tdewin

import inkex

from inkex.elements import TextElement,Group,Circle
from inkex.transforms import Transform
from inkex.styles import Style

class KitimoPerfectCircle(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--r", type=int, default=1)
        pars.add_argument("--l", type=int, default=1)


    def effect(self):
        layer = self.svg.get_current_layer()
        
        g = Group.new(KitimoPerfectCircle)

        r = self.options.r
        s = Style.parse_str("fill:none;stroke:#333333;stroke-width:{0};stroke-linejoin:round;paint-order:markers fill stroke;stop-color:#000000".format(self.options.l))
       
        c = Circle()
        c.set("inkscape:label","c")
        c.radius = r
        c.center = [0,0]
        c.style = s
        g.append(c)


        layer.append(g)

if __name__ == "__main__":
    KitimoPerfectCircle().run()
