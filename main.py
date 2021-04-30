import xml.etree.ElementTree as ET
import copy
import json

def assign(li, idx, val, pad={}):
    if len(li) <= idx:
        for _ in range(idx - len(li) + 1):
            li.append(pad)
    li[idx] = val

def parse_color(hexstr):
    h = hexstr.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def int2rgb(num):
    b = num&255
    g = (num>>8)&255
    r = (num>>16)&255

    return (r,g,b)

def rgb2int(r,g,b):
    rgb = r;
    rgb = (rgb << 8) + g
    rgb = (rgb << 8) + b

    return rgb

f = open("in.xml", "rb")
data = f.read().decode("utf8")
f.close()

root = ET.fromstring(data)

out = {
    "wireMagic": "pb3",
    "pens": [],
    "wsWinStyles": [],
    "wpWinPositions": [],
    "events": []
}

head = root.find("head")

for pen in head.findall("pen"):
    pen_d = {}
    idx = 0
    for key in pen.attrib:
        value = pen.attrib[key]
        if key == "b":
            pen_d["bAttr"] = int(value)

        elif key == "i":
            pen_d["iAttr"] = int(value)

        elif key == "u":
            pen_d["uAttr"] = int(value)

        elif key == "fc":
            rgb = parse_color(value)
            pen_d["fcForeColor"] = rgb2int(*rgb)

        elif key == "bc":
            rgb = parse_color(value)
            pen_d["bcBackColor"] = rgb2int(*rgb)

        elif key == "sz":
            pen_d["szPenSize"] = int(value)

        elif key == "bo":
            pen_d["boBackAlpha"] = int(value)

        elif key == "fo":
            pen_d["foForeAlpha"] = int(value)
        
        elif key == "et":
            pen_d["etEdgeType"] = int(value)

        elif key == "rb":
            pen_d["rbRuby"] = int(value)

        elif key == "hg":
            pen_d["hgHorizGroup"] = int(value)
        
        elif key == "ec":
            rgb = parse_color(value)
            pen_d["ecEdgeColor"] = rgb2int(*rgb)

        elif key == "fs":
            pen_d["fsFontStyle"] = int(value)

        elif key == "of":
            pen_d["ofOffset"] = int(value)
        elif key == "id":
            idx = int(value)
        else:
            print(key, value)
    assign(out["pens"], idx, pen_d)

for wp in head.findall("wp"):
    wp_d = {}
    idx = 0
    for key in wp.attrib:
        value = wp.attrib[key]

        if key == "ap":
            wp_d["apPoint"] = int(value)
        elif key == "ah":
            wp_d["ahHorPos"] = int(value)
        elif key == "av":
            wp_d["avVerPos"] = int(value)
        elif key == "id":
            idx = int(value)
        else:
            print(key, value)
    assign(out["wpWinPositions"], idx, wp_d)

for ws in head.findall("ws"):
    ws_d = {}
    idx = 0
    for key in ws.attrib:
        value = ws.attrib[key]

        if key == "ju":
            ws_d["juJustifCode"] = int(value)
        elif key == "pd":
            ws_d["pdPrintDir"] = int(value)
        elif key == "sd":
            ws_d["sdScrollDir"] = int(value)
        elif key == "id":
            idx = int(value)
        else:
            print(key, value)
    assign(out["wsWinStyles"], idx, ws_d)

body = root.find("body")
for p in body.findall("p"):
    p_d = {"segs":[]}
    idx = 0
    for key in p.attrib:
        value = p.attrib[key]

        if key == "t":
            p_d["tStartMs"] = int(value)
        elif key == "d":
            p_d["dDurationMs"] = int(value)
        elif key == "wp":
            p_d["wpWinPosId"] = int(value)
        elif key == "ws":
            p_d["wsWinStyleId"] = int(value)
        elif key == "p":
            p_d["pPenId"] = int(value)
        else:
            print(key, value)

    pdd = copy.deepcopy(p_d)
    if len(p.findall("s")) <= 0:
        pdd["segs"].append({"utf8": p.text.replace("\u200b", "") })
        out["events"].append(pdd)
    else:
        for seg in p.findall("s"):
            seg_d = {"utf8": seg.text.replace("\u200b", "") }
            for key in seg.attrib:
                value = seg.attrib[key]
                if key == "p":
                    seg_d["pPenId"] = int(value)
                else:
                    print(key)
            pdd["segs"].append(seg_d)
            out["events"].append(pdd)

f=open("out", "w")
f.write(json.dumps(out, ensure_ascii=False, indent=2))
f.close()
