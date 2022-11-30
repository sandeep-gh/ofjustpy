"""
drop down color not working in firefox
"""

from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
def on_toggle_change(dbref,msg):
    print ("changed ")
    
    pass

request = Dict()
request.session_id = "abc"

def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        select_ = oj.ToggleBtn_("mytoggle",
                                value=True
                                
                   ).event_handle(oj.input, on_toggle_change)
    
        span_ = oj.Span_("mytext", text = "a toggle btn")

        wp_ = oj.WebPage_("oa", cgens =[span_, select_], template_file='svelte.html', title="myoa")
        wp = wp_()
    return wp

#jp.Route("/", launcher)



app = jp.app
jp.justpy(launcher, start_server=False)
