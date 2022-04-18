import justpy as jp
import ofjustpy as oj
from addict import Dict


def launcher(request):
    session_id = request.session_id
    session_manager = oj.get_session_manager(session_id)

    with oj.sessionctx(session_manager):
        print('do all work here')
        uictx = session_manager.uictx
        with uictx("myctx") as ctx:
            oj.Span_("myspan", text="write here")
            pass
        # print(uictx)
        wp = jp.WebPage()
    print(session_manager)
    return wp


request = Dict()
request.session_id = "abs"
launcher(request)
