"""
drop down color not working in firefox
"""

#from tailwind_tags import *
from tailwind_tags import bg, blue, bd, bdr, gray, H, W, full, pd, jc
import ofjustpy as oj
from addict import Dict
import justpy as jp
def on_btn_click(dbref,msg):
    print ("clicked ", msg.value)
    pass

request = Dict()
request.session_id = "abc"

def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        colorselector_ = oj.ColorSelector_(
            "colorselector", pcp=[jc.start, W/"1/2"]).event_handle(
                        oj.click, on_btn_click)

        eq_ = oj.Span_("eqt", text=":", pcp=[jc.center])
        label_= oj.Span_("aspan", text="a big long text", pcp=[jc.end, W/"1/2"])
        r1_ = oj.StackH_("r1", cgens=[ label_, eq_, colorselector_], pcp=[W/full])
        
        records_ = oj.Align_(oj.StackV_("records", cgens=[r1_, r1_]))
        
        wp_ = oj.WebPage_("oa", cgens =[records_], template_file='svelte.html', title="myoa")

        wp = wp_()
        wp.session_manager = session_manager
    return wp

#jp.Route("/", launcher)



app = jp.app
jp.justpy(launcher, start_server=False)

# request = Dict()
# request.session_id = "abc"

# wp = launcher(request)
# from aenum import Enum
# def get_attribute_value(twsty_tags, elabel="mr"):
#     for _ in filter(lambda _ : not isinstance(_, Enum), twsty_tags):
#         if _.elabel == elabel:
#             return int(_.arg2)
#     return 0


# def get_margin(twsty_tags):
#     return get_attribute_value(twsty_tags, "mr")

# def get_height(twsty_tags):
#     return get_attribute_value(twsty_tags, "H")

# def get_padding(twsty_tags):
#     return get_attribute_value(twsty_tags, "pd")

# def recurse(root):
#     child_spacings = [recurse(child_comp) for child_comp in root.components]
#     all_margins = [_cs.mr for _cs in child_spacings]
#     all_effective_heights = [_cs.effective_height  for _cs in child_spacings]
#     print ("margin and heights ", all_margins, " ", all_effective_heights, " ", root.stub.key)
#     if len(set(all_margins)) > 1:
#         print ('uneven margin at sibling=', all_margins, " ", root.stub.key)

#     if len(set(all_effective_heights)) > 1:
#         print ('uneven effective_heights for  sibling=', all_effective_heights, " ", root.stub.key)
                

#     root_margin = get_margin(root.twsty_tags)
#     root_effective_height = get_height(root.twsty_tags) + get_padding(root.twsty_tags)
#     max_mr = 0
#     if all_margins:
#         max_mr = max(all_margins)
#     max_effective_height = 0
#     if all_effective_heights:
#         max_effective_height = max(all_effective_heights)
        
#     return  Dict({'mr': max_mr + root_margin, 'effective_height': max_effective_height + root_effective_height})
# res = recurse(wp)
# _ss = wp.session_manager.stubStore
# msg = Dict()

# msg.value = 0

# _ss.myslider.target.circle_stubs[0].target.on_click(msg)
