import ofjustpy as oj
from tailwind_tags import *
import justpy as jp
from tailwind_tags import *


def launcher(request):

    def on_btn_click(dbref, msg):
        print("circle clicked", dbref.text, msg.value)

        pass

    def on_input_change(dbref, msg):
        print("on input called", msg.value)
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
                             text="Click me ", pcp=[bg/blue/100/50]).event_handle(oj.click, on_btn_click),
                  oj.InputChangeOnly_("ico", placeholder="haan"),
                  oj.Input_("inp", placeholder="hoon", type="number"),
                  oj.LabeledInput_("linp", "Enter a value",
                                   "avalue", pcp=[fc/green/800]).event_handle(oj.change, on_input_change),
                  oj.CheckboxInput_(
                      "cboxinp", "selected text", pcp=[bg/rose/100]).event_handle(oj.change, on_input_change),
                  oj.Textarea_("textarea", text="lets put lots of text lets put lots of text lets put lots of textlets put lots of text").event_handle(
                      oj.change, on_input_change),

                  oj.KeyValue_("keyvalue", "akeya", "itsvalue"),
                  oj.Option_("myopt", text="choice", value="value"),
                  oj.Select_("myselect", [oj.Option_(
                      k, text=k, value=k) for k in ['red', 'blue', 'green']], text="def", value="def").event_handle(oj.click, on_btn_click),
                  # oj.Slider_("myslider", range(5), pcp=[bg/green/5]) #TODO: slider is messed up
                  oj.ColorSelector_(
            "colorselector", pcp=[bg/rose/"200/20"])
        ]:
            yield _

    # mystackv = oj.Halign_(oj.StackV_(
    #     "mystackv", cgens=[oj.Halign_(stub) for stub in stubs()]))
    # mystackh = oj.Halign_(oj.StackH_(
    #     "mystackh", cgens=[oj.Halign_(stub) for stub in stubs()]))

    # mystackw = oj.Halign_(oj.StackW_(
    #     "mystackh", cgens=[oj.Halign_(stub) for stub in stubs()]))

    # mystackg = oj.Halign_(oj.StackG_(
    #     "mystackh", num_rows=3, num_cols=3,  cgens=[oj.Halign_(stub) for stub in stubs()]))
    # mystackh(wp)
    #wp = jp.WebPage()
    session_manager = oj.get_session_manager(request.session_id)
    stubStore = session_manager.stubStore
    with oj.sessionctx(session_manager):
        with session_manager.uictx("tlctx") as tlctx:
            mystackv = oj.Halign_(oj.StackV_(
                "mystackv", cgens=[oj.Halign_(stub) for stub in stubs()]))
            wp_ = oj.WebPage_("oa", cgens = [mystackv], template_file='svelte.html', title="myoa")
    wp = wp_()
    # mystackw(wp)
    # mystackg(wp)
    # oj.Subsection_("subsection", "Grid display", mystackg)(wp)
    # oj.Subsubsection_("subsubsection", "Wrap display", mystackw)(wp)
    return wp

#jp.CastAsEndpoint(launcher, "/", "cases_and_mounts")
jp.Route("/", launcher)
#wp = jp.WebPage()
# circle = circleStub(wp)
# print(circle.twsty_tags)
# request = Dict()
# request.session_id = 'abc'
# wp = launcher(request)
app = jp.app
jp.justpy(launcher, start_server=False)
#wp = launcher(None)








