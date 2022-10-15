from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
def on_btn_click(dbref,msg):
    pass

request = Dict()
request.session_id = "abc"


app = jp.build_app()

all_colors = [slate , gray , zinc , neutral , stone , red , orange , amber , yellow , lime , green , emerald , teal , cyan , sky , blue , indigo , violet , purple , fuchsia , pink , rose]

def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        all_btns_ = [ oj.StackW_(f"colorrow{cp}",
                                cgens = [oj.Button_(f"mybtn:{cp}{k}",
                                            value="myval",
                                            text="Click me ",
                                            pcp=[bg/cp/k]).event_handle(oj.click, on_btn_click)
                                         for k in range(1,10,1)
                                 ]
                                )
                     for cp in all_colors]

                                      
        panel_ = oj.Halign_(oj.StackV_(
            "mystackv", cgens=all_btns_))


        def on_click(dbref, msg):
            pass
        btn_ = oj.Button_("abtn",
                   text="a disabled button",
                   disabled = True,
                   pcp = variant(bg/rose/"50",
                                 fc/slate/5,
                                 bd/slate/2,
                                 bsw.none,
                                 rv="disabled")
                          ).event_handle(oj.click, on_click)
        wp_ = oj.WebPage_("oa", cgens =[btn_], template_file='svelte.html', title="myoa")

        wp = wp_()
        oj.get_svelte_safelist(session_manager.stubStore)
    return wp

app.add_jproute("/", launcher, "launcher")

#wp  = launcher(request)
