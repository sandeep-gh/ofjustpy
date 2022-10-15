from addict import Dict
import justpy as jp
from justpy import JustpyBaseComponent
from justpy import WebPage
from tailwind_tags import *
from dpath.util import get as dget, set as dset
import hjson
from ofjustpy.htmlcomponents import genStubFunc 
import ofjustpy  as oj


chart_options = Dict(hjson.loads("""
{options: {
    title: {
      display: true,
      text: 'World population per region (in millions)'
    },
    scales : {
      x: {  title: { text: "hello", display: true}}
    }
    
  }
}"""
                                 ))

oj.dupdate(chart_options, "/options/scales/x/title/bha",  "okeke")

print (chart_options.options)


