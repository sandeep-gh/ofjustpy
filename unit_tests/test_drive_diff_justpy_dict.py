"""
communication optimized justpy. Instead of sending across
the whole justpy dict. We send only the diff. 
"""

"""
drop down color not working in firefox
"""

from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
import ofjustpy_react as ojr

app = jp.build_app()

def on_btn_click(dbref,msg):
    dbref.add_twsty_tags(bg/green/5, bd/2, bd/gray/2, bdr.sm)
    pass


def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        btn_ = oj.Button_("mybtn",
                          value="myval",
                          text="Click me ",
                          pcp=[bg/rose/5]).event_handle(oj.click, on_btn_click)
        wp = oj.WebPage_("wp_root",
                         cgens= [btn_],
                         WPtype=ojr.WebPage,
                         session_manager = session_manager,
                         template_file='svelte.html',
                         title="diff-path-apply")()
    wp.session_manager = session_manager
    return wp

app.add_jproute("/", launcher, "root")
# jp.justpy(launcher, start_server=False
# from starlette.testclient import TestClient
# client = TestClient(app)
# response = client.get('/')


# request  = Dict()
# request.session_id = "abc"

# wp = launcher(request)
# _sm = wp.session_manager
# _ss = _sm.stubStore
# msg = Dict()
# _ss.mybtn.target.on_click(msg)
