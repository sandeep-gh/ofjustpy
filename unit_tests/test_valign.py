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
    session_manager = oj.get_session_manager(request.session_id)
    def on_input_change(dbref, msg):
        #traceback.print_stack(file=sys.stdout)
        #print (msg)
        print ('in input change')
        print (msg)
        print ('value = ', msg.checked)
        pass
        
    with oj.sessionctx(session_manager):
        target_ = oj.Valign_(oj.CheckboxInput_("Acboxinp",
                                               cbox_attrs={'checked':True},
                                               input_attrs={'placeholder':"whatsup"}
                                               
                                          ).event_handle(oj.change,
                                                                   on_input_change
                                                                   ),
                             pcp=[H/128]
                             )
        wp_ = oj.WebPage_("oa",
                          cgens =[target_],
                          template_file='svelte.html',
                          title="myoa"
                          )
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

