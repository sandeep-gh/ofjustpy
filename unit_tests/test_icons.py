from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
def on_btn_click(dbref,msg):
    pass

request = Dict()
request.session_id = "abc"


app = jp.build_app()


def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):

        btn1_ = oj.Button_("mybtn1",
                           icon_f = oj.cog_icon,
                   value="myval",
                   text="Click me "
                   )

        btn2_ = oj.Button_("mybtn1",
                           icon_f = oj.menu_icon,
                   value="myval",
                   text="Click me ")

                                      
        panel_ = oj.Halign_(oj.StackV_("mystackv",
                                       cgens=[btn1_, btn2_],
                                       pcp=[space/y/4]
                                       )
                            )

        #aspan_ = oj.Span_("aspan", text="hello", pcp=[bg/green/1])
        wp_ = oj.WebPage_("oa", cgens =[panel_], template_file='svelte.html', title="myoa")

        wp = wp_()
        oj.get_svelte_safelist(session_manager.stubStore)
    return wp

app.add_jproute("/", launcher, "launcher")


#wp  = launcher(request)
