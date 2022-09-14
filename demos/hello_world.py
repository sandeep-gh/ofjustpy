import logging
import os

if os:
    try:
        os.remove("launcher.log")
    except:
        pass

import sys
if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)

  
import ofjustpy as oj
import justpy as jp
from tailwind_tags import *
def wp_hello_world(request):
    session_id = request.session_id
    session_manager = oj.get_session_manager(session_id)
    stubStore = session_manager.stubStore
    with oj.sessionctx(session_manager):
        with session_manager.uictx("header") as headerCtx:
            title_ = oj.Title_("title", "A hello world page", pcp=[bg/pink/"100/20"])
        with session_manager.uictx("body") as bodyCtx:
            body_ = oj.Halign_(
                oj.Prose_("greeting", "Hello world! This page was written using ofjustpy python  framework ", pcp=[fz.lg, bsw._, sw/gray/400, ta.center]), pcp=[mr/st/8]
                )
        with session_manager.uictx("footer") as bodyCtx:
            footer_ = oj.Halign_(
                oj.Prose_("depart", "Thats all folks! Hope you got the broad drift of this framework", pcp=[mr/st/64, ta.right]), "end"
                )
        oj.Container_("tlc",
                          cgens = [title_,
                                   body_,
                                   footer_],
                          pcp=[H/"screen", bg/gray/"100/20"])
        wp = oj.WebPage_("wp_hello_world",
                         cgens= [stubStore.tlc],
                         template_file='svelte.html',
                             title="a svelte page")()

        return wp
#jp.CastAsEndpoint(wp_hello_world, "/", "hello_world_entry_point")
jp.Route("/", wp_hello_world)
app = jp.app
#jp.justpy(wp_hello_world, start_server=False)
#from starlette.testclient import TestClient
#client = TestClient(app)
#response = client.get('/') 
