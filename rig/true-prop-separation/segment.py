#!/usr/bin/env python3
"""True prop separation for Cape Jones PURPLE LOT boards (v2).

Method (NOT box cuts): every prop is cut along the art's own edges.
  * grabCut props (cars, Jones): a hand-measured polygon traces the prop
    ~5px outside its true edge; grabCut segments the true silhouette
    inside it; the result is CLAMPED to the polygon dilated 6-8px, so it
    can never leak into the background the way v1's first pass did.
    Sure-background seeds pin the asphalt below the tires and the fence
    above the rooflines.
  * traced props (lamps, stop sign): thin/geometric objects whose edges
    are straight lines and ellipses. The mask IS the traced outline
    (pole rect, head ellipse, sign octagon), feathered 1px. No grabCut,
    no glow: the lamp glow is a light layer, not part of the prop.
  * Masks are saved as full-frame RGBA — alpha follows the silhouette,
    never a box. Background underneath is rebuilt by complete_bg.py.

Source art: production/2d-parking-lot/boards/cj-pl-0N.png (the original
drawings) and rig/plate-sodium.png (the flat V2 plate, itself built from
board 01). There are no hidden layers in the boards — they are flat RGB
drawings — so "re-sliced from the board art" means edge-following
segmentation of the board art itself, not recovery of layers that never
existed. Overlapping car rows cannot be split car-by-car: the cars occlude
each other and their shared edges do not exist in the drawing, so each row
is ONE cluster layer whose outer silhouette follows the cars' real edges.
"""
import os, json, math
import numpy as np
import cv2
from PIL import Image

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
BOARDS = f"{WD}/repo/production/2d-parking-lot/boards"
OUT = f"{WD}/true-sep"

def ellipse_poly(cx, cy, rx, ry, n=24):
    return [(int(cx + rx * math.cos(2 * math.pi * i / n)),
             int(cy + ry * math.sin(2 * math.pi * i / n))) for i in range(n)]

# Shared plate/board-01 prop specs (plate == board 01 minus Jones).
PLATE_PROPS = {
  "cars_left_row": dict(method="grabcut", clamp=3,
    poly=[(0,568),(25,555),(90,544),(180,539),(260,536),(340,534),(400,539),(422,552),(422,636),(0,636)],
    seeds_fg=[(60,590,12),(180,590,12),(300,585,12),(390,590,10)],
    seeds_bg=[(100,522,8),(300,518,8),(100,648,10),(300,648,10)], erode=10),
  "blue_car_mid": dict(method="grabcut", clamp=3,
    # Hood top edge measured from the 3x zoom: leading edge y572@435,
    # windshield base y545@505, roof y537@600. The white car behind the
    # roof (y520-545, x590-690) is NOT the blue car: bg seeds pin it out.
    poly=[(435,572),(450,566),(475,556),(505,545),(545,538),(600,537),(640,544),(663,560),(668,595),(665,610),(655,614),(460,614),(442,606)],
    seeds_fg=[(500,590,14),(580,585,14),(640,600,10),(520,605,10)],
    seeds_bg=[(620,528,8),(665,525,6),(460,548,10),(480,540,6),(550,630,10),(420,600,8)], erode=10),
  "cars_right_row": dict(method="grabcut", clamp=3,
    poly=[(1225,562),(1290,542),(1380,533),(1480,529),(1580,526),(1680,529),(1755,542),(1775,562),(1775,636),(1225,636)],
    seeds_fg=[(1300,590,12),(1450,590,12),(1600,590,14),(1720,595,12)],
    seeds_bg=[(1400,514,8),(1650,510,8),(1400,648,10),(1650,648,10),(1758,580,4),(1734,635,8)], erode=10),
  "stop_sign": dict(method="traced", shapes=[
    {"poly": [(788,490),(784,502),(773,506),(762,502),(758,490),(762,478),(773,474),(784,478)]},
    {"poly": [(768,500),(785,500),(785,576),(768,576)]},
    {"poly": ellipse_poly(776, 576, 11, 4, 12)}]),
  "street_lamp_right": dict(method="traced", shapes=[
    # CORRECTED 2026-11-23 (pixel profiles, not the eyeballed zoom): the
    # pole is at x1752-1767, NOT x1727-1738 — the first trace caught sky
    # and left the real pole standing in the background. Brightest-pixel
    # trace: lit edge x1756, y280-560; base widens left below y613.
    {"poly": ellipse_poly(1666, 205, 46, 13)},
    {"poly": [(1688,196),(1720,186),(1756,180),(1758,196),(1725,202),(1692,208)]},
    {"poly": [(1752,182),(1767,182),(1767,615),(1752,615)]},
    {"poly": [(1719,612),(1748,612),(1748,662),(1719,662)]}]),
  "street_lamp_far": dict(method="traced", shapes=[
    {"poly": ellipse_poly(606, 386, 20, 8)},
    {"poly": [(588,384),(600,378),(614,380),(612,390),(596,392)]},
    {"poly": [(584,388),(594,388),(594,540),(584,540)]}]),
}

