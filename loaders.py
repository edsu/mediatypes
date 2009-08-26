from google.appengine.ext import bulkload
from google.appengine.tools import bulkloader

import sys
import os
sys.path.append(os.path.dirname(__file__))

import models

class MediaTypeLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'MediaType', 
                                   [('name', str),
                                    ('type', str),
                                    ('subtype', str),
                                    ('application_url', str),
                                    ('rfc_url', str)
                                   ])

loaders = [MediaTypeLoader]
