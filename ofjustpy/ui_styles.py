import os
from . import snowsty as snow
#from . import fancysty as fancy
from . import basesty
styles = {'snow': snow
          # , 'fancy': fancy
          }


sty = styles['snow']

if 'WFSTY' in os.environ:
    sty = styles[os.environ['WFSTY']]


def set_style(label='snow'):
    global sty
    sty = styles[label]


def check_style():
    print(sty)
