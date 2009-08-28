import sys
sys.path.insert(0, 'lib')

import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import models

from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef, Literal
from rdflib.namespace import Namespace, RDF, RDFS

class MyRequestHandler(webapp.RequestHandler):
    def render(self, template_file, context):
        self.response.out.write(template.render(template_file, context))

class Home(MyRequestHandler):
    def get(self):
        title = 'Home'
        types = list(set([mt.type for mt in models.MediaType.all()]))
        types.sort()
        return self.render('templates/home.html', locals())

class Type(MyRequestHandler):
    def get(self, type):
        title = type
        media_types = models.MediaType.gql("WHERE type = :1 ORDER BY name", 
                                           type)
        return self.render('templates/type.html', locals())

class MediaType(MyRequestHandler):
    def get(self, type, subtype):
        subtype = urllib.unquote(subtype)
        mt = models.MediaType.gql("WHERE type = :1 AND subtype = :2",
                                  type, subtype)
        mt = mt.fetch(1)[0]
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

urls = [
        (r'/dump.rdf$', Dump),
        (r'/(.+)/(.+)$', MediaType),
        (r'/(.+)$', Type),
        (r'/', Home),
       ]

application = webapp.WSGIApplication(urls, debug=True)

def render_template(template, context):
    self.response

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
