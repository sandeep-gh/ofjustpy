import logging
import sys
if sys:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
import collections
from aenum import Enum
from typing import List, AnyStr, Callable, Any
from addict import Dict
import justpy as jp
from .ui_styles import basesty, sty
from tailwind_tags import tstr, W, full, jc, twcc2hex, bg, onetonine, fz
from .tracker import trackStub
from dpath.util import set as dset, search as dsearch
from .dpathutils import dget, dnew
StubFunc_T = Callable[Any, Any]


#https://stackoverflow.com/questions/44664040/type-hints-with-user-defined-classes/44664064#44664064
from typing import Type

class EventType(Enum):
    click = "click"
    mouseover = "mouseover"
    mouseout = "mouseout"
    mouseenter = "mouseenter"
    mouseleave = "mouseleave"
    input = "input"  # input is keyword of python
    change = "change"
    submit = "submit"


class Nav(jp.Nav):
    """
    HCC: html component container
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spathMap = Dict(track_changes=True)

    def addItems(self, cgens):
        collections.deque(map(lambda cgen: cgen(self), cgens), maxlen=0)
        for stub in cgens:
            self.spathMap[stub.spath] = stub.target
    def getItem(self, stub):
        return self.spathMap[stub.spath]

class Footer(jp.Footer):
    """
    HCC: html component container
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spathMap = Dict(track_changes=True)

    def addItems(self, cgens):
        collections.deque(map(lambda cgen: cgen(self), cgens), maxlen=0)
        for stub in cgens:
            self.spathMap[stub.spath] = stub.target
    def getItem(self, stub):
        return self.spathMap[stub.spath]
    

    
        
