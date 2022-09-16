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

app = jp.app

#@app.jproute("/")
def launcher(request):
    _sm = oj.get_session_manager(request.session_id)
    _ss = _sm.stubStore
    with oj.sessionctx(_sm):
        def on_btn_click(dbref,msg):
            # print ("btn clicked ", _ss.mybtn1.spath)
            # print ("btn clicked ", _ss.mybtn2.spath)
            _ss.mydeck.target.bring_to_front(dbref.value)
            pass
        btn1_ = oj.Button_("mybtn1",
                   value="/mybtn2",
                   text="Click me1 ", pcp=[bg/blue/100/50]).event_handle(oj.click, on_btn_click)
        


        btn2_ = oj.Button_("mybtn2",
                   value="/mybtn1",
                   text="Click me2 ", pcp=[bg/blue/100/50]).event_handle(oj.click, on_btn_click)

        deck_ = oj.StackD_("mydeck",
                   cgens = [btn1_, btn2_]
                    )

        wp_ = oj.WebPage_("oa", cgens =[deck_], template_file='svelte.html', title="myoa")
        wp = wp_()
        print ("v1 = ", btn1_.target.value)
        print ("v2 = ", btn2_.target.value)
        wp.session_manager = _sm
        
    return wp

#jp.Route("/", launcher)
app.add_jproute("/", launcher)
# wp = launcher(request)
# _sm = wp.session_manager
# _ss = _sm.stubStore

# msg = Dict()
# msg.value = "somevalue"
# print(_ss.mydeck.target.selected_card_spath)
# _ss.mybtn1.target.on_click(msg)
# print(_ss.mydeck.target.selected_card_spath)


#jp.justpy(launcher, start_server=False)
