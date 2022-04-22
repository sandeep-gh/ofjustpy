import logging
import os
if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

import json
import logging
import os
import traceback
import typing
from itertools import tee
from typing import get_type_hints
import functools
import jsbeautifier
from typing import Any, NamedTuple
from addict import Dict

# This is a global variable
curr_session_ctx = None

#from webapp_framework_tracking.dbrefBoard import register as dbrefBoard_register


#_hcs = Dict()
#refBoard = Dict(track_changes=True)
#_currTracker = _hcs
#_currSpath = "/"
#session_dict = Dict(track_changes=True)
#session_dict.model = Dict(track_changes=True)


# def build_hcdbref():
#     """build a replica for _hcs
#     but with values as dbref instead of stub
#     """
#     hcdbref = Dict()
#     for k, v in walker(_hcs):
#         dnew(hcdbref, k, v.key)

#     return hcdbref


# def get_sref(spath):
#     return dget(_currTracker, spath)


# def get_dbref(spath):
#     """spath: stub path
#     """
#     hcgen = dget(_currTracker, spath)

#     return hcgen.target

# def save_sty(model: Dict, arg: Dict):
#     logger.debug("In save sty")
#     styreport = session_dict['styj']
#     opts = jsbeautifier.default_options()
#     res = jsbeautifier.beautify(json.dumps(session_dict['styj']), opts)
#     with open("styreport.json", "w") as fh:
#         fh.write(res)
#     pass


# def load_sty(model: Dict, arg: Dict):
#     logger.debug("loading sty")
#     with open("styreport.json", "r") as fh:
#         session_dict['styj'] = Dict(json.loads(fh.read()))


# class uictx:
#     def __init__(self, ctx, **kwargs):

#         self.ctx = ctx
#         pass

#     def __enter__(self):
#         global _currTracker
#         global _currSpath
#         if self.ctx not in _currTracker:
#             _currTracker[self.ctx] = Dict()
#         self.pctx = _currTracker
#         self.pspath = _currSpath
#         _currTracker = _currTracker[self.ctx]
#         _currSpath = _currSpath + f"{self.ctx}/"
#         return _currTracker

#     def __exit__(self, type, value, traceback):
#         global _currTracker
#         global _currSpath
#         _currTracker = self.pctx
#         _currSpath = self.pspath
#         pass


def get_session_manager(session_id):
    session_ctx = Dict()
    session_ctx.stubStore = Dict(track_changes=True)
    session_ctx.refBoard = Dict(track_changes=True)
    session_ctx.appstate = Dict(track_changes=True)

    class uictx:
        _currTracker = session_ctx.stubStore
        _currSpath = "/"

        def __init__(self, ctx, **kwargs):
            self.ctx = ctx
            pass

        def __enter__(self):
            #global _currTracker
            #global _currSpath
            if self.ctx not in uictx._currTracker:
                uictx._currTracker[self.ctx] = Dict()
            self.pctx = uictx._currTracker
            self.pspath = uictx._currSpath
            uictx._currTracker = uictx. _currTracker[self.ctx]
            uictx._currSpath = uictx._currSpath + f"{self.ctx}/"
            return uictx._currTracker

        def __exit__(self, type, value, traceback):
            #global _currTracker
            #global _currSpath
            uictx._currTracker = self.pctx
            uictx._currSpath = self.pspath
            pass

    session_ctx.uictx = uictx
    #input_, button_

    def track_stubGen_wrapper(func, *args, **kwargs):
        """
        a wrapper over stub generator function to track 
        it
        """
        # TODO: put check for arguments to the stub
        if 'DEBUG_WEBAPP' in os.environ:
            type_hints = get_type_hints(func)
            # this function takes a stub as argument
            if "content_" in type_hints or "input_" in type_hints or "button_" in type_hints:
                for argname, argval in zip(type_hints.keys(), args):
                    if argname in ['content_', ' input_',  'button_']:
                        if isinstance(argval, Dict):
                            print(
                                "aha -- got dict instead of stub; you mistyped fatso")
                            print(traceback.format_exc())
                            raise ValueError("Got empty dict instead of stub")

            if 'cgens' in kwargs:
                cgens = kwargs.pop('cgens')
                if isinstance(cgens, typing.List):
                    cgens_c = cgens

                else:
                    cgens, cgens_c = tee(cgens)

                for idx, cgen in enumerate(cgens_c):
                    if isinstance(cgen, Dict):
                        print(
                            f"aha -- got dict instead of stub; you mistyped fatso finger at array position {idx}")
                        print(traceback.format_exc())
                        raise ValueError("Got empty dict instead of stub")

                kwargs['cgens'] = cgens
        stub = func(*args, **kwargs)
        uictx._currTracker[stub.key] = stub
        stub.spath = uictx._currSpath + stub.key
        #logger.debug(f"adding {hcgen.key} to tracking at {hcgen.spath}")
        return stub

    session_ctx.track_stubGen_wrapper = track_stubGen_wrapper
    return session_ctx


