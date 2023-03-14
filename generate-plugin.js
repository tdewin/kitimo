//node generate-plugin.js . "Kitimo" "Perfect Circle"
const path = require('path');
const fs = require('fs');
const { exit } = require('process');


var args = process.argv.slice(2);

if (args.length < 3) {
    console.log("<dir> <effectMenu> <pluginName>")
    exit
}
//let extPath = path.join(process.env.ProgramFiles,"Inkscape","share","inkscape","extensions");
let extPath = args[0]

if (!fs.existsSync(extPath)) {
    console.log("not a valid path")
    exit
}

let effectMenu = args[1]
let pluginName = args[2]
let fullName = `${effectMenu} ${pluginName}`
let fName = fullName.replaceAll(" ","_").toLowerCase()
let className = fullName.replaceAll(" ","")
let uid = `com.github.tdewin.inkscape.${className}`

let menuFile = path.join(extPath,`${fName}.inx`)
let menuInx = `<?xml version="1.0" encoding="UTF-8"?>
<inkscape-extension xmlns="http://www.inkscape.org/namespace/inkscape/extension">
    <name>${pluginName}</name>
    <id>${uid}</id>
    <param name="tab" type="notebook">
        <page name="Parameters" gui-text="Main Parameters">
            <param name="l"   type="int" min="1" max="100" gui-text="Line of circle">1</param>
            <param name="r"   type="int" min="1" max="100" gui-text="Radius of a circle">1</param>
        </page>
        <page name="Help" gui-text="Help">
            <label xml:space="preserve">Drawing Perfect Circles
            </label>
        </page>
    </param>
    <effect>
        <object-type>all</object-type>
        <effects-menu>
            <submenu name="${effectMenu}"/>
        </effects-menu>
    </effect>
    <script>
        <command location="inx" interpreter="python">${fName}.py</command>
    </script>
</inkscape-extension>`

fs.writeFileSync(menuFile,menuInx,"utf8")
console.log("Wrote to ",menuFile)

let pyFile = path.join(extPath,`${fName}.py`)
let code = `#!/usr/bin/env python
# coding=utf-8
# MIT 2023 github.com/tdewin

import inkex

from inkex.elements import TextElement,Group,Circle
from inkex.transforms import Transform
from inkex.styles import Style

class ${className}(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--r", type=int, default=1)
        pars.add_argument("--l", type=int, default=1)


    def effect(self):
        layer = self.svg.get_current_layer()
        
        g = Group.new("${className}")

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
    ${className}().run()
`

fs.writeFileSync(pyFile,code,"utf8")
console.log("Wrote to ",pyFile)