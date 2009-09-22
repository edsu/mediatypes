import sys
sys.path.insert(0, 'lib')

import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import memcache

import models

from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef, Literal
from rdflib.namespace import Namespace, RDF, RDFS

memcache_ttl = 60 * 60 # 1 hr

class MyRequestHandler(webapp.RequestHandler):
    def render(self, template_file, context):
        self.response.out.write(template.render(template_file, context))

    def host(self):
        return self.request.headers['HOST']

class Home(MyRequestHandler):
    def get(self):
        host = self.host()
        types = fetch_types()
        return self.render('templates/home.html', locals())

class Type(MyRequestHandler):
    def get(self, type):
        title = "%s/*" % type
        types = fetch_types()
        media_types = fetch_mediatypes(type)
        return self.render('templates/type.html', locals())

class MediaType(MyRequestHandler):
    def get(self, type, subtype):
        types = fetch_types()
        subtype = urllib.unquote(subtype)
        mt = db.Query(models.MediaType).filter('type =', type).filter('subtype =', subtype).get()
        if not mt:
            title = "Not Found"
            message = "%s/%s not found" % (type, subtype)
            return self.render('templates/404.html', locals())
        title = mt.name
        return self.render('templates/mediatype.html', locals())

class Dump(MyRequestHandler):
    def get(self):
        g = ConjunctiveGraph()
        ns = Namespace('http://purl.org/NET/mediatype#')
        for mt in models.MediaType.all():
            g.add((URIRef(mt.uri), RDF.type, ns['MediaType']))
            g.add((URIRef(mt.uri), RDFS.label, Literal(mt.name)))
            if mt.rfc_url:
                g.add((URIRef(mt.uri), RDFS.seeAlso, URIRef(mt.rfc_url)))
            if mt.application_url:
                g.add((URIRef(mt.uri), RDFS.seeAlso, URIRef(mt.application_url)))
        self.response.headers['Content-Type'] = 'application/rdf+xml'
        g.serialize(self.response.out)

class Robots(MyRequestHandler):
    def get(self):
        host = self.host()
        self.response.headers['Content-Type'] = 'text/plain'
        self.render('templates/robots.txt', locals())

class Sitemap(MyRequestHandler):
    def get(self):
        host = self.host()
        media_types = models.MediaType.all()
        self.response.headers['Content-Type'] = 'text/xml'
        self.render('templates/sitemap.xml', locals())

def fetch_types():
    types = memcache.get("types")
    if not types:
        types = list(set([mt.type for mt in models.MediaType.all()]))
        types.sort()
        memcache.add("types", types, memcache_ttl)
    return types

def fetch_mediatypes(type):
        media_types = memcache.get(type)
        if not media_types:
            media_types = models.MediaType.gql("WHERE type = :1 ORDER BY name", 
                                               type)
            memcache.add(type, media_types, memcache_ttl)
        return media_types

urls = [
        ('/dump.rdf', Dump),
        ('/robots.txt', Robots),
        ('/sitemap.xml', Sitemap),
        (r'/(.+)/(.+)$', MediaType),
        (r'/(.+)$', Type),
        (r'/', Home),
       ]

application = webapp.WSGIApplication(urls, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
