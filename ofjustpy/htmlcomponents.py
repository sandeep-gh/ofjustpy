from aenum import Enum
from addict import Dict
import justpy as jp
from .ui_styles import basesty, sty
from tailwind_tags import tstr
from .tracker import trackStub


class EventType(Enum):
    click = "click"
    mouseover = "mouseover"
    mouseout = "mouseout"
    mouseenter = "mouseenter"
    mouseleave = "mouseleave"
    input = "input"  # input is keyword of python
    change = "change"


class HCC(jp.Div):
    """
    HCC: html component container
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spathMap = Dict(track_changes=True)

    def addItems(self, cgens):
        cdbref = [cgen(self) for cgen in cgens]

        for dbref in cdbref:
            self.spathMap[dbref.stub.spath] = dbref

    def getItem(self, stub):
        return self.spathMap[stub.spath]


class StackG(HCC):
    def __init__(self, *args, **kwargs):
        print("all kwargs passed as is")
        num_rows = kwargs.pop('num_rows', 2)
        num_cols = kwargs.pop('num_cols', 2)
        # pcp passed via Stub gets  incorporated in twsty_tags in genStubFunc
        twsty_tags = kwargs.pop('twsty_tags', [])
        twsty_tags = [*twsty_tags, *sty.stackG(num_cols, num_rows)]
        super().__init__(*args,  twsty_tags=twsty_tags, **kwargs)


class Stub:
    def __init__(self, *args, **kwargs):
        self.key = args[0]
        self.hcgen = args[1]
        self.target = None
        self.eventhandlers = []
        self.args = args
        self.kwargs = kwargs
        self.postrender = kwargs.pop('postrender', None)
        self.cgens = kwargs.pop('cgens', None)
        pass

    def __call__(self, a):
        # print(f"calling as function {self.id}")
        # TODO: what about other parameters
        self.target = self.hcgen(**self.kwargs, a=a)

        self.target.stub = self
        if self.postrender:
            # print("call postrender ", self.key)
            self.postrender(self.target)

        # TODO: will think about this
        # self.target.postrender()

        # TODO: attach events
        for event_type, handler in self.eventhandlers:
            self.target.on(event_type, handler)

        if self.cgens:
            self.target.addItems(self.cgens)
        # return anchor so that other components can hang on to it
        return a

    def event_handle(self, event_type, handler):
        self.eventhandlers.append((event_type.value, handler))
        return self


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
Label_ = genStubFunc(jp.Label, sty.label)
Circle_ = genStubFunc(jp.Button, sty.circle)
Span_ = genStubFunc(jp.Span, sty.span)
StackV_ = genStubFunc(HCC, sty.stackv)
StackH_ = genStubFunc(HCC, sty.stackh)
StackW_ = genStubFunc(HCC, sty.stackw)
# sty will be set in StackG:init
StackG_ = genStubFunc(StackG, [])


@trackStub
def SubheadingBanner_(key, heading_text, pcp=[], heading_text_sty=sty.subheading_text,  **kwargs):
    # = genStubFunc(jp.Div, sty.subheading_box)
    spanl_ = Span_("headingL", text=heading_text, pcp=heading_text_sty)
    spanr_ = Span_("headingR", text=heading_text, pcp=[
        *heading_text_sty, "invisible"])
    return Stub(key, jp.Div, twsty_tags=[*pcp, *sty.subheading_box], postrender=lambda dbref, spanl_=spanl_, spanr_=spanr_: spanr_(spanl_(dbref), **kwargs))


@trackStub
def Subsection_(key, heading_text, content_, pcp=[], **kwargs):
    return StackV_(key, cgens=[SubheadingBanner_(
        "heading", heading_text), Halign_(content_)])


def SubsubheadingBanner_(key, heading_text, pcp=[], **kwargs):
    return SubheadingBanner_(key, heading_text, pcp=[], heading_text_sty=sty.subsubheading_text, **kwargs)


def Subsubsection_(key, heading_text, content_, pcp=[], **kwargs):
    return StackV_(key, cgens=[SubsubheadingBanner_(
        "heading", heading_text), Halign_(content_)], **kwargs)


def WithBanner_(key, banner_text, component_, pcp=[], **kwargs):
    return StackH_(key, cgens=[Span_("banner", text=banner_text), component_], pcp=pcp, **kwargs)


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
    return Stub(key, jp.Form, twsty_tags=[*sty.Form, *pcp], postrender=postrender)


def Button_(key, icon_f=None, pcp=[], **kwargs):
    postrender = None
    if icon_f:
        def postrender(dbref, icon_f=icon_f): return icon_f(dbref)
    return Stub(key, jp.Button, twsty_tags=[*sty.button, *pcp], postrender=postrender,  **kwargs)

# class StackV(HCC):
#     def __init__(self, key, **kwargs):
#         super().__init__(key, sty.stackv, **kwargs)
# TwContainer_ = genStubFunc(jp.Div, sty.container)

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