JONES_01 = dict(method="grabcut", clamp=3,
  # Measured from the board (pixel profiles, not the downscaled preview):
  # head top y497, cowl x1000-1055; shoulders flare only BELOW y560;
  # cape left edge x965@600 -> 944@700, right edge x1080@600 -> 1075@700;
  # cape tips end y745; boots end y776. Above y560 the polygon stays
  # narrow (head+neck only) so grabCut cannot eat the fence behind the
  # shoulders; below the boots bg seeds pin the ground shadow out.
  poly=[(992,505),(1000,497),(1046,497),(1056,508),(1062,535),(1068,560),(1080,600),(1072,650),(1078,700),(1070,745),(1058,762),(1046,774),(1016,774),(1010,758),(1002,774),(972,774),(962,760),(948,745),(942,700),(950,650),(962,600),(968,570),(978,545),(986,520)],
  seeds_fg=[(1000,650,15),(1000,740,12),(1015,515,10),(1015,545,8),(955,680,8),(1065,680,8)],
  seeds_bg=[(920,700,8),(1100,700,8),(1015,482,8),(955,768,6),(1062,768,6),(1009,768,5),(960,792,8),(1010,795,8),(1060,792,8)], erode=6)

SPECS = {
  "plate": {
    "src": f"{WD}/rig/plate-sodium.png",
    "props": dict(PLATE_PROPS),
    # make_plates.py v3 painted Jones out with a BOX (x920-1120, y478-835):
    # horizontal interp + mirrored asphalt. The mirror dragged the blue
    # car's rear into the box (ghost car sliced by the box edge at x1120)
    # and left a visible rectangle. Rebuild the whole box, not just Jones.
    "rebuild_rects": [(895, 453, 1145, 860)],
  },
  "cj-pl-01": {
    "src": f"{BOARDS}/cj-pl-01.png",
    "props": dict(PLATE_PROPS, jones=JONES_01),
    "rebuild_rects": [],
  },
}

# ---------------------------------------------------------------- boards 02-07
# Each board is a DIFFERENT drawing: Jones is large in the foreground on
# 02/03/04/06/07, the cars are small background rows, the lamps sit in
# different places, 05 has no cars at all. No coordinates are reused from
# board 01 or the plate. Polygons below were measured from the board art:
# white-suit extents come from per-row pixel profiles (probe_boards.py),
# lamp geometry from 1:1 crops of the lamp areas, cape/car rooflines from
# the full-frame own-eyes view + mask-qa iteration. grabCut refines the
# true edge inside the polygon; the clamp (3px) keeps it from leaking.
def _gc(poly, fg, bg, erode=6):
    return dict(method="grabcut", clamp=3, poly=poly,
                seeds_fg=fg, seeds_bg=bg, erode=erode)

