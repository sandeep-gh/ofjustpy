"""
drop down color not working in firefox
"""

from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
import traceback
from starlette.middleware import Middleware
from asgi_signing_middleware import SerializedSignedCookieMiddleware
# from csrf_middleware import CSRFMiddleware
# csrf_cookie_name = "csrftoken"
# csrf_secret="scsdsfwe" #should this be signed by cookie signer??

# X = Middleware(CSRFMiddleware,
#                                 secret=csrf_secret,
#                                 field_name = csrf_cookie_name)
csrf_cookie_name = "csrftoken"
csrf_secret='shhshh' #should this be signed by cookie signer??
app = jp.build_app([Middleware(SerializedSignedCookieMiddleware,
                               secret=b'a very, very secret thing',  
                               state_attribute_name='messages',  
                               cookie_name='my_cookie',
                               cookie_ttl=60 * 5,  
                               )
                    ])

#app = jp.build_app()

def launcher(request):

    wp = jp.WebPage(template_file='svelte.html')
    
    def on_click(dbref, msg):
        print (" obtn clicked")
    obtn = jp.Button(text="oSubmit", a=wp, type="submit", classes=["bg-pink-500"])
    obtn.on('click', on_click)
    #wp.cookies[csrf_cookie_name] =  csrf_secret
    request.state.messages.data = {'A Title': 'The message',
                                   'Another title': 'With another msg',
                                   csrf_cookie_name: csrf_secret
                                   }
    
    wp.use_websockets = False
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
