import webapp2
import csv
import logging

import os
import sys


from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

from google.appengine.ext import db


class MainHandler(webapp2.RequestHandler):
    def get(self):

		schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
		ix = create_in("indexdir", schema)
		writer = ix.writer()
		writer.add_document(title=u"First document", path=u"/a", content=u"This is the first document we've added!")
		writer.add_document(title=u"Second document", path=u"/b", content=u"The second one is even more interesting!")
		writer.commit()
		with ix.searcher() as searcher:
		    query = QueryParser("content", ix.schema).parse("first")
		    results = searcher.search(query)

		self.response.write(results)


app = webapp2.WSGIApplication([
    ('/', MainHandler)], debug=True)
