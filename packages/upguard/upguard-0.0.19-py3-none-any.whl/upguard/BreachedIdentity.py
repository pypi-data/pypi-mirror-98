import json

from .BaseObject import BaseObject

class BreachedIdentity(BaseObject):

    def __init__(self, api_key):
        BaseObject.__init__(self, api_key)
        self.brached_identities = None
        self.breaches = None
