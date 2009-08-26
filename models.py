import re

from google.appengine.ext import db

class MediaType(db.Model):
    name = db.StringProperty()
    type = db.StringProperty()
    subtype = db.StringProperty()
    application_url = db.StringProperty()
    rfc_url = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    def url(self):
        return "/%s/%s" % (self.type, self.subtype)

    def rfc(self):
        if self.rfc_url == None:
            return None
        m = re.search(r'rfc(\d+)', self.rfc_url)
        return m.group(1)

