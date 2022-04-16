import ofjustpy as oj
from tailwind_tags import *
import justpy as jp
from tailwind_tags import *


def launcher(request):
    wp = jp.WebPage()

    def on_btn_click(dbref, msg):
        print("circle clicked", dbref.text, msg.value)
        pass

    def stubs():
        for _ in [oj.Circle_("mycircle", text="myc").event_handle(oj.click, on_btn_click),

                  oj.Span_("myspan", text="span text"),
                  oj.A_("myA", text="myurl", href="myurl"),
                  oj.P_("myP", text="my looooongins para"),
                  oj.SubsubheadingBanner_(
                      "ssb", "a smaller banner", pcp=[bg/pink/100]),
                  oj.WithBanner_("labeled", "mybtn",
                                 oj.P_("mypara", text="hello heloo ")),
                  oj.Button_("mybtn", value="myval",
                             text="Click me ", pcp=[bg/blue/100/50]).event_handle(oj.click, on_btn_click)
                  ]:
            yield _

    mystackv = oj.Halign_(oj.StackV_(
        "mystackv", cgens=[oj.Halign_(stub) for stub in stubs()]))
    mystackh = oj.Halign_(oj.StackH_(
        "mystackh", cgens=[oj.Halign_(stub) for stub in stubs()]))

    mystackw = oj.Halign_(oj.StackW_(
        "mystackh", cgens=[oj.Halign_(stub) for stub in stubs()]))

    mystackg = oj.Halign_(oj.StackG_(
        "mystackh", num_rows=3, num_cols=3,  cgens=[oj.Halign_(stub) for stub in stubs()]))
    mystackh(wp)
    mystackv(wp)
    # mystackw(wp)
    # mystackg(wp)
    oj.Subsection_("subsection", "Grid display", mystackg)(wp)
    oj.Subsubsection_("subsubsection", "Wrap display", mystackw)(wp)
    return wp


#wp = jp.WebPage()
# circle = circleStub(wp)
# print(circle.twsty_tags)
#wp = launcher(None)
app = jp.app
jp.justpy(launcher, start_server=False)
#wp = launcher(None)
