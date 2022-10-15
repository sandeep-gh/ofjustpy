"""
drop down color not working in firefox
"""

from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
def on_btn_click(dbref,msg):
    pass

request = Dict()
request.session_id = "abc"




all_colors = [slate , gray , zinc , neutral , stone , red , orange , amber , yellow , lime , green , emerald , teal , cyan , sky , blue , indigo , violet , purple , fuchsia , pink , rose]

def wp_destination(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        wp_ = oj.WebPage_("oa", cgens =[oj.Span_("myspan", text="Hopped to here")], template_file='svelte.html', title="myoa")
        wp = wp_()
    return wp
        
def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        select_ = oj.Select_("myselect",
                   [oj.Option_(k, text=k, value=k, pcp=[bg/blue/100])
                    for k in ['red', 'blue', 'green']
                    ],
                   text="def",
                   value="def",
                   pcp=[bg/green/100]
                   ).event_handle(oj.click, on_btn_click)
        
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

        wp_ = oj.WebPage_("oa", cgens =[select_], template_file='svelte.html', title="myoa")
        wp = wp_()
        def page_ready(dbref, msg):
            print ("page is ready")
            wp.redirect = "/destination"
        wp.on("page_ready", page_ready)
    return wp

jp.Route("/", launcher)

jp.Route("/destination", wp_destination)



app = jp.app
jp.justpy(launcher, start_server=False)
