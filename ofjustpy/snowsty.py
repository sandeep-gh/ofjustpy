# https://www.creative-tim.com/learning-lab/tailwind-starter-kit/documentation/css/typography/headings
from tailwind_tags import *

h1 = [xl3, lh.normal,  lh.normal, mr/st/0, mr/sb/2, text/gray/6]

h2 = [xl, lh.normal,  lh.normal, mr/st/0, mr /
      sb/2]  # "prose", "prose-2xl"

h3 = [fz.lg, lh.normal,  lh.normal, mr/st/0, mr /
      sb/2]  # "prose", "prose-2xl"

para = [base, fw.light, relaxed, mr/st/0, mr/sb/4, ]


container = [mr/x/auto, container]
# ?? para.mr.sb = 5
# type = "button"
button = [bg/gray/1, fc/gray/6,  mr/sr/1, mr/sb/1, pd/x/4, pd/y/2, bold, Outline.n, bsw._, bsw.sm,
          bdr.md, bold,  "uppercase ease-linear transition-all duration-150 outline-none focus:outline-none", *hover(noop/bsw.md, bg/gray/2)]
title_box = [db.f, jc.center]
title_text = [xl6, fw.bold,  mr/st/0, mr/sb/2, text/gray/8]

heading_box = [db.f, jc.around]
heading_text = [*h1, fw.bold]
subheading_box = [db.f, jc.around]
subheading_text = [*h2, fw.bold, bsw.sm,
                   sw/slate/"500/50"]  # "prose", "prose-2xl"

subsubheading_text = [*h3, fw.medium, bsw.xl,
                      sw/slate/"500/80"]  # "prose", "prose-2xl"

spacing = [pd/1]
centering_div = [db.f, jc.center]
span = [base, fw.light, relaxed, *spacing, ]
form = [db.f, jc.center]
theme = []  # default background, font, border, etc stuff
P = []
A = []
stackv = [db.f, flx.col]

# ================ copied from fancy str--using empty ================
_ = dbr = Dict()
_.banner = []
_.result = [hidden/""]

border_style = []

icon_button = [bg/gray/1, ta.center,
               pd/1, bsw.md,  *spacing,  *hover(bg/gray/2)]


theme = []

heading = heading_box
heading2 = subheading_box
heading_span = heading_text
heading2_span = subheading_text
title_banner = [
    db.f, jc.center, *spacing]


title_span = [bdr.md, fc/gray/6, fz.xl, pd/2]
span = [*theme, *spacing, db.f, ai.center]
prose = [*spacing, fc/gray/6, prse.lg]  # TODO:use some other name than prose
#prose = [fc/gray/6, "prose", "prose-2xl"]

divbutton = [db.f, jc.center]
# button = [fz.xl, bg/gray/2,  fc/gray/6, ta.center, bt.bd,
#           bdr.md,   pd/1, bsw.md, mr/2, op.c, hover(bg/gray/4)]

expansion_item = [mr/st/0, bg/gray/2, bsw.sm]

inputJbutton = [pd/4, bg/gray/1, flex, jc.center, * border_style]
select = [fz.sm, mr/x/"2", bg/"inherit"

          ]
selectwbanner = [bt.bd, bdr.md, bd/gray/1, pd/1, mr/x/2]

infocard = [mr/4]
#[db.f, flx.col, bg/pink/1]

barpanel = [mr/1]

slider = [H/1, bg/gray/9, bg/opacity/5,
          db.fi, ji.center, mr/1, ]
circle = [W/6, H/6, bg/gray /
          7, fc/pink/2, bdr.full, mr/2, *hover(noop/bds.double, noop/bt.bd, bg/gray/1, bd/gray/2)]  # bg/gray/5

expansion_item = [mr/1, bg/gray/2]

textarea = [fz.sm, fw.bold, fc/gray/6, bg/gray/1, opacity/80,
            fw.light,  ta.center, *spacing, W/"full", H/"full"]

textinput = [db.f, jc.center, bt.bd, bdr.md, bd/gray/1]
input = [bg/gray/1, opacity/80]
stackW = [db.f, flx.wrap, jc.center, ]

cell = [fc/gray/6, fz.xl, pd/1, bg/gray/2]

left_cell = [*cell, ta.right, W/"1/3"]
right_cell = [*cell, ta.left, W/"1/3"]
eq_cell = [*cell, ta.center, op.c]

option = []
label = []


def stackG(num_cols, num_rows):
    return [db.g,  gap/1, G/cols/f'{num_cols}', G/rows/f'{num_rows}', gf.row]


def get_color_tag(colorname):
    return globals()[colorname]


def build_classes(*args):
    return tstr(*args)


td = [bt.bd, pd/2, ta.center]
tr = [[bg/gray/2, fc/gray/6],
      [bg/pink/1, fc/gray/6]]  # for odd/even row  # 'text-gray-600'

tbl = [fz.sm, 'table-auto',  W/full, "table-fixed",  "overflow-auto",
       "overflow-x-auto"]  # TODO: incorporate into twtags

expansion_container = [mr/st/8, bg/gray/1, shdw.sm, fz.lg]


def halign(align="center"):
    """
    align the contents : options are start, end, center, between, evenly, around
    """
    return [db.f, getattr(jc, align)]
