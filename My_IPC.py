import csv
import sys
import re
import os

sys.path.append(os.path.join(sys.path[0], "kicad-footprint-generator"))  # enable package import from directory

from KicadModTree import *

'''Debug Mode'''
debug = True
#debug = False
print(f"DEBUG: {debug}")

def dprint(x=None):
    if debug:
        if x == None:
            print("") # Empty Line
        else:
            print(x) # Only when Debug

'''Units Conversions'''
def mm(n):           # to convert ipc to mm
    return float(n)/100
def mil(n):      # to convert ipc to mm
    return float(n)*100/2.54

'''AD - Axial Cylindrical Jellybean Type Packages (Like Common Resistors)'''
def res_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = mm(match[1]) # LS
    pitch = 0
    pins = 2
    cols = 2
    rows = 1
    lead_width = mm(match[3]) # W
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = 0
    length = mm(match[5]) # L
    width = mm(match[7]) # D
    height = mm(match[7]) # D
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''ADV - Axial Cylindrical Jellybean Type Packages Verticaly Mounted (Like Common Resistors)'''
def rev_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = mm(match[1]) # LS
    pitch = 0
    pins = 2
    cols = 2
    rows = 1
    lead_width = mm(match[3]) # W
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = mm(match[7]) # D
    length = mm(match[5]) # L
    width = 0
    height = 0
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''AR - Axial Rectangular Jellybean Type Packages (Like Power Resistors)'''
def pow_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = mm(match[1]) # P
    pitch = 0
    pins = 2
    cols = 2
    rows = 1
    lead_width = mm(match[3]) # W
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = 0
    length = mm(match[5]) # L
    width = mm(match[7]) # T
    height = mm(match[9]) # H
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''ARV - Axial Rectangular Jellybean Type Packages Verticaly Mounted (Like Power Resistors)'''
def pov_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = mm(match[1]) # LS
    pitch = 0
    pins = 2
    cols = 2
    rows = 1
    lead_width = mm(match[3]) # W
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = 0
    length = mm(match[5]) # L
    width = mm(match[7]) # T
    height = mm(match[9]) # H
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''RD - Cylindrical Jellybean Type Packages (Like Electrolytic Capacitors or LEDs)'''
def cap_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = mm(match[1]) # P
    pitch = 0
    pins = 2
    cols = 2
    rows = 1
    lead_width = mm(match[3]) # W
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = mm(match[5]) # D
    length = 0
    width = 0
    height = mm(match[7]) # H
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''RR - Radial Jellybean Type Packages (Like Common Box Film Caps and Ceramic Disc Caps)'''
def box_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = mm(match[1]) # P
    pitch = 0
    pins = 2
    cols = 2
    rows = 1
    lead_width = mm(match[3]) # W
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = 0
    length = mm(match[5]) # L
    width = mm(match[7]) # T
    height = mm(match[9]) # H
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''One Row, Multiple Pins Type Packages Horizonlal (Like SIP)'''
def sip_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = 0
    pitch = mm(match[5]) # P
    pins = int(match[11]) # Q
    cols = pins
    rows = 1
    lead_width = mm(match[3]) # W
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = 0
    length = mm(match[7]) # L
    width = mm(match[1]) # T
    height = mm(match[9]) # H
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''DIP Style Packages'''
def dip_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    try:        # Check if a Width is Given
        width_calc = mm(line["Width"])
    except:     # Calculate the Aproximative Width
        if "DIPS" in match: width_calc = lead_span + pitch
        else: width_calc = lead_span - pitch
    lead_span = mm(match[1]) # LS
    lead_width = mm(match[3]) # W
    pitch = mm(match[5]) # P
    pins = int(match[11]) # Q
    cols = 2
    rows = int(pins/cols)
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = 0
    length = mm(match[7]) # L
    width = width_calc
    height = mm(match[9]) # H
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''Multiple Rows, Multiple Pins Type Packages'''
def pga_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = 0
    pitch = mm(match[3]) # P
    pins = int(match[1]) # Q
    cols = int(match[5]) # C
    rows = int(match[7]) # R
    lead_width = 0
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = 0
    length = mm(match[9]) # L
    width = mm(match[11]) # T
    height = mm(match[13]) # H
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''Jumper, Wires'''
def jmp_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = mm(match[1]) # LS
    pitch = 0
    pins = 2
    cols = 2
    rows = 1
    lead_width = mm(match[3]) # W
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = 0
    length = lead_width
    width = lead_span
    height = lead_width
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''Mounting Holes'''
def mtg_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = 0
    pitch = 0
    pins = 1
    cols = 1
    rows = 1
    lead_width = 0
    hole_size = mm(match[3]) # HS
    land_size = mm(match[1]) # LD
    if match[4] == "Z":
        antipad_size = mm(match[5]) # Z
    else:
        antipad_size = 0
    if match[4] == "V":
        vias = int(match[5]) # V
    else:
        vias = 0
    diameter = 0
    length = 0
    width = 0
    height = 0
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''Circular Transistor Outlines (Like TO-99 Packages)'''
def tor_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

    lead_span = 0
    pitch = mm(match[1]) * 2 # PR
    pins = int(match[7]) # Q
    cols = 1
    rows = 1
    lead_width = 0
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = mm(match[3]) # D
    length = 0
    width = 0
    height = mm(match[5]) # H
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''Inline Transistor Outlines (Like TO-220 Packages)'''
def top_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = 0
    pitch = mm(match[1]) # P
    pins = int(match[9]) # Q
    cols = pins
    rows = 1
    lead_width = 0
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = 0
    if match[7] > max(match[3], match[5]):
        length = min(mm(match[5]), mm(match[3]))
        width = max(mm(match[5]), mm(match[3]))
    else:
        length = mm(match[3]) # L
        width = mm(match[5]) # T
    height = mm(match[7]) # H
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''HDR - Pin Headers'''
def hdr_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = 0
    pitch = mm(match[5]) # P
    pins = int(match[1]) # Q
    cols = int(match[9]) # R
    rows = int(match[7]) # C
    lead_width = mm(match[3]) # W
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = 0
    length = mm(match[11]) # L
    width = mm(match[13]) # T
    height = mm(match[15]) # H
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''Circular Test Points'''
def tpc_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = 0
    pitch = 0
    pins = 1
    cols = 1
    rows = 1
    lead_width = mm(match[1]) # W
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = mm(match[3]) # D
    length = 0
    width = 0
    height = mm(match[5]) # H
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level

