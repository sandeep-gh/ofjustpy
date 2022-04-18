import ofjustpy as oj
from tailwind_tags import *
import justpy as jp
from tailwind_tags import *


def launcher(request):
    wp = jp.WebPage()
    wp.head_html = """<script src="https://cdn.tailwindcss.com/"></script>"""

    def on_btn_click(dbref, msg):
        print("btn clicked ", msg)

        pass

    def on_input_change(dbref, msg):
        print("on input called", msg.value)
        pass

    # separator_ = oj.Button_("sep",  pcp=[mr/st/8, mr/sb/8,
    #                                      W/full, H/4, bg/slate/"500/50"])

    def stubs():
        for _ in [
                # TODO: slider is messed up
                # oj.Slider_("myslider", range(5), pcp=[
                #            bg/green/5]).event_handle(oj.click, on_btn_click)
                # separator_,
                # oj.Slider_("myslider", range(5), pcp=[bg/green/5]),
                oj.ColorSelector_("colorselector").event_handle(
                    oj.click, on_btn_click)

        ]:
            yield _

    mystackv = oj.Halign_(oj.StackV_(
        "mystackv", cgens=[oj.Halign_(stub) for stub in stubs()]))
    # mystackh = oj.Halign_(oj.StackH_(
    #     "mystackh", cgens=[oj.Halign_(stub) for stub in stubs()]))

    # mystackw = oj.Halign_(oj.StackW_(
    #     "mystackh", cgens=[oj.Halign_(stub) for stub in stubs()]))

    # mystackg = oj.Halign_(oj.StackG_(
    #     "mystackh", num_rows=3, num_cols=3,  cgens=[oj.Halign_(stub) for stub in stubs()]))
    # mystackh(wp)
    mystackv(wp)
    # mystackw(wp)
    # mystackg(wp)
    # oj.Subsection_("subsection", "Grid display", mystackg)(wp)
    # oj.Subsubsection_("subsubsection", "Wrap display", mystackw)(wp)
    return wp


#wp = jp.WebPage()
# circle = circleStub(wp)
# print(circle.twsty_tags)
#wp = launcher(None)
app = jp.app
jp.justpy(launcher, start_server=False)
#wp = launcher(None)
# print(oj.stubStore.keys())
