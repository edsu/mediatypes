import re

from google.appengine.ext import db

class Crawl(db.Model):
    """
    A model for recording a crawl. 
    """
    created = db.DateTimeProperty(auto_now_add=True)

class MediaType(db.Model):
    name = db.StringProperty()
    type = db.StringProperty()
    subtype = db.StringProperty()
    application_url = db.StringProperty()
    rfc_url = db.StringProperty()
    obsolete = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @property
    def uri(self):
        return "http://purl.org/NET/mediatypes" + self.relative_uri

    @property
    def relative_uri(self):
        return "/%s/%s" % (self.type, self.subtype)

    @property
    def rfc(self):
        if self.rfc_url == None:
            return None
        m = re.search(r'rfc(\d+)', self.rfc_url)
        return m.group(1)

