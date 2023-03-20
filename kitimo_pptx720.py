#!/usr/bin/env python
# coding=utf-8
# MIT 2023 github.com/tdewin

import inkex

from inkex.elements import TextElement,Group,Circle,Layer,Rectangle
from inkex.paths import Path,Move,Horz,Vert
from inkex.transforms import Transform
from inkex.styles import Style

# manual troubleshooting
# cd 'C:\Program Files\Inkscape\share\inkscape\extensions\'
# ..\..\..\bin\python.exe $env:USERPROFILE\Documents\dev\kitimo\kitimo_pptx720.py .\kitimo_logo.svg
from lxml import etree

class KitimoPPTX720(inkex.EffectExtension):
	def add_arguments(self, pars):
		pars.add_argument("--tab")
		pars.add_argument("--height", type=int, default=720)
		pars.add_argument("--ratio", default="16/9")
		pars.add_argument("--numPages", type=int, default=5)
		pars.add_argument("--moveX", type=float, default=0)
		pars.add_argument("--moveY", type=float, default=1)
		pars.add_argument("--guideX", default="100,1180")
		pars.add_argument("--guideY", default="200")
		pars.add_argument("--dark",type=inkex.Boolean, default=False)
		pars.add_argument("--rectLayer",type=inkex.Boolean, default=False)
		pars.add_argument("--fakeGuide",type=inkex.Boolean, default=False)

	def effect(self):
		svg = self.svg

		sp = svg.namedview
		rectLayer = self.options.rectLayer
		fakeGuide = self.options.fakeGuide

		for page in sp:
			sp.remove(page)

		r =  list(map(lambda x:int(x),self.options.ratio.split("/")))
		height = self.options.height
		width = int(height*r[0]/r[1])


		numPages = self.options.numPages
		moveX = self.options.moveX
		moveY = self.options.moveY

		guideX = list(map(lambda x:int(x),self.options.guideX.split(",")))
		guideY = list(map(lambda x:int(x),self.options.guideY.split(",")))

		fakeGuideStyle = Style.parse_str("stroke:{0};stroke-width:{1};stroke-linejoin:round;paint-order:markers fill stroke;stop-color:#000000".format("#ff0000",3))
		fakeGuideLayer = Layer()

		if fakeGuide:
			fakeGuideLayer.set("sodipodi:insensitive","true")
			fakeGuideLayer.set("inkscape:label","fakeguidelayer")
			fakeGuideLayer.set("inkscape:groupmode","layer")
			fakeGuideLayer.set("id","fakeguidelayer")

			# 0 means only line required
			#etree.register_namespace("sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")

			if moveX == 0:
				for g in guideX:
					#self.svg.namedview.new_guide(g, False)
					p = Path()
					p.append(Move(g,0))
					p.append(Vert(height*numPages))
					pe = inkex.PathElement.new(p)
					pe.set("style",fakeGuideStyle)
					fakeGuideLayer.insert(0,pe)
				
			if moveY == 0:
				for g in guideY:
					#self.svg.namedview.new_guide(g, True)
					p = Path()
					p.append(Move(0,g))
					p.append(Horz(width*numPages))
					pe = inkex.PathElement.new(p)
					pe.set("style",fakeGuideStyle)
					fakeGuideLayer.insert(0,pe)


		
 
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

		
		sp.set("bordercolor",border)
		sp.set("pagecolor",fg)
		sp.set("inkscape:deskcolor",bg)

		sp.set("inkscape:document-units","px")
		sp.set("inkscape:showpageshadow","false")
		sp.set("inkscape:cy",int(height/2))
		sp.set("inkscape:cx",int(width/2))
		
		

		#https://stackoverflow.com/questions/62395506/how-do-i-create-a-namespaced-element-with-lxml
		#etree.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")

		nl = Layer()
		s = Style.parse_str("fill:{0};stroke:#333333;stroke-width:{1};stroke-linejoin:round;paint-order:markers fill stroke;stop-color:#000000".format(fg,0))
			

		for i in range(0,numPages):
			y = height*(moveY*i)
			x = width*(moveX*i)
			page = self.svg.namedview.new_page(str(x), str(y), str(width), str(height), "kitimo-page-{0}".format(i))
			page.set("id","kitimo-page-{0}".format(i))

			if fakeGuide:
				if moveX != 0:
					for g in guideX:
						#self.svg.namedview.new_guide(x, False)
						p = Path()
						p.append(Move(x+g,0))
						p.append(Vert(height))
						pe = inkex.PathElement.new(p)
						pe.set("style",fakeGuideStyle)
						fakeGuideLayer.insert(0,pe)
					
				if moveY  != 0:
					for g in guideY:
						#self.svg.namedview.new_guide(y, True)
						p = Path()
						p.append(Move(0,y+g))
						p.append(Horz(width))
						pe = inkex.PathElement.new(p)
						pe.set("style",fakeGuideStyle)
						fakeGuideLayer.insert(0,pe)
			
			if rectLayer:
				c = Rectangle.new(top=y,left=x,width=width,height=height)
				c.set("inkscape:label","kitimo-bgpage-{0}".format(i))
				c.set("id","kitimo-bgpage-{0}".format(i))
				c.style = s
				nl.insert(0,c)

		if fakeGuide:	
			svg.insert(0,fakeGuideLayer)

		#always make a background layer just for a best practice
		nl.set("sodipodi:insensitive","true")
		nl.set("inkscape:label","bglayer")
		nl.set("inkscape:groupmode","layer")
		nl.set("id","kitimo-bg-layer")
		svg.insert(0,nl)

		

if __name__ == "__main__":
	KitimoPPTX720().run()
