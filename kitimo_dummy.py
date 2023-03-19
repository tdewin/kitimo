#!/usr/bin/env python
# coding=utf-8
# MIT 2023 github.com/tdewin

import inkex

from inkex.elements import TextElement,Group,Circle
from inkex.transforms import Transform
from inkex.styles import Style


import time
import sys
import re

def current_milli_time():
    return str(round(time.time() * 1000))

class KitimoDummy(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--r", type=int, default=1)
        pars.add_argument("--l", type=int, default=1)


    def effect(self):
        layer = self.svg.get_current_layer()
        g = Group.new("KitimoDummy")
        layer.append(g)

if __name__ == "__main__":
    f = open("c:\\d\\kitimodummydriver.log", "a")
    f.write("{0} - Dummy Test\n".format(current_milli_time()))
    argcmd = ' '.join(sys.argv[0:])
    f.write("{0}\n".format(argcmd))
    
    potentialsvg = sys.argv[len(sys.argv)-1]
    if re.search("[.]svg.*",potentialsvg):
        f.write("Got input svg {0}, dumping..".format(potentialsvg))
        svgfile = open(potentialsvg, "r")
        data = svgfile.read()
        svgfile.close()
        f.write(data)
    else:
        f.write("No sigar {0} ...".format(potentialsvg))
        
    f.close()
    KitimoDummy().run()
