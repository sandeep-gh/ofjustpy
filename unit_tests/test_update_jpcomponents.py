"""
Test if we are able to update justpyComponents 
properly
"""

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

    
from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp

def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    logging.debug("Shri ganesh")
    print("Shri ganesh")
    with oj.sessionctx(session_manager):

        btn2_ = oj.Button_("mybtn2",
                   value="myval",
                   text="Btn2: change text ", pcp=[bg/blue/100/50])
        def on_btn_click(dbref,msg):
            print(btn2_.target.text)
            btn2_.target.text = "Updated text"
            pass

        btn1_ = oj.Button_("mybtn1",
                   value="myval",
                   text="Btn1: click me  ", pcp=[bg/blue/100/50]).event_handle(oj.click, on_btn_click)


        wp_ = oj.WebPage_("oa", cgens =[btn1_, btn2_], template_file='svelte.html', title="myoa")
        wp = wp_()
    return wp

#jp.Route("/", launcher)



app = jp.app
jp.justpy(launcher, start_server=False)
