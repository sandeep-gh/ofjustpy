"""
drop down color not working in firefox
"""

from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
def on_btn_click(dbref,msg):
    print ("clicked ", msg.value)
    pass

request = Dict()
request.session_id = "abc"

def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        select_ = oj.ColorSelector_("mycolorselector").event_handle(oj.click, on_btn_click) #TODO: slider is messed up
        wp_ = oj.WebPage_("oa", cgens =[select_], template_file='svelte.html', title="myoa")
        wp = wp_()
    return wp

#jp.Route("/", launcher)



app = jp.app
jp.justpy(launcher, start_server=False)




