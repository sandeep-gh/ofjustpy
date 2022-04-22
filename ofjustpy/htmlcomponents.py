from aenum import Enum
from typing import List, AnyStr, Callable, Any
from addict import Dict
import justpy as jp
from .ui_styles import basesty, sty
from tailwind_tags import tstr, W, full, jc, twcc2hex, bg, onetonine
from .tracker import trackStub

StubFunc_T = Callable[Any, Any]


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
        self.eventhandlers = {}
        self.args = args
        self.kwargs = kwargs
        self.postrender = kwargs.pop('postrender', None)
        if self.key == "wp":
            print("in init stub")
            print(kwargs)
        self.cgens = kwargs.pop('cgens', None)
        redirects = kwargs.pop('redirects', None)
        self.redirects = None
        if redirects:
            self.redirects = Dict(redirects)

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

        # attach event handlers
        for event_type, handler in self.eventhandlers.items():
            if self.redirects and event_type in self.redirects:
                # self.target.on(event_type, handler)
                # call local handler
                self.target.on(event_type, self.redirects[event_type])
            else:
                self.target.on(event_type, handler)

        if self.cgens:
            self.target.addItems(self.cgens)
        # return anchor so that other components can hang on to it
        return a

    def event_handle(self, event_type, handler):
        self.eventhandlers[event_type.value] = handler
        return self


class WPStub(Stub):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self):
        """for webpage instantiation"""
        # print(f"calling as function {self.id}")
        # TODO: what about other parameters
        self.target = self.hcgen(**self.kwargs)

        self.target.stub = self
        if self.postrender:
            # print("call postrender ", self.key)
            self.postrender(self.target)

        # TODO: will think about this
        # self.target.postrender()

        # attach event handlers
        if self.cgens:
            # wp is not an HCC
            for cgen in self.cgens:
                cgen(self.target)
        # return anchor so that other components can hang on to it
        return self.target


def genStubFunc(jpf, stytags):

    @trackStub
    def func(key: AnyStr, **kwargs):
        pcp = kwargs.pop('pcp', [])
        twsty_tags = [*stytags,  *pcp]
        return Stub(key, jpf, twsty_tags=twsty_tags, **kwargs)
    return func


P_ = genStubFunc(jp.P, sty.P)
A_ = genStubFunc(jp.A, sty.A)
Label_ = genStubFunc(jp.Label, sty.label)
Circle_ = genStubFunc(jp.Button, sty.circle)
Span_ = genStubFunc(jp.Span, sty.span)
InputChangeOnly_ = genStubFunc(jp.InputChangeOnly, sty.input)
Input_ = genStubFunc(jp.Input, sty.input)

# use glossy=True,
# size="sm", label=label, value =False for toggle btn
ToggleBtn_ = genStubFunc(jp.QToggle, sty.togglebtn)
Textarea_ = genStubFunc(jp.Textarea, sty.textarea)
Option_ = genStubFunc(jp.Option, sty.option)
Container_ = genStubFunc(HCC, sty.container)
StackV_ = genStubFunc(HCC, sty.stackv)
StackH_ = genStubFunc(HCC, sty.stackh)
StackW_ = genStubFunc(HCC, sty.stackw)
# sty will be set in StackG:init using num_rows, num_cols keyword arguments
StackG_ = genStubFunc(StackG, [])


@trackStub
def SubheadingBanner_(key: AnyStr, heading_text: AnyStr, pcp: List = [], heading_text_sty=sty.subheading_text,  **kwargs):
    # = genStubFunc(jp.Div, sty.subheading_box)
    spanl_ = Span_("headingL", text=heading_text, pcp=heading_text_sty)
    spanr_ = Span_("headingR", text=heading_text, pcp=[
        *heading_text_sty, "invisible"])
    return Stub(key, jp.Div, twsty_tags=[*pcp, *sty.subheading_box], postrender=lambda dbref, spanl_=spanl_, spanr_=spanr_: spanr_(spanl_(dbref), **kwargs))


@trackStub
def LabeledInput_(key: AnyStr, label: AnyStr, placeholder: AnyStr,  input_type="changeonly", pcp=[], **kwargs):
    span_ = Span_("iname", text=label, pcp=sty.span)
    if input_type == "changeonly":
        input_ = InputChangeOnly_(
            "input", placeholder=placeholder, type=type)
    else:
        input_ = Input_("input", placeholder=placeholder)
    return Stub(key, jp.Label, twsty_tags=[*pcp, *sty.label], postrender=lambda dbref, span_=span_, input_=input_: input_(span_(dbref)))