JONES_02 = _gc(
  # Cape top edge is a WAVY field of thin folds, measured from the black
  # outline (first lum<6 crossing per column, -5px): the tongues crest at
  # y81 (x510) and y86 (x185) and dip to y300 (x910). A smooth polygon
  # cut the tongues off by up to 100px. erode=2 so the thin tongues keep
  # a sure-FG core; fg seeds sit ON the tongues, bg seeds in the sky
  # just above the edge (never inside a tongue).
  [(110,134),(135,113),(160,95),(185,81),(210,103),(235,100),(260,98),
   (285,99),(310,102),(335,107),(360,114),(385,124),(410,137),(435,153),
   (460,122),(485,140),(510,76),(535,92),(560,113),(585,137),(610,117),
   (635,118),(660,121),(685,129),(710,139),(735,155),(760,183),(785,225),
   (810,257),(835,275),(860,286),(885,293),(910,295),(935,289),(960,286),
   (985,289),(1010,288),(1035,277),(1060,274),(1085,279),(1110,287),
   (1130,178),(1215,103),(1285,118),(1300,220),(1290,320),(1330,400),
   (1420,430),(1490,520),(1545,700),(1585,900),(1575,1152),(990,1152),
   (985,1000),(1000,880),(880,895),(700,900),(560,880),(420,830),(330,740),
   (250,620),(200,480),(160,330),(115,200)],
  fg=[(1100,700,20),(1250,550,15),(900,850,15),(1200,1000,20),(500,450,25),(300,550,20),
      (200,110,8),(300,125,8),(500,110,8),(600,140,8),(700,160,8),(800,250,8),
      (1150,165,10),(1170,150,10),(1200,145,10),(1570,900,8),(1575,950,8)],
  bg=[(500,60,10),(700,110,10),(900,250,10),(1500,300,10),(900,1050,8),(1600,900,10),(100,900,10),(700,1000,10),
      (1150,130,8),(1200,110,8)],
  erode=2)
JONES_03 = _gc(
  # Cape left (hanging) edge measured from the outline scan: it runs
  # (497,550)->(574,1050), much further left than the first draft.
  # Cape top edge (shoulder->tip) is wavy y450-530; cape is solid black
  # here so grabCut refines well from a smooth polygon + edge seeds.
  [(300,55),(390,80),(420,180),(460,300),(520,400),(600,411),(650,415),(680,431),
   (700,446),(730,467),(745,465),(738,360),(740,280),(745,200),(800,185),(880,190),(945,230),
   (950,330),(940,430),(1000,470),(1150,500),(1400,520),(1650,560),(1905,665),
   (1880,800),(1800,950),(1750,1080),(1700,1152),(660,1152),(574,1050),
   (549,1000),(529,950),(513,900),(450,850),(457,800),(489,750),(489,700),
   (483,650),(459,600),(497,550),(370,460),(320,400),(320,300),(290,180),(265,90)],
  fg=[(850,700,20),(1000,900,20),(1500,750,25),(700,900,15),(350,250,12),(900,300,12),
      (1400,550,12),(1700,550,12),(550,700,12),(305,200,10),(300,250,10),
      (680,440,15),(700,420,12),(620,430,10),(370,420,12),(380,470,10)],
  bg=[(600,300,12),(1200,300,10),(300,600,10),(1950,900,10),(100,1000,10),
      (1400,420,10),(1700,470,10),(250,180,10),(270,200,8),(275,280,8),(320,450,8)],
  erode=4)
JONES_04 = _gc(
  # Face top-left + cape bridge + hand centre + sleeve bottom-left. The
  # polygon DIPS into the notch between the face and the hand (cape top
  # edge y~380-450): the blurred background above that edge is OUTSIDE
  # the polygon, so grabCut can never pull it into the Jones layer.
  # Cape top edge measured: y~337 for x420-620 (flat). The notch edge
  # must run along it, not 40px below it.
  [(0,0),(430,0),(435,200),(410,330),(520,330),(620,335),(680,400),(800,380),
   (950,250),(1080,180),(1250,190),(1400,330),(1450,520),(1430,720),
   (1360,900),(1260,1050),(1150,1152),(0,1152)],
  fg=[(200,250,20),(1100,600,25),(300,800,25),(1000,950,20),(500,420,12)],
  bg=[(600,200,15),(750,150,12),(1500,300,10),(1600,900,10),(900,150,10)],
  erode=6)
JONES_05 = _gc(
  [(885,240),(960,280),(965,380),(980,470),(1000,420),(1010,380),(1030,370),
   (1075,375),(1085,420),(1095,470),(1120,510),(1180,560),(1300,620),
   (1400,690),(1350,760),(1240,800),(1150,820),(1160,900),(1150,945),
   (1080,945),(1060,880),(1040,820),(1010,880),(1000,945),(920,945),
   (872,940),(872,880),(920,810),(850,780),(700,720),(585,610),(650,575),(750,550),
   (850,510),(900,478),(920,400),(880,320),(878,270)],
  fg=[(1010,700,18),(1100,850,15),(950,850,12),(950,350,10),(800,650,20),(1250,650,20),
      (900,300,10),(895,280,8),(900,900,12),(880,920,10),(1050,930,12),(1100,930,10),
      (900,938,8),(880,935,8),(950,938,8),(1020,940,8),(1080,940,8),(1130,938,8)],
  bg=[(1030,870,8),(700,300,10),(1500,900,10),(500,900,10),(1200,300,10),(860,300,8)],
  erode=5)
