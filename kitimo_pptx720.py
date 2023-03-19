#!/usr/bin/env python
# coding=utf-8
# MIT 2023 github.com/tdewin

import inkex

from inkex.elements import TextElement,Group,Circle
from inkex.transforms import Transform
from inkex.styles import Style

from lxml import etree

class KitimoPPTX720(inkex.EffectExtension):
	def add_arguments(self, pars):
		pars.add_argument("--tab")
		pars.add_argument("--height", type=int, default=720)
		pars.add_argument("--ratio", default="16/9")
		pars.add_argument("--numPages", type=int, default=5)
		pars.add_argument("--moveX", type=float, default=0)
		pars.add_argument("--moveY", type=float, default=1)
		pars.add_argument("--dark",type=inkex.Boolean, default=False)

	def effect(self):
		svg = self.svg
		r =  list(map(lambda x:int(x),self.options.ratio.split("/")))

		


		numPages = self.options.numPages
		moveX = self.options.moveX
		moveY = self.options.moveY

		height = self.options.height
		width = int(height*r[0]/r[1])
 
		svg.set("width",width)
		svg.set("height",height)
		svg.set("viewBox","0 0 {width} {height}".format(width=width,height=height))
		
		bg = "#1c1c1c"
		fg = "#f2f2f2"
		border = "#00b7ff"

		if self.options.dark:
			t = bg
			bg = fg
			fg = t

		sp = svg.xpath('//svg:svg/sodipodi:namedview')[0]
		sp.set("bordercolor",border)
		sp.set("pagecolor",fg)
		sp.set("inkscape:deskcolor",bg)

		sp.set("inkscape:document-units","px")
		sp.set("inkscape:showpageshadow","false")
		sp.set("inkscape:cy",int(height/2))
		sp.set("inkscape:cx",int(width/2))
		
		for page in sp:
			sp.remove(page)

		#https://stackoverflow.com/questions/62395506/how-do-i-create-a-namespaced-element-with-lxml
		#etree.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")
		for i in range(0,numPages):
			page = etree.Element(etree.QName("http://www.inkscape.org/namespaces/inkscape","page"))
			page.set("id","kitimo-page-{0}".format(i))
			page.set("height",str(height))
			page.set("width",str(width))
			page.set("y",str(height*(moveY*i)))
			page.set("x",str(width*(moveX*i)))
			sp.append(page)		

if __name__ == "__main__":
	KitimoPPTX720().run()