class sessionctx:
    def __init__(self, session_ctx, **kwargs):
        global curr_session_ctx
        if curr_session_ctx is not None:
            raise ValueError(
                f"Fatal error: building new session ctx within an existing one {curr_session_ctx} {session_ctx}")

        curr_session_ctx = session_ctx
        print("current session context is set")
        pass

    def __enter__(self):
        print("entering the context")
        return

    def __exit__(self, type, value, traceback):
        global curr_session_ctx
        print("exit a session context")
        curr_session_ctx = None
        pass


def trackStub(func):
    """
    register the stub in _hcs/stubStore
    """
    @functools.wraps(func)
    def stubGen_wrapper(*args, **kwargs):
        return curr_session_ctx.track_stubGen_wrapper(func, *args, **kwargs)

    return stubGen_wrapper


# def hcGen_register(func):
#     @functools.wraps(func)
#     def hcGen_wrapper(*args, **kwargs):
#         """
#         wrapper for _f/generator function in htmlcomponents
#         """
#         if args and args[0] == None:  # skip the _f(None) call
#             return func(*args, **kwargs)

#         hcref = func(
#             *args, **kwargs)  # this is the chance to add dbref to dbrefBoard
#         # we store the stub/func; use func.target
#         # print("register ", func, " ", hcref.stub, " ", hcref.key)
#         # TODO: pick it up: its a mystry why func !=
#         # dbrefBoard.register(refBoard, func, hcref)
#         dbrefBoard_register(refBoard, hcref.stub, hcref)
#         return hcref

#     return hcGen_wrapper


# def register(func):
#     """
#     register the stub in _hcs/stubStore
#     """
#     @functools.wraps(func)
#     def stubGen_wrapper(*args, **kwargs):

#         if 'DEBUG_WEBAPP' in os.environ:

#             type_hints = get_type_hints(func)
#             if "content_" in type_hints:  # this function takes a stub as argument
#                 for argname, argval in zip(type_hints.keys(), args):
#                     if argname == 'content_':
#                         if isinstance(argval, Dict):
#                             print(
#                                 "aha -- got dict instead of stub; you mistyped fatso")
#                             print(traceback.format_exc())
#                             raise ValueError("Got empty dict instead of stub")

#             if 'cgens' in kwargs:
#                 cgens = kwargs.pop('cgens')
#                 if isinstance(cgens, typing.List):
#                     cgens_c = cgens

#                 else:
#                     cgens, cgens_c = tee(cgens)

#                 for idx, cgen in enumerate(cgens_c):
#                     if isinstance(cgen, Dict):
#                         print(
#                             f"aha -- got dict instead of stub; you mistyped fatso finger at array position {idx}")
#                         print(traceback.format_exc())
#                         raise ValueError("Got empty dict instead of stub")

#                 kwargs['cgens'] = cgens
#         hcgen = func(*args, **kwargs)
#         _currTracker[hcgen.key] = hcgen
#         hcgen.spath = _currSpath + hcgen.key
#         logger.debug(f"adding {hcgen.key} to tracking at {hcgen.spath}")
#         return hcgen

#     return stubGen_wrapper


# def tag2path(*args):
#     print("in tag2path ", _currSpath, " ", _currTracker)
#     print("in tag2path ", _hcs.keys())