JONES_06 = _gc(
  [(1190,95),(1260,100),(1295,160),(1295,300),(1300,380),(1350,395),
   (1400,390),(1450,393),(1550,400),(1600,485),(1700,620),(1850,625),(2048,625),(2048,1152),(990,1152),
   (975,1100),(830,1050),(805,1000),(820,900),(825,800),(870,750),(935,750),(928,650),(930,600),
   (935,550),(940,500),(945,472),(995,420),(1020,445),(1050,460),(1070,430),(1080,340),(1078,280),
   (1085,210),(1100,150),(1150,110)],
  fg=[(1200,700,20),(1250,1000,18),(1700,800,25),(1000,800,15),(1180,250,12),
      (1900,900,20),(870,850,12),(860,950,12),(900,1000,10),
      (1000,440,10),(1400,405,10),(940,550,10),(935,650,10)],
  bg=[(900,300,10),(900,1100,10),(1600,300,10),(700,600,10),(1400,1100,10),
      (1700,580,10),(1900,580,10),(1600,450,8),(1000,400,8),(1400,370,8)],
  erode=4)
JONES_07 = _gc(
  # Cape left edge measured from the outline scan (x per row y550-1150):
  # it runs diagonally (624,600)->(288,1150), NOT the steep line first
  # drawn. Shoulder top edge y~400 for x700-800.
  # RIM: the cape's bright purple rim-light sits ~25-35px LEFT of the
  # black outline (rim peak vs outline, y700-1050). The left-edge
  # vertices below are rim-peak-8, not outline-5, so the rim stays with
  # Jones instead of ghosting in the background.
  [(1010,60),(1150,80),(1210,150),(1230,350),(1180,480),(1250,550),
   (1250,900),(1300,1000),(1360,1060),(1420,1110),(1570,1100),(1660,1152),(288,1152),
   (280,1100),(296,1050),(314,1000),(334,950),(355,900),(379,850),
   (412,800),(442,750),(469,700),(553,650),(624,600),(700,400),(750,398),
   (800,398),(820,300),(850,180),(900,100)],
  fg=[(950,800,20),(1100,950,18),(450,900,25),(1000,300,15),(1150,600,12),
      (370,900,8),(430,800,8),(1500,1120,12),(1600,1130,10)],
  bg=[(600,300,12),(1500,500,10),(1450,900,10),(150,500,10),(700,1100,10),
      (250,900,8),(320,800,8),(1700,1120,8)],
  erode=6)

def _lamp(shapes):
    return dict(method="traced", shapes=[{"poly": p} for p in shapes])

