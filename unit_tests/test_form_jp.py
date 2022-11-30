"""
drop down color not working in firefox
"""

from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
import traceback

app = jp.build_app()

def launcher(request):
    # this is necessary
    # a bug in justpy for input change
    def on_input_change(dbref, msg):
        #traceback.print_stack(file=sys.stdout)
        print (msg)
        pass

    def on_submit_click(dbref, msg):
        print ("ok whatever")
        try:
            print("ohoo")
            id = dbref.id
            print (msg)
            print("Aha")
            
        except Exception as e:
            print ("OMG ", e)
        pass

    wp = jp.WebPage()
    
    def on_click(dbref, msg):
        print (" obtn clicked")
    obtn = jp.Button("obtn", text="oSubmit", a=wp, type="submit")
    obtn.on('click', on_click)
    form = jp.Form(a = wp)
    jp.Input(a = form, 
        btn_ = oj.Button_("mybtn", text="Submit", type="submit")
        target_ = oj.Form_("myform", oj.LabeledInput_(
                                 "labeldinput",
                                 "Input a value", "30").event_handle(oj.change, on_input_change)
                           ,btn_
                ).event_handle(oj.submit, on_submit_click)
        # target_ = oj.Halign_(oj.LabeledInput_(
        #                          "labeldinput",
        #                          "Input a value", "30").event_handle(oj.change,
        #                                                              on_input_change
        #                                                              )
        #                      )
        wp_ = oj.WebPage_("oa", cgens =[target_, obtn_], template_file='svelte.html', title="myoa")
        wp = wp_()
        wp.session_manager = session_manager
    return wp

app.add_jproute("/", launcher, name="root")

#jp.justpy(launcher, start_server=False)


# from starlette.testclient import TestClient
# client = TestClient(app)
# response = client.get('/')
# request = Dict()
# request.session_id = "abc"
# wp = launcher(request)
# _sm = wp.session_manager
# _ss = _sm.stubStore
# print(_ss.labeldinput.target.on_change)

#wp = launcher.log