@trackStub
def CheckboxInput_(key: AnyStr, placeholder: AnyStr, pcp=[], **kwargs):
    # TODO: make form-checkbox firstclass
    cbox_ = Input_("cbox", type="checkbox", pcp=['form-checkbox'])
    input_ = Input_("inp", type="text", placeholder=placeholder)
    return Stub(key, jp.Label, twsty_tags=[*pcp, *sty.label], postrender=lambda dbref, cbox_=cbox_, input_=input_: input_(cbox_(dbref)), **kwargs)


@trackStub
def Subsection_(key: AnyStr, heading_text: AnyStr, content_: Callable, pcp=[], **kwargs):
    return StackV_(key, cgens=[SubheadingBanner_(
        "heading", heading_text), Halign_(content_)], **kwargs)


def KeyValue_(key: AnyStr, keyt: AnyStr, valuet: AnyStr, readonly=True, pcp=[], **kwargs):
    key_ = Span_("keyt", text=keyt, pcp=sty.left_cell)
    eq_ = Span_("eqt", text="=", pcp=sty.eq_cell)
    value_ = Span_("valuet", type="text", text=valuet,
                   readonly=readonly, pcp=sty.right_cell)
    # TODO: overwrite xmargin. put padding only around stack
    return StackH_(key, cgens=[key_, eq_, value_], pcp=[W/full, jc.center], **kwargs)


def SubsubheadingBanner_(key: AnyStr, heading_text: AnyStr, pcp=[], **kwargs):
    return SubheadingBanner_(key, heading_text, pcp=[], heading_text_sty=sty.subsubheading_text, **kwargs)


def Subsubsection_(key: AnyStr, heading_text: AnyStr, content_: Callable, pcp: List = [], **kwargs):
    return StackV_(key, cgens=[SubsubheadingBanner_(
        "heading", heading_text), Halign_(content_)], **kwargs)


def WithBanner_(key: AnyStr, banner_text: AnyStr, component_: Callable, pcp: List = [], **kwargs):
    return StackH_(key, cgens=[Span_("banner", text=banner_text), component_], pcp=pcp, **kwargs)


@trackStub
def Halign_(content_: Callable, align="center", pcp=[], **kwargs):
    """
    tstub: target stub, i.e., the one needs to be aligned
    """
    return Stub(f"Halign{content_.key}",  jp.Div, twsty_tags=[
        *pcp, *sty.halign(align)],     postrender=lambda dbref, tstub=content_: tstub(dbref), **kwargs)
# TODO: implement default value


@trackStub
def Slider_(key: AnyStr, itemiter: List, pcp: List = [], **kwargs):
    def on_circle_click(dbref, msg):
        # print("circle clicked with value ", dbref.text,
        #       " ", msg.value, " ", dbref.slider)
        # pass the value of selected circle to slider
        dbref.slider.value = msg.value

        pass
    circle_stubs = [Circle_(f"c{_}", text=str(_), value=_).event_handle(
        EventType.click, on_circle_click) for _ in itemiter]

    def postrender(dbref, circle_stubs=circle_stubs):
        for cs in circle_stubs:
            cs(dbref)
            cs.target.slider = dbref
        dbref.circle_stubs = circle_stubs

    # return Stub(key, jp.Div, twsty_tags=[*pcp, *sty.slider], postrender=lambda dbref, circle_stubs=circle_stubs: [_(dbref) for _ in circle_stubs])
    # The click on Slider should come to this function; its value updated then passed to user

    def on_click_hook(dbref, msg):
        msg.value = dbref.value
        if 'click' in dbref.stub.eventhandlers:
            dbref.stub.eventhandlers['click'](dbref, msg)
        pass
    stub = Stub(key, jp.Div, twsty_tags=[
                *pcp, *sty.slider], postrender=postrender, redirects=[('click', on_click_hook)], **kwargs)
    stub.circle_stubs = circle_stubs
    return stub


def MainColorSelector_(key: AnyStr, **kwargs):
    color_list = twcc2hex.keys()
    all_options = [Option_(f"opt_{option}", text=option, value=option, pcp=[bg/sty.get_color_tag(option)/5])
                   for option in color_list]
    return Select_(key, all_options, **kwargs)