SPECS.update({
  "cj-pl-02": {
    "src": f"{BOARDS}/cj-pl-02.png",
    "props": {
      "cars_left_row": _gc([(0,575),(120,568),(260,573),(368,582),(368,682),(0,682)],
        fg=[(100,620,12),(250,620,12)], bg=[(100,548,8),(250,550,8),(100,700,8)], erode=8),
      "cars_right_row": _gc([(1468,585),(1600,572),(1800,574),(2048,580),(2048,690),(1468,690)],
        fg=[(1600,625,12),(1850,625,12),(2000,625,10)], bg=[(1600,545,8),(1850,545,8),(1600,710,8)], erode=8),
      # Lamp head is cut by the frame top (bright y0 x1569-1629); pole
      # x1430-1450 runs to y665 where Jones's arm covers it.
      "street_lamp_right": _lamp([ellipse_poly(1570, 10, 90, 30),
        [(1438,0),(1560,0),(1560,30),(1438,32)],
        [(1430,0),(1450,0),(1450,665),(1430,665)]]),
      "jones": JONES_02,
    },
    "rebuild_rects": [],
  },
  "cj-pl-03": {
    "src": f"{BOARDS}/cj-pl-03.png",
    "props": {
      "cars_left_row": _gc([(0,552),(90,518),(230,503),(400,518),(480,542),(460,650),(485,750),(455,800),(470,832),(0,832)],
        fg=[(150,650,15),(350,650,15),(200,750,12)], bg=[(150,490,8),(350,490,8),(150,850,8)], erode=8),
      # Right row is mostly BEHIND the cape: only a thin band of roofs
      # shows above the cape's wavy top edge, plus the full row right of
      # the cape tip (x1905). The polygon's bottom edge IS the cape edge;
      # bg seeds below it pin the cape out of the cars layer. Thin band,
      # so erode=2.
      "cars_right_row": _gc([(1150,508),(1400,503),(1700,503),(1905,515),(2048,520),(2048,662),(1905,662),(1905,610),(1700,525),(1400,550),(1150,555)],
        fg=[(1300,525,8),(1600,515,8),(1950,580,12),(2000,600,10)], bg=[(1300,490,6),(1600,490,6),(1300,600,10),(1600,580,10),(1800,600,10),(1300,680,8)], erode=2),
      "street_lamp_far": _lamp([ellipse_poly(1608, 372, 28, 10),
        [(1600,380),(1616,380),(1616,480),(1600,480)]]),
      # Head ellipse + arm + pole (pole ends y565 where the cape covers
      # it) + concrete pedestal/plinth at the base.
      "street_lamp_right": _lamp([ellipse_poly(1620, 72, 72, 26),
        [(1680,58),(1755,48),(1755,82),(1685,92)],
        [(1742,55),(1762,55),(1762,565),(1742,565)],
        [(1715,625),(1760,625),(1760,715),(1715,715)],
        [(1695,710),(1785,710),(1785,745),(1695,745)]]),
      "jones": JONES_03,
    },
    "rebuild_rects": [],
  },
  "cj-pl-04": {
    "src": f"{BOARDS}/cj-pl-04.png",
    "props": {
      # Blurred background cars (right). The hand covers x<1455 in this
      # band, so the polygon starts at x1455 — the first draft started at
      # x1300 and grabCut's sure-FG swallowed a chunk of the hand.
      "cars_right_row": _gc([(1455,458),(1600,438),(1750,442),(2048,452),(2048,820),(1455,820)],
        fg=[(1600,600,15),(1800,600,15),(1950,700,12)], bg=[(1600,420,8),(1800,420,8),(1600,840,8)], erode=10),
      # Three blurred lamps: two tall (heads + poles) + one small right.
      "street_lamp_far": _lamp([ellipse_poly(820, 125, 65, 30),
        [(808,150),(832,150),(832,460),(808,460)],
        ellipse_poly(1640, 150, 70, 35),
        [(1628,180),(1652,180),(1652,450),(1628,450)],
        ellipse_poly(1945, 282, 42, 30),
        [(1937,305),(1953,305),(1953,430),(1937,430)]]),
      "jones": JONES_04,
    },
    "rebuild_rects": [],
  },
  "cj-pl-05": {
    "src": f"{BOARDS}/cj-pl-05.png",
    "props": {
      # No cars on this board (hero wide, empty lot).
      # Broken lamp: cracked head + two cross-arms + pole + base. The
      # thin crack shards below the head are light effects, left in the
      # background (a polygon around them would carry sky).
      "street_lamp_broken": _lamp([
        [(1448,298),(1598,318),(1602,348),(1452,330)],
        [(1585,320),(1645,345),(1640,360),(1580,335)],
        [(1615,375),(1660,400),(1650,415),(1610,390)],
        [(1605,320),(1625,320),(1625,700),(1605,700)],
        [(1598,680),(1632,680),(1632,720),(1598,720)]]),
      "jones": JONES_05,
    },
    "rebuild_rects": [],
  },
  "cj-pl-06": {
    "src": f"{BOARDS}/cj-pl-06.png",
    "props": {
      "cars_left_row": _gc([(0,602),(200,598),(450,612),(800,628),(800,852),(0,852)],
        fg=[(150,720,15),(400,720,15),(650,720,12)], bg=[(150,580,8),(400,580,8),(150,870,8)], erode=8),
      "cars_right_row": _gc([(1640,618),(1850,612),(2048,618),(2048,852),(1640,852)],
        fg=[(1750,730,12),(1950,730,12)], bg=[(1750,590,8),(1950,590,8),(1750,870,8)], erode=8),
      # Broken/leaning lamp: head + bent arm + upper stub, a real BREAK
      # GAP y482-490, lower pole + concrete base. The gap stays a gap.
      "street_lamp_broken": _lamp([
        [(315,262),(455,255),(460,290),(320,295)],
        [(318,282),(238,348),(222,362),(305,298)],
        [(188,318),(232,322),(228,480),(205,482)],
        [(232,490),(262,492),(300,820),(268,825)],
        [(258,800),(338,800),(338,860),(258,860)]]),
      "jones": JONES_06,
    },
    "rebuild_rects": [],
  },
  "cj-pl-07": {
    "src": f"{BOARDS}/cj-pl-07.png",
    "props": {
      "cars_left_row": _gc([(0,236),(190,230),(380,236),(380,330),(0,330)],
        fg=[(100,280,10),(280,280,10)], bg=[(100,215,8),(280,215,8),(100,345,8)], erode=6),
      "cars_centre": _gc([(1235,300),(1280,282),(1360,278),(1420,290),(1420,400),(1235,400)],
        fg=[(1320,340,10)], bg=[(1250,285,6),(1400,285,6),(1320,415,6)], erode=6),
      "cars_right_row": _gc([(1740,302),(1900,298),(2048,302),(2048,520),(1740,520)],
        fg=[(1850,400,12),(2000,400,10)], bg=[(1850,280,8),(2000,280,8),(1850,540,8)], erode=8),
      # Dumpsters + barriers as FOUR tight single-object props. The first
      # draft used one cluster polygon over the whole group and grabCut
      # swallowed the fence/wall between the objects (91k px, most of it
      # background). If any of these four still pulls background, drop
      # that one (static set dressing) rather than faking it.
      "dumpsters": _gc([(495,212),(655,208),(660,332),(495,332)],
        fg=[(550,270,12),(620,270,10)], bg=[(550,195,8),(620,195,8),(550,345,8)], erode=6),
      "dumpster_small": _gc([(230,292),(330,292),(330,400),(230,400)],
        fg=[(280,350,10)], bg=[(280,275,8),(280,415,8)], erode=6),
      "barriers_left": _gc([(0,340),(200,340),(200,420),(0,420)],
        fg=[(100,380,12)], bg=[(100,325,8),(100,435,8)], erode=6),
      "barriers_centre": _gc([(330,330),(560,330),(560,410),(330,410)],
        fg=[(400,370,12),(500,370,10)], bg=[(400,315,8),(500,315,8),(400,425,8)], erode=6),
      # Broken lamp: big cracked head (tilted) + stem + floating broken
      # fragment + jagged-top stub at the right frame edge.
      "street_lamp_broken": _lamp([
        [(1485,60),(1755,35),(1850,175),(1760,335),(1490,185)],
        [(1800,300),(1860,330),(1875,385),(1830,395)],
        [(1820,405),(1865,400),(1875,455),(1830,460)],
        [(1820,530),(1832,470),(1850,505),(1868,462),(1888,500),(1890,1152),(1818,1152)]]),
      "jones": JONES_07,
    },
    "rebuild_rects": [],
  },
})

