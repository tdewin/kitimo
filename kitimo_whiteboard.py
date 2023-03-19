#!/usr/bin/env python
# coding=utf-8
# MIT 2023 github.com/tdewin

import inkex

from inkex.elements import TextElement,Group,Circle,Rectangle,Tspan
from inkex.transforms import Transform
from inkex.styles import Style

import re

def elementName(e):
    if e.get("inkscape:label") != None:
        return e.get("inkscape:label")
    return e.get("id")

class KitimoWhiteBoard(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--bg", type=inkex.Color, default="#eeeeee")
        pars.add_argument("--fontSize", type=int, default=16)
        pars.add_argument("--fontSizeMode", type=int, default=1)



    def effect(self):
        #https://inkscape-extensions-guide.readthedocs.io/en/latest/_modules/inkex/deprecated.html#DeprecatedEffect.getselected
        #https://inkscape-extensions-guide.readthedocs.io/en/latest/_modules/inkex/elements.html
        #baseelement is basically a glorified xml element https://lxml.de/api/lxml.etree.ElementBase-class.html
        layer = self.svg.get_current_layer()
        
        selected = self.svg.selected

        if len(selected) == 1 and selected[0].TAG.lower() == "text" and len(list(selected[0])) == 1:
            t = selected[0]
            tSpan = list(t)[0]

            match = re.search("([a-zA-Z0-9]+)(,([0-9]+))?(:)?(.*)", tSpan.text)
            if match:
                wbClass = match.group(1)
                wbBlockSize = 1

                wbSubtext = match.group(5)

                if match.group(3) is not None:
                    wbBlockSize = int(match.group(3))
                else:
                    wbBlockSize = max(1,round(len(wbClass)/2))
                

                gName = "grouped - {0} {1}".format(elementName(t),len(list(t)))
                g = Group.new(gName)
                
                fontSize = self.options.fontSize
                if self.options.fontSizeMode == 1:
                    fontSize = round(float(t.style.get("font-size").replace("px","")))
                
                boxSize = fontSize*3.5
                boxFontSize = fontSize*2

                xOffset = int(fontSize/2)
                yOffset = xOffset+boxFontSize

                #TextElement in inkex\elements\_text.py
                #Bounding box in inkex\transforms.py 
                boundingBox = t.shape_box()
                left = boundingBox.left
                top = boundingBox.top

                g.transform = Transform(translate=(left,top))

                textStyle = Style.parse_str("font-size:{0}px;line-height:1.25;font-family:{1};-inkscape-font-specification:'{1}, Normal';font-variant-ligatures:none;letter-spacing:0px;word-spacing:0px;stroke-width:0".format(fontSize,"Cascadia Mono"))

                t.set("x",0)
                t.set("y",boxSize+fontSize)
                tSpan.set("x",0)
                tSpan.set("y",boxSize+fontSize)

                t.transform = None
                tSpan.transform = None
                tSpan.text = wbSubtext

                t.style = textStyle

                p = t.getparent()
                p.remove(t)
                g.append(t)


                # class box
                bg = self.options.bg
                s = Style.parse_str("fill:{0};stroke:#333333;stroke-width:{1};stroke-linejoin:round;paint-order:markers fill stroke;stop-color:#000000".format(bg,2))
            
                c = Rectangle.new(top=0,left=0,width=(boxSize)*wbBlockSize,height=boxSize)
                c.set("inkscape:label","r")
                c.style = s
                g.append(c)

                textStyle = Style.parse_str("font-size:{0}px;line-height:1.25;font-family:{1};-inkscape-font-specification:'{1}, Normal';font-variant-ligatures:none;letter-spacing:0px;word-spacing:0px;stroke-width:0".format(int(boxFontSize),"Cascadia Mono"))
                ct = TextElement.new(x=xOffset,y=yOffset)
                ct.style = textStyle
                ctSpan = Tspan.new(x=xOffset,y=yOffset)
                ctSpan.text = wbClass
                ct.append(ctSpan)
                g.append(ct)

                layer.append(g)
            else:
                inkex.errormsg(_("Could detect whiteboard syntax class:subtext"))
        else:
            #https://inkscape-extensions-guide.readthedocs.io/en/latest/_modules/inkex/utils.html?highlight=exception
            inkex.errormsg(_("This extension requires a single text to be selected GOT {0} objects (or it is not a text or not a single tspan (multiline))".format(str(len(selected)))))

if __name__ == "__main__":
    KitimoWhiteBoard().run()
