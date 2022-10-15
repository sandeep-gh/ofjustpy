"""
drop down color not working in firefox
"""

from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
def on_btn_click(dbref,msg):
    print("button clicked")
    pass

request = Dict()
request.session_id = "abc"




all_colors = [slate , gray , zinc , neutral , stone , red , orange , amber , yellow , lime , green , emerald , teal , cyan , sky , blue , indigo , violet , purple , fuchsia , pink , rose]

def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        colorselector_ = oj.ColorSelector_(
            "colorselector").event_handle(
                        oj.click, on_btn_click)
        
        # select_ = oj.Select_("myselect",
        #            [oj.Option_(k, text=k, value=k, pcp=[bg/blue/100])
        #             for k in ['red', 'blue', 'green']
        #             ],
        #            text="def",
        #            value="def",
        #            pcp=[bg/green/100]
        #            ).event_handle(oj.click, on_btn_click)
        
        # all_btns = [ oj.StackW_(f"colorrow{cp}",
        #                         cgens = [oj.Button_("mybtn:{cp}{k}",
        #                                     value="myval",
        #                                     text="Click me ",
        #                                     pcp=[bg/cp/k]).event_handle(oj.click, on_btn_click)
        #                                  for k in range(100,1000,100)
        #                          ]
        #                         )
        #              for cp in all_colors]
        # panel_ = oj.Halign_(oj.StackV_(
        #     "mystackv", cgens=all_btns))

        wp_ = oj.WebPage_("oa", cgens =[colorselector_], template_file='svelte.html', title="myoa")
        wp = wp_()
        wp.session_manager = session_manager
        oj.get_svelte_safelist(session_manager.stubStore)
    return wp

#jp.Route("/", launcher)

# request = Dict()
# request.session_id = "abc"
# wp = launcher(request)
# _ss = wp.session_manager.stubStore

# msg = Dict()

# msg.value = 'pink'
# _ss.MainColorSelector.target.on_click(msg)
# _ss.colorselector.target.on_click(msg)

# msg.page = wp

# print(wp.session_manager.stubStore.colorselector.target.on_click(msg))

app = jp.app
jp.justpy(launcher, start_server=False)

