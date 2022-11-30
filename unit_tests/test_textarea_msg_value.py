"""
drop down color not working in firefox
"""

from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
import traceback
#from wtforms.validators	import DataRequired

app = jp.build_app()

def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    # this is necessary
    # a bug in justpy for input change




    
    with oj.sessionctx(session_manager):
        def on_input(dbref, msg):
            print ("on_input = ", msg.value)
            
        textarea_ = oj.Textarea_("textarea", placeholder="write something").event_handle(oj.change, on_input)
        
        input_ = oj.Input_("myinput", type="text", placeholder="x").event_handle(oj.change,
                                                                                 on_input)
        
        def on_submit_click(dbref, msg):
            print("in submit click")
            print (input_.target.value)
            pass
        
        btn_ = oj.Button_("mybtn", text="Submit", type="submit").event_handle(oj.click,
                                                                              on_submit_click)
        
        wp_ = oj.WebPage_("oa",
                          cgens =[textarea_, input_,  btn_],
                          template_file='svelte.html',
                          title="myoa"
                          )
        wp = wp_()
        wp.session_manager = session_manager
    return wp

app.add_jproute("/", launcher, name="root")