@trackStub
def ColorSelector_(key: AnyStr, pcp: List = [], **kwargs):
    def on_main_color_select(dbref, msg):
        print("main color selected ", msg.value)
        # pass the selection to parent component
        dbref.colorSelector.maincolor_value = msg.value
        colortag = sty.get_color_tag(dbref.colorSelector.maincolor_value)
        dbref.colorSelector.component_clicked = 'mainColorSelector'
        pass
    mainColorSelector_ = MainColorSelector_("MainColorSelector").event_handle(
        EventType.click, on_main_color_select)

    def on_slider_select(dbref, msg):
        print("slider selected with value = ", msg.value)
        # whatever value is computed pass to colorselector
        # pass the selection to parent component
        dbref.colorSelector.slider_value = int(msg.value)
        dbref.colorSelector.component_clicked = 'slider'
        pass
    shades_ = Slider_("Shades", range(1, 10)).event_handle(
        EventType.click, on_slider_select)

    def update_slider(colortag, shades_=shades_):
        for cs in shades_.circle_stubs:
            cref = cs.target
            shid = int(cref.value)
            cref.twcc = f"{colortag}-{shid}00"
            # TODO: also update twsty_tags
            cref.set_class(f"bg-{colortag}-{shid}00")

    def postrender(dbref):
        dbref.addItems([mainColorSelector_, shades_])
        shades_.target.colorSelector = dbref
        mainColorSelector_.target.colorSelector = dbref
        dbref.maincolor_value = "blue"
        dbref.slider_value = 5  # the default value
        dbref.component_clicked = None

    def on_click_hook(dbref, msg):
        main_color = dbref.maincolor_value
        shade = dbref.slider_value

        msg.value = twcc2hex[main_color][onetonine[shade]]
        match dbref.component_clicked:
            case 'mainColorSelector':
                update_slider(dbref.maincolor_value)
            case None:
                pass
            case 'slider':
                if 'click' in dbref.stub.eventhandlers:
                    dbref.stub.eventhandlers['click'](dbref, msg)
    # TODO: fix spacing
    # TODO: event handling
    # return StackH_(key, cgens=[mainColorSelector_, shades_])
    return Stub(key, HCC, twsty_tags=[*pcp, *sty.stackh], postrender=postrender, redirects=[('click', on_click_hook)], **kwargs)


# TODO: toggleBtn, expansionContainer

# TODO: check event_handle for form
@trackStub
def Form_(key: AnyStr, content_: Callable, submit_: Callable, pcp: List = [], **kwargs):
    def postrender(dbref, c=content_, s=submit_):
        c(dbref)
        s(dbref)
    return Stub(key, jp.Form, twsty_tags=[*sty.Form, *pcp], postrender=postrender, **kwargs)


@trackStub
def Button_(key: AnyStr, icon_f: Callable = None, pcp: List = [], **kwargs):
    postrender = None
    if icon_f:
        def postrender(dbref, icon_f=icon_f): return icon_f(dbref)
    return Stub(key, jp.Button, twsty_tags=[*sty.button, *pcp], postrender=postrender,  **kwargs)

# seriously wrong with select -- default val is not working


@trackStub
def Select_(key: AnyStr, options: List, pcp: List = [], **kwargs):
    """
    to use default option, pass it to kwargs with text and value
    """
    return Stub(key, jp.Select, twsty_tags=[*sty.select, *pcp], postrender=lambda dbref: [_(dbref) for _ in options],  **kwargs)

# TODO: how to deal with events at Div level


@trackStub
def InputJBtn_(key: AnyStr, input_: Callable,  button_: Callable, pcp=[], **kwargs):
    """
    Put an input next to button
    """

    return Stub(key, jp.Div, twsty_tags=[*sty.centering_div, *sty.spacing, *pcp], postrender=lambda dbref, input_=input_, button_=button_: button_(input_(dbref), **kwargs))


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
@trackStub
def WebPage_(key: AnyStr, page_type: AnyStr = 'tailwind', head_html_stmts: List[AnyStr] = [], cgens: List = [], **kwargs):
    def postrender(wp, cgens=cgens):
        # TODO: declare session manager here
        wp.tailwind = False  # we inject our tailwind
        wp.head_html = "\n".join([*head_html_stmts,
                                  """<link rel = "stylesheet" href = "https://cdn.jsdelivr.net/npm/inter-ui@3.13.1/inter.min.css" > """,
                                  """ <script src = "https://cdn.tailwindcss.com/" > </script >"""
                                  ])
        # wp.head_html = "\n".join(head_html)
        wp.css = 'body { font-family: Inter; }'
        wp.body_classes = tstr(*wp.twsty_tags)

    if page_type == 'tailwind':
        stub = WPStub(key, jp.WebPage, twsty_tags=[
            *sty.wp], postrender=postrender, cgens=cgens, **kwargs)
    elif page_type == 'quasar':
        stub = WPStub(key, jp.QuasarPage, twsty_tags=[
            *sty.wp], postrender=postrender, cgens=cgens,  **kwargs)
    return stub