# ---------------------------------------------------------------- helpers
def grabcut_poly(img_bgr, spec):
    poly = np.array(spec["poly"], dtype=np.int32)
    x0, y0 = max(0, poly[:, 0].min() - 20), max(0, poly[:, 1].min() - 20)
    x1, y1 = min(img_bgr.shape[1], poly[:, 0].max() + 20), min(img_bgr.shape[0], poly[:, 1].max() + 20)
    crop = img_bgr[y0:y1, x0:x1]
    ch, cw = crop.shape[:2]
    lp = poly - np.array([x0, y0])
    mask = np.full((ch, cw), cv2.GC_PR_BGD, np.uint8)
    cv2.fillPoly(mask, [lp], cv2.GC_PR_FGD)
    pm = np.zeros((ch, cw), np.uint8)
    cv2.fillPoly(pm, [lp], 255)
    e = spec.get("erode", 8)
    er = cv2.erode(pm, np.ones((2 * e + 1, 2 * e + 1), np.uint8))
    mask[er > 0] = cv2.GC_FGD
    for (x, y, r) in spec.get("seeds_fg", []):
        cv2.circle(mask, (x - x0, y - y0), r, cv2.GC_FGD, -1)
    for (x, y, r) in spec.get("seeds_bg", []):
        cv2.circle(mask, (x - x0, y - y0), r, cv2.GC_BGD, -1)
    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(crop, mask, None, bgd, fgd, 5, cv2.GC_INIT_WITH_MASK)
    fg_crop = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    fg = np.zeros(img_bgr.shape[:2], np.uint8)
    fg[y0:y1, x0:x1] = fg_crop
    # clamp: never more than `clamp` px outside the traced polygon
    cl = spec.get("clamp", 8)
    pm_full = np.zeros(img_bgr.shape[:2], np.uint8)
    cv2.fillPoly(pm_full, [poly], 255)
    allowed = cv2.dilate(pm_full, np.ones((2 * cl + 1, 2 * cl + 1), np.uint8))
    fg[allowed == 0] = 0
    return fg

