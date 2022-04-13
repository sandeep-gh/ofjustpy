
import justpy as jp
from .ui_styles import basesty, sty
from tailwind_tags import tstr
from .tracker import trackStub


class Stub:
    def __init__(self, *args, **kwargs):
        self.key = args[0]
        self.hcgen = args[1]
        self.target = None
        self.eventhandlers = []
        self.args = args
        self.kwargs = kwargs
        self.postrender = kwargs.pop('postrender', None)
        pass

    def __call__(self, a):
        # print(f"calling as function {self.id}")
        # TODO: what about other parameters
        self.target = self.hcgen(**self.kwargs, a=a)
        if self.postrender:
            self.postrender(self.target)

        # TODO: will think about this
        # self.target.postrender()

        # TODO: attach events

        return self.target

    def add_event_handler(self, event_type, handler):
        self.eventhandlers.append((event_type, handler))
        pass


@trackStub
def Halign_(tstub, align="center", pcp=[], **kwargs):
    """
    tstub: target stub, i.e., the one needs to be aligned
    """
    return Stub(f"Halign{tstub.key}",  jp.Div, twsty_tags=[
        *pcp, *sty.halign(align)],     postrender=lambda dbref, tstub=tstub: tstub(dbref), **kwargs)


@trackStub
def Form_(key, content_, submit_, on_form_submit, pcp=[]):
    def postrender(dbref, c=content_, s=submit_):
        c(dbref)
        s(dbref)
    return Stub(key, jp.Form, twsty_tags=[*sty.Form, *pcp], postinit=postrender)

# def A_(key, **kwargs):
#     pcp = kwargs.pop('pcp')
#     twsty_tags = [*sty.A,  *pcp]
#     return Stub(key, jp.A, twsty_tags=twsty_tags, **kwargs)

# def P_(key, **kwargs):
#     pcp = kwargs.pop('pcp')
#     twsty_tags = [*sty.P,  *pcp]
#     return Stub(args[0], jp.P, kwargs)


def genStubFunc(jpf, stytags):
    @trackStub
    def func(key, **kwargs):
        pcp = kwargs.pop('pcp', [])
        twsty_tags = [*stytags,  *pcp]
        return Stub(key, jpf, twsty_tags=twsty_tags, **kwargs)
    return func


P_ = genStubFunc(jp.P, sty.P)
A_ = genStubFunc(jp.A, sty.A)
Circle_ = genStubFunc(jp.Button, sty.circle)
Span_ = genStubFunc(jp.Span, sty.span)

# def Circle_(*args, **kwargs):
#     pcp = kwargs.pop('pcp')
#     twsty_tags = [*sty.circle,  *pcp]
#     return Stub(args[0], jp.Button, *args[1:], twsty_tags=twsty_tags, **kwargs)


# class Circle(jp.Button):
#     def __init__(self,  key, text, *args, **kwargs):
#         pcp = kwargs.pop('pcp')
#         twsty_tags = [*sty.circle,  pcp]
#         super().__init__(classes=tstr(*twsty_tags),
#                          text=text, value=text, twsty_tags=twsty_tags, **kwargs)

# short tag for htmlcomponents
