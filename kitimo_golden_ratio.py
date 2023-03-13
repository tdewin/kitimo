#!/usr/bin/env python
# coding=utf-8
# MIT 2023 github.com/tdewin

import inkex

from inkex.elements import TextElement,Group,Circle
from inkex.transforms import Transform
from inkex.styles import Style

class KitimoGoldenRatio(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--max", type=int, default=8)
        pars.add_argument("--r", type=int, default=1)
        pars.add_argument("--l", type=int, default=1)
        pars.add_argument("--x", type=int, default=0)
        pars.add_argument("--y", type=int, default=0)


    def effect(self):
        layer = self.svg.get_current_layer()
        
        g = Group.new("golden-circles")

        fib = [1,2]
        max = self.options.max-len(fib)
        for x in range(max):
            l = len(fib)
            fib.append(fib[l-1]+fib[l-2])

        ### If you wanted to print text with the circles
        # textElement = TextElement()
        # textElement.set("inkscape:label","textGolden")
        # textElement.set("id","textGolden")
        # textElement.text = ', '.join(str(x) for x in fib)
        # g.append(textElement)

        r = self.options.r
        s = Style.parse_str("fill:none;stroke:#333333;stroke-width:{0};stroke-linejoin:round;paint-order:markers fill stroke;stop-color:#000000".format(self.options.l))

        
        for f in fib:
            c = Circle()
            c.set("inkscape:label","c{0}".format(f))
            c.radius = r*f
            # no offset, we global offset with transform on the group
            # but just for documentation purposes
            c.center = [0,0]
            c.style = s
            g.append(c)

        
        
        g.transform = Transform(translate=(self.options.x, self.options.y))

        layer.append(g)

      

if __name__ == "__main__":
    KitimoGoldenRatio().run()