def traced_mask(img_shape, spec):
    m = np.zeros(img_shape[:2], np.uint8)
    for sh in spec["shapes"]:
        cv2.fillPoly(m, [np.array(sh["poly"], dtype=np.int32)], 255)
    return m

def refine(fg):
    h, w = fg.shape
    ff = fg.copy()
    # Hole-fill: flood from a BORDER pixel that is actually background.
    # (0,0) is NOT safe: on boards where Jones touches the top-left
    # corner (04) the seed lands inside the figure and the fill inverts
    # the whole mask. Scan the border for a real background seed first.
    seed = None
    for (y, x) in list(zip([0]*w, range(w))) + list(zip([h-1]*w, range(w))) \
            + list(zip(range(h), [0]*h)) + list(zip(range(h), [w-1]*h)):
        if fg[y, x] == 0:
            seed = (x, y)
            break
    if seed is not None:
        flood = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(ff, flood, seed, 128)
        fg[ff == 0] = 255
    n, lab, stats, _ = cv2.connectedComponentsWithStats((fg > 0).astype(np.uint8), 8)
    if n > 1:
        areas = stats[1:, cv2.CC_STAT_AREA]
        biggest = 1 + int(np.argmax(areas))
        keep = np.zeros_like(fg)
        for i in range(1, n):
            if i == biggest or stats[i, cv2.CC_STAT_AREA] >= 0.005 * stats[biggest, cv2.CC_STAT_AREA]:
                keep[lab == i] = 255
        fg = keep
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    return fg

def soft_alpha(fg):
    a = cv2.GaussianBlur(fg.astype(np.float32), (0, 0), 0.8)
    return np.clip(a, 0, 255).astype(np.uint8)

def run_board(name, spec):
    img = cv2.imread(spec["src"])
    assert img is not None, spec["src"]
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    outdir = os.path.join(OUT, "boards", name) if name.startswith("cj-") else os.path.join(OUT, name)
    layers_dir = os.path.join(outdir, "layers")
    os.makedirs(layers_dir, exist_ok=True)
    report = {"board": name, "src": spec["src"], "props": {}}
    qa = rgb.copy()
    for pname, pspec in spec["props"].items():
        if pspec["method"] == "grabcut":
            fg = grabcut_poly(img, pspec)
            fg = refine(fg)
        else:
            fg = traced_mask(img.shape, pspec)
        alpha = soft_alpha(fg)
        rgba = np.dstack([rgb, alpha])
        Image.fromarray(rgba, "RGBA").save(os.path.join(layers_dir, pname + ".png"))
        ys, xs = np.where(fg > 0)
        report["props"][pname] = {
            "method": pspec["method"],
            "pixels": int((fg > 0).sum()),
            "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
        }
        cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        overlay = qa.copy()
        cv2.drawContours(overlay, cnts, -1, (255, 0, 255), 2)
        cv2.fillPoly(overlay, cnts, (255, 0, 255))
        qa = cv2.addWeighted(overlay, 0.30, qa, 0.70, 0)
        cv2.drawContours(qa, cnts, -1, (255, 0, 255), 2)
        print(f"  {name}/{pname}: {(fg>0).sum()} px bbox {report['props'][pname]['bbox']}", flush=True)
    Image.fromarray(qa).save(os.path.join(outdir, "mask-qa.png"))
    with open(os.path.join(outdir, "masks.json"), "w") as f:
        json.dump(report, f, indent=2)
    return report

if __name__ == "__main__":
    import sys
    targets = sys.argv[1:] or ["plate", "cj-pl-01"]
    for t in targets:
        print("==", t, flush=True)
        run_board(t, SPECS[t])