'''Square Test Points'''
def tpr_type(match):
    global lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level
    lead_span = 0
    pitch = 0
    pins = 1
    cols = 1
    rows = 1
    lead_width = mm(match[1]) # W
    hole_size = 0
    land_size = 0
    antipad_size = 0
    vias = 0
    diameter = 0
    length = mm(match[3]) # L
    width = mm(match[3]) # L
    height = mm(match[5]) # H
    fab_level = str(match[16]) # FL
    return lead_span, pitch, pins, cols, rows, lead_width, hole_size, land_size, antipad_size, vias, diameter, length, width, height, fab_level



'''CSV Paths'''
my_file = "ipc.csv"     # Complete

'''IPC Name Regex'''
my_regex = re.compile(r'([A-Z]+)(\d+)(\D)(\d+)(\D*)(\d*)(\D*)(\d*)(\D*)(\d*)(\D*)(\d*)(\D*)(\d*)(\D*)(\d*)([ABC])', re.I)

'''CSV Parsing'''
with open(my_file, 'r') as csv_file: #
    csv_reader = csv.DictReader(csv_file, delimiter = ";")
    for line in csv_reader:
        matches = my_regex.findall(line["IPC Name"])
        for match in matches:
            match = [x.upper() for x in match]
            footprint_name = str((line["IPC Name"]).upper())
            description = str(line["IPC Description"])

            dprint("\n"+str(match))

            # Default Margins
            margin = mm(254) / 8
            # silkscreen margins
            s_margin_d = +margin*4
            s_margin_h = +margin*4
            s_margin_w = +margin*4
            # courtyard margins
            c_margin_d = +margin*8
            c_margin_h = +margin*8
            c_margin_w = +margin*8

            if "CAPAD" in match or "CAPPAD" in match or "DIOAD" in match or "FUSAD" in match or "INDAD" in match or "RESAD" in match:
                res_type(match)
                # AD Margins
                # silkscreen margins
                s_margin_h = +pitch/2+(lead_span-length)+(margin*8)
                # courtyard margins
                c_margin_h = pitch/2+(lead_span-length)+(margin*12)
            elif "CAPAR" in match or "RESAR" in match:
                pow_type(match)
                # AR Margins
                # silkscreen margins
                s_margin_h = +pitch/2+(lead_span-length)+(margin*8)
                # courtyard margins
                c_margin_h = +pitch/2+(lead_span-length)+(margin*12)
            elif "CAPRR" in match or "FUSRR" in match or "CAPRB" in match or "CAPAR" in match or "RESAR" in match:
                box_type(match)

            elif "CAPRD" in match or "CAPPRD" in match or "LEDRD" in match:
                cap_type(match)
            elif "DIP" in match or "DIPS" in match or "OSC" in match:
                dip_type(match)
                length, width = width, length

            elif "SIP" in match:
                sip_type(match)

            elif "PGA" in match:
                pga_type(match)

            elif "TO" in match:
                if match[2] == "R":
                    tor_type(match)
                elif match[2] == "P":
                    top_type(match)
                    length, width = width, length
            elif "MTGP" in match or "MTGNP" in match:
                mtg_type(match)
            elif "HDRRA" in match or "HDRV" in match:
                hdr_type(match)
            elif "TPCW" in match:
                tpc_type(match)
            elif "TPRW" in match:
                tpr_type(match)
            elif "JUMP" in match:
                jmp_type(match)
                length, width = width, length
            elif "CAPADV" in match or "CAPPADV" in match or "DIOADV" in match or "FUSADV" in match or "INDADV" in match or "RESADV" in match:
                rev_type(match)
            elif "CAPARV" in match or "RESARV" in match:
                pov_type(match)
                length, height = height, length


            # #'''Calcs'''
            if fab_level == "A":
                pad_margin = 0.7
                hole_margin = 0.25
            elif fab_level == "B":
                pad_margin = 0.6
                hole_margin = 0.20
            elif fab_level == "C":
                pad_margin = 0.5
                hole_margin = 0.15 

            h_lead_span = lead_span / 2
            h_col_span = pitch * (rows - 1) / 2
            h_row_span = pitch * (cols - 1) / 2

            # val definitions
            r_fab = diameter / 2
            h_fab = length              # Vertical_Length
            w_fab = width               # Horizontal_Width
            t_fab = h_fab / 2           # Vertical_Start_Point
            l_fab = w_fab / 2           # Horizontal_Start_Point

            d_silk = s_margin_d + r_fab
            h_silk = s_margin_h + h_fab
            w_silk = s_margin_w + w_fab
            t_silk = h_silk / 2
            l_silk = w_silk / 2

            d_crt = c_margin_d + r_fab
            h_crt = c_margin_h + h_fab
            w_crt = c_margin_w + w_fab
            t_crt = h_crt / 2
            l_crt = w_crt / 2

            ddrill = round(lead_width + hole_margin, 3)
            # ddrill = 0.8                  # Overwrite
            pad_size = round(lead_width + hole_margin + pad_margin, 3)
            # pad_size = 1.6               # Overwrite

            #'''Footprint name, description & tags'''
            kicad_mod = Footprint(footprint_name)
            kicad_mod.setDescription(description)
            tags = description
            kicad_mod.setTags(tags)

            # create pads
            #'''One Hole Components'''
            if "MTGNP" in match or "MTGP" in match:
                kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[0,0], size=[land_size, land_size], drill=hole_size, layers=Pad.LAYERS_THT))

            if "TPCW" in match or "TPRW" in match:
                kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[0, 0], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))

            #'''Two Leads Components'''
            if pins == 2:
                for i in range(1, pins + 1):
                    t_pin_pos = round(-(h_lead_span) + ((i - 1) * lead_span), 3)
                    if i == 1:
                        if match[0] == "CAPPAD" or match[0] == "CAPPRD" or match[0] == "DIOAD" or match[0] == "DIOADV":
                            kicad_mod.append(Pad(number="C", type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                                    at=[t_pin_pos, 0], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                        else:
                            kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                    at=[t_pin_pos, 0], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                    else:
                        if match[0] == "CAPPAD" or match[0] == "CAPPRD" or match[0] == "DIOAD" or match[0] == "DIOADV":
                            kicad_mod.append(Pad(number="A", type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                    at=[t_pin_pos, 0], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                        else:
                            kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                    at=[t_pin_pos, 0], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                    i += 1



            #'''Two Cols Packages (DIP Style)'''
            if "DIP" in match or "DIPS" in match or "OSC" in match:
                for i in range(1, rows + 1):
                    l_pin_pos = round(h_col_span - ((i - 1) * pitch), 3)
                    t_pin_pos = round((h_lead_span), 3)
                    if i == rows: # 1st Pin
                        kicad_mod.append(Pad(number=1+rows-i, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                                at=[-t_pin_pos, l_pin_pos], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                    else:
                        kicad_mod.append(Pad(number=1+rows-i, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                at=[-t_pin_pos, l_pin_pos], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                    i += 1
                for j in range(1, rows + 1):
                    l_pin_pos = round(h_col_span - ((j - 1) * pitch), 3)
                    t_pin_pos = (h_lead_span)
                    kicad_mod.append(Pad(number=0+(rows+j), type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[t_pin_pos, l_pin_pos], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                    j += 1


            #'''One or Mulpiple Rows Packages (SIP, Headers...)'''
            if "HDRV" in match or "HDRRA" in match or "SIP" in match: # only for HDR package
                pin_n = 0
                for c in range(0, cols): #hr = cols / hc = rows
                    for r in range(0, rows):
                        pin_n += 1
                        t_pin_pos = round((pitch * c) - h_row_span, 3)
                        l_pin_pos = round(h_col_span - (pitch * r), 3)
                        if c == 0 and r == 0: # 1st Pin
                            kicad_mod.append(Pad(number=pin_n, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                                    at=[t_pin_pos, l_pin_pos], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                        else:
                            kicad_mod.append(Pad(number=pin_n, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                    at=[t_pin_pos, l_pin_pos], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                        r += 1
                    c += 1
            if "PGA" in match: # only for PGA package
                for c in range(0, cols): #hr = cols / hc = rows
                    pin_n = 0
                    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    pin_l = letters[c]
                    for r in range(0, rows):
                        pin_n += 1
                        t_pin_pos = round((pitch * c) - h_row_span, 3)
                        l_pin_pos = round(-h_col_span + (pitch * r), 3)
                        if c == 0 and r == 0: # 1st Pin
                            kicad_mod.append(Pad(number=pin_l+str(pin_n), type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                                    at=[t_pin_pos, l_pin_pos], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                        else:
                            kicad_mod.append(Pad(number=pin_l+str(pin_n), type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                    at=[t_pin_pos, l_pin_pos], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                        r += 1
                    c += 1



            if "TO" in match and match[2] == "P":
                if height > max(length, width): # only for TO-220 Style package VERTICAL
                    i = 0
                    for i in range(0, pins):
                        t_pin_pos = round(h_row_span - i * pitch, 3)
                        if i == pins-1: # 1st Pin
                            kicad_mod.append(Pad(number=pins-i, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                                at=[t_pin_pos, 0], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                        else:
                            kicad_mod.append(Pad(number=pins-i, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                at=[t_pin_pos, 0], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                        i += 1
                else:
                    i = 0
                    for i in range(0, pins):
                        t_pin_pos =  -(l_fab + 4*margin)
                        l_pin_pos = round(h_row_span - i * pitch, 3)
                        if i == pins-1: # 1st Pin
                            kicad_mod.append(Pad(number=pins-i, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                                at=[t_pin_pos, l_pin_pos], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                        else:
                            kicad_mod.append(Pad(number=pins-i, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                at=[t_pin_pos, l_pin_pos], size=[pad_size, pad_size], drill=ddrill, layers=Pad.LAYERS_THT))
                        i += 1

            # set general values
            text_offset = pitch + max(r_fab, w_fab) / 2 if pitch != 0 else 2.54 + max(w_fab, r_fab) / 2
            kicad_mod.append(Text(type='reference', text='REF**', at=[0, -text_offset], layer='F.SilkS'))
            kicad_mod.append(Text(type='value', text=footprint_name, at=[0, text_offset], layer='F.Fab'))



            if "CAPADV" in match or "CAPPADV" in match or "DIOADV" in match or "FUSADV" in match or "INDADV" in match or "RESADV" in match:
                kicad_mod.append(Circle(center = [h_lead_span, 0], radius = r_fab, layer = 'F.Fab'))
                kicad_mod.append(RectLine(start=[-h_lead_span - s_margin_h, -s_margin_w], end=[h_lead_span + s_margin_h, s_margin_w], layer='F.SilkS'))
                kicad_mod.append(RectLine(start=[-h_lead_span - c_margin_h, -c_margin_w], end=[h_lead_span + c_margin_h, c_margin_w], layer='F.CrtYd'))

            else:
                if r_fab == 0: # For Rect. Footprints
                    kicad_mod.append(RectLine(start=[-t_fab, -l_fab], end=[h_fab + 0 - t_fab, w_fab - l_fab], layer='F.Fab'))
                    kicad_mod.append(RectLine(start=[-t_silk, -l_silk], end=[h_silk + 0 - t_silk, w_silk - l_silk], layer='F.SilkS'))
                    kicad_mod.append(RectLine(start=[-t_crt, -l_crt], end=[h_crt + 0 - t_crt, w_crt - l_crt], layer='F.CrtYd'))

                if r_fab != 0: # For Round Footprints
                    kicad_mod.append(Circle(center = [0, 0], radius = r_fab, layer = 'F.Fab'))
                    kicad_mod.append(Circle(center = [0, 0], radius = d_silk, layer = 'F.SilkS'))
                    kicad_mod.append(Circle(center = [0, 0], radius = d_crt, layer = 'F.CrtYd'))





            # add model
            kicad_mod.append(Model(filename="example.3dshapes/example_footprint.wrl",
                    at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

            #'''OUTPUT'''
            print(f"{footprint_name} -- {description}") # Name

            keys = [
                "lead_span",
                "Lead_Width",
                "Diameter",
                "Length",
                "Width",
                "Height",
                "pitch",
                "Pins",
                "Cols",
                "Rows",
                "Hole_Size",
                "Land_Size",
                "Antipad_Size",
                "Vias",
                "Fab_Level"
                ]
            values = [
                lead_span,
                lead_width,
                diameter,
                length,
                width,
                height,
                pitch,
                pins if pins > 2 else 0, #
                cols if cols > 2 else 0, #
                rows if rows > 2 else 0, #
                hole_size,
                land_size,
                antipad_size,
                vias,
                fab_level
                ]
            comments = [
                "Lead Spacing/Span (Distance Between Two Leads or Columns)",
                "Maximum Lead Width (or Component Lead Diameter)",
                "Body Diameter (for Round Component Body)",
                "Body Length (for Horizontal Mounting)",
                "Body Thickness (for Rectangular Component Body)",
                "Height (for Vertically Mounted Components)",
                "Pitch (for Components With More Than Two Leads)",
                "Pin Quantity (for Components with More Than Two Leads)",
                "Pin per Columns (Number of Pins Per Columns)",
                "Number of Rows",
                "Hole Size",
                "Land Size",
                "Anti-Pad Size",
                "Number of Vias",
                "Fabrication Complexity Level"
                ]

            zlist = zip(keys, values, comments)
            for key, val, com in zlist:
                if key != "Fab_Level" and val != 0:
                    if key == "Pins" or key == "Rows" or key == "Cols" or key == "Vias":
                        dprint(f"   {key}: {val}, {com}")
                    else:
                        dprint(f"   {key}: {val}mm ({round(mil(val))}mil), {com}")

            od = f"D:{diameter} x " if diameter > 0 else ""
            ol = f"L:{length} x " if length > 0 else ""
            ow = f"W:{width} x " if width > 0 else ""
            oz = f"H:{height}" if height > 0 else ""
            output = f"IC Volume: {od}{ol}{ow}{oz}"
            dprint(output)

            # output kicad model
            file_handler = KicadFileHandler(kicad_mod)
            file_handler.writeFile("Output/"+footprint_name+".kicad_mod")

print("\nOutput OK")