import ofjustpy as oj
from tailwind_tags import *
import justpy as jp
from tailwind_tags import *


def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
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
                        oj.click, on_btn_click),
                    oj.ToggleBtn_("togglebtn", glossy=True,
                                  size="sm", label="atogglebtn", value=False).event_handle(oj.iinput, on_input_change)

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
        wp = oj.WebPage_("wp_index", page_type='quasar', head_html_stmts=[
        ], cgens=[mystackv])()
        #wp = jp.WebPage()
        #wp.head_html = """<script src="https://cdn.tailwindcss.com/"></script>"""

        # mystackv(wp)
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
