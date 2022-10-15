"""
drop down color not working in firefox
"""

#from tailwind_tags import *
from tailwind_tags import bg, blue, bd, bdr, gray, H, W, full, pd
import ofjustpy as oj
from addict import Dict
import justpy as jp
def on_btn_click(dbref,msg):
    print ("clicked ", msg.value)
    pass

request = Dict()
request.session_id = "abc"
@jp.app.requires(['authenticated'])
@jp.app.jproute("/home", name="homepage")
def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        select_ = oj.Span_("xyz", text="alhpa")
        wp_ = oj.WebPage_("oa", cgens =[select_], template_file='svelte.html', title="myoa")

        wp = wp_()
        wp.session_manager = session_manager
    return wp



from starlette.testclient import TestClient
client = TestClient(jp.app)
response = client.get('/') 
