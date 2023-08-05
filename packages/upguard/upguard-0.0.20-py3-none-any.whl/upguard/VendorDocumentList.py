import json
from .BaseObject import BaseObject
from .VendorDocument import VendorDocument

class VendorDocumentList(BaseObject):

    def __init__(self, api_key):
        BaseObject.__init__(self, api_key)
        self.inner_list = []


