import ofjustpy as oj
from tailwind_tags import *
import justpy as jp


def launcher(request):
    wp = jp.WebPage()
    stubs = [oj.Circle_("mycircle", text="myc"),

             oj.Span_("myspan", text="span text"),
             oj.A_("myA", text="mytext", href="myurl"),
             oj.P_("myP", text="my looooongins para")
             ]
    for stub in stubs:
        dbref = oj.Halign_(stub)(wp)
    return wp


# wp = jp.WebPage()
# circle = circleStub(wp)
# print(circle.twsty_tags)
#wp = launcher(None)
app = jp.app
jp.justpy(launcher, start_server=False)