class HCC(jp.Div):
    """
    HCC: html component container
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spathMap = Dict(track_changes=True)

    def addItems(self, cgens):
        collections.deque(map(lambda cgen: cgen(self), cgens), maxlen=0)
        for stub in cgens:
            self.spathMap[stub.spath] = stub.target
    def getItem(self, stub):
        return self.spathMap[stub.spath]

# class Li(jp.Li):
    
    

class StackG(HCC):
    def __init__(self, *args, **kwargs):
        num_rows = kwargs.pop('num_rows', 2)
        num_cols = kwargs.pop('num_cols', 2)
        # pcp passed via Stub gets  incorporated in twsty_tags in genStubFunc
        twsty_tags = kwargs.pop('twsty_tags', [])
        twsty_tags = [*twsty_tags, *sty.stackG(num_cols, num_rows)]
        super().__init__(*args,  twsty_tags=twsty_tags, **kwargs)


class StackD(HCC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def addItems(self, cgens):
        super().addItems(cgens)
        
        for spath, dbref in self.spathMap.items():
            dbref.set_class('hidden')

        self.selected_card_spath = cgens[0].spath
        selected_dbref = self.spathMap[self.selected_card_spath]
        selected_dbref.remove_class('hidden')
        selected_dbref.set_class('flex') #TODO: only if there was flex originally
    def bring_to_front(self, spath):
        '''
        tapk: the target apk of du which needs to be brought in front
        '''

        tapk = spath  # f'{self.apk}_{tlid}'
        if tapk in self.spathMap.keys():
            #hide the current front
            self.spathMap[self.selected_card_spath].set_class('hidden')
            #make the selected card visible
            selected_dbref = self.spathMap[tapk]
            selected_dbref.remove_class('hidden')
            selected_dbref.set_class('flex')  # workaround for eat-flex bug

            self.selected_card_spath = tapk
        else:
            logger.debug(
                f"debug: deck  does not have card {tapk}..skipping bring to front")
        
        
        
class Stub:
    def __init__(self, *args, **kwargs):
        self.key = args[0]
        self.hcgen = args[1]
        self.target = None
        self.eventhandlers = {}
        self.args = args

        self.postrender = kwargs.pop('postrender', None)
        if self.key == "wp":
            print(kwargs)
        self.cgens = kwargs.pop('cgens', None)
        redirects = kwargs.pop('redirects', None)
        self.redirects = None
        if redirects:
            self.redirects = Dict(redirects)
        self.kwargs = kwargs
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

    def appctx_trrules(self, ctxl):
        """
        ui transition rules over appstate context
        """
        pass
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


Div_ = genStubFunc(jp.Div, sty.div)
P_ = genStubFunc(jp.P, sty.P)
A_ = genStubFunc(jp.A, sty.A)
Label_ = genStubFunc(jp.Label, sty.label)
Circle_ = genStubFunc(jp.Button, sty.circle)
Span_ = genStubFunc(jp.Span, sty.span)
InputChangeOnly_ = genStubFunc(jp.InputChangeOnly, sty.input)
Input_ = genStubFunc(jp.Input, sty.input)
Td_ = genStubFunc(jp.Td, sty.td)
Divider_ = genStubFunc(jp.Hr, sty.hr)




                
# use glossy=True,
# size="sm", label=label, value =False for toggle btn
ToggleBtn_ = genStubFunc(jp.QToggle, sty.togglebtn)
Textarea_ = genStubFunc(jp.Textarea, sty.textarea)
Option_ = genStubFunc(jp.Option, sty.option)
Container_ = genStubFunc(HCC, sty.container)
StackV_ = genStubFunc(HCC, sty.stackv)
StackH_ = genStubFunc(HCC, sty.stackh)
StackW_ = genStubFunc(HCC, sty.stackw)
StackD_ = genStubFunc(StackD, sty.stackd)
# sty will be set in StackG:init using num_rows, num_cols keyword arguments
StackG_ = genStubFunc(StackG, [])
Nav_ = genStubFunc(Nav, sty.nav)

Footer_ = genStubFunc(Footer, sty.footer)



@trackStub
def SubheadingBanner_(key: AnyStr, heading_text: AnyStr, pcp: List = [], heading_text_sty=sty.subheading_text,  **kwargs):
    # = genStubFunc(jp.Div, sty.subheading_box)
    spanl_ = Span_("headingL", text=heading_text, pcp=heading_text_sty)
    spanm_ = Span_("headingR", text=heading_text, pcp=[
        *heading_text_sty, "invisible"])
    spanx_ = Span_("headingR", text=heading_text, pcp=[
        *heading_text_sty, "invisible"])
    spanr_ = Span_("headingR", text=heading_text, pcp=[
        *heading_text_sty, "invisible"])
    return Stub(key,
                jp.Div,
                twsty_tags=[*pcp, *sty.subheading_box],
                postrender=lambda dbref,  spanl_=spanl_, spanm_=spanm_, spanr_=spanr_: spanr_(spanx_(spanm_(spanl_(dbref)))),
                **kwargs)


@trackStub
def LabeledInput_(key: AnyStr, label: AnyStr, placeholder: AnyStr,  changeonly=True, input_type="text", pcp=[], **kwargs):
    span_ = Span_("iname", text=label, pcp=sty.span)
    if changeonly:
        input_ = InputChangeOnly_(
            "input", placeholder=placeholder, type=input_type)
    else:
        input_ = Input_("input", placeholder=placeholder, type=input_type)
    return Stub(key, jp.Label, twsty_tags=[*pcp, *sty.label], postrender=lambda dbref, span_=span_, input_=input_: input_(span_(dbref)))

@trackStub
def Checkbox_(key:AnyStr, placeholder:AnyStr, val=False, pcp=[], **kwargs):
    cbox_ = Input_(f"{key}cbox", type='checkbox',  value=val,
                   pcp=['form-checkbox'])
    span_ = Span_(f"{key}span", text=placeholder, pcp=[fz.sm])
    return Stub(key, jp.Label, twsty_tags=[*pcp, *sty.label], postrender=lambda dbref, span_=span_, cbox_=cbox_: cbox_(span_(dbref)))
    

@trackStub
def CheckboxInput_(key: AnyStr, placeholder: AnyStr, pcp=[], **kwargs):
    # TODO: make form-checkbox firstclass
    cbox_ = Input_(f"{key}cbox", type="checkbox", pcp=['form-checkbox'])
    input_ = InputChangeOnly_(f"{key}inp", type="text", placeholder=placeholder)
    return Stub(key, jp.Label, twsty_tags=[*pcp, *sty.label], postrender=lambda dbref, cbox_=cbox_, input_=input_: input_(cbox_(dbref)), **kwargs)


@trackStub
def Subsection_(key: AnyStr, heading_text: AnyStr, content_: Callable, pcp=[], **kwargs):
    return StackV_(key, cgens=[SubheadingBanner_(
        "heading", heading_text), Halign_(content_)], pcp=pcp, **kwargs)

def Prose_(key:AnyStr, text:AnyStr, pcp=[], **kwargs):
    return P_(key, text=text, pcp = [*pcp, *sty.prose], **kwargs)
                   
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
        "heading", heading_text), Halign_(content_)], pcp=pcp, **kwargs)


def WithBanner_(key: AnyStr, banner_text: AnyStr, component_: Callable, pcp: List = [], **kwargs):
    return StackH_(key, cgens=[Span_("banner", text=banner_text), component_], pcp=pcp, **kwargs)




@trackStub
def Halign_(content_: Callable, align="center", pcp=[], **kwargs):
    """
    tstub: target stub, i.e., the one needs to be aligned
    """
    return Stub(f"Halign{content_.key}",  jp.Div, twsty_tags=[
        *pcp, *sty.halign(align)],     postrender=lambda dbref, tstub=content_: tstub(dbref), **kwargs)


@trackStub
def ExpansionContainer_(key: AnyStr, label: AnyStr, content_: AnyStr, pcp: List=[]):
    return Stub(key, jp.QExpansionItem, twsty_tags=[*pcp, *sty.expansion_container], postrender=lambda dbref, tstub=content_:tstub(dbref), dense=True, header_class='bg-grey-1', label=label,)



# TODO: implement default value
def Title_(key:AnyStr, title_text:AnyStr, pcp=[], align="center", **kwargs):
    return Halign_(Span_(key, text=title_text, pcp=[*sty.title_text, *pcp]), align=align)
                   

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
        # pass the selection to parent component
        dbref.colorSelector.maincolor_value = msg.value
        colortag = sty.get_color_tag(dbref.colorSelector.maincolor_value)
        dbref.colorSelector.component_clicked = 'mainColorSelector'
        pass
    mainColorSelector_ = MainColorSelector_("MainColorSelector").event_handle(
        EventType.click, on_main_color_select)

    def on_slider_select(dbref, msg):
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
    return Stub(key, jp.Form, twsty_tags=[*sty.form, *pcp], postrender=postrender, **kwargs)


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
def Tr_(key, cgens, isodd=True, pcp=[], **kwargs):
    return Stub(key, jp.Tr, twsty_tags=[*sty.tr[isodd], *pcp], postrender=lambda dbref, cgens=cgens: [_(dbref) for _ in cgens], **kwargs)


@trackStub
def Table_(key, cgens, pcp=[], **kwargs):
    return Stub(key, jp.Table, twsty_tags=[*sty.tbl, *pcp], postrender=lambda dbref, cgens=cgens: [_(dbref) for _ in cgens], **kwargs)

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
def WebPage_(key: AnyStr,  head_html_stmts: List[AnyStr] = [], cgens: List = [], WPtype: Type[jp.WebPage] = jp.WebPage, pcp = [], **kwargs):
    """
    WPtype: the WebPage class, either jp.WebPage or derived from it, jp.QuasarPage, or ojr.WebPage, 
    """
    def postrender(wp, cgens=cgens):
        # TODO: declare session manager here
        #wp.tailwind = False  # we inject our tailwind
        # not yet able to inject our own tailwind
        wp.tailwind = True  # we inject our tailwind

        wp.head_html = "\n".join(head_html_stmts)
        #tailwind comes bundled with svelte
        # wp.head_html = "\n".join([*head_html_stmts,
        #                           """<link rel = "stylesheet" href = "https://cdn.jsdelivr.net/npm/inter-ui@3.13.1/inter.min.css" > """,
        #                           """ <script src = "https://cdn.tailwindcss.com/" > </script >"""
        #                           ])
        # wp.head_html = "\n".join(head_html)
        wp.css = 'body { font-family: Inter; }'
        wp.body_classes = tstr(*wp.twsty_tags)



    stub = WPStub(key, WPtype, twsty_tags=[
            *sty.wp, *pcp], postrender=postrender, cgens=cgens, **kwargs)
    
    # if page_type == 'tailwind':
    #     stub = WPStub(key, WPtype, twsty_tags=[
    #         *sty.wp], postrender=postrender, cgens=cgens, **kwargs)
    # elif page_type == 'quasar':
    #     stub = WPStub(key, jp.QuasarPage, twsty_tags=[
    #         *sty.wp], postrender=postrender, cgens=cgens,  **kwargs)
    return stub


