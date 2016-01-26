#!/usr/bin/env python

from elasticsearch import Elasticsearch
import json
import click

@click.group(chain=True)
@click.option('--raw-result/--no-raw-result', default=False)
@click.option('--show', default=5, help='Number of results to display')

def cli():
	""" This script play as a client of Elasticsearch, one powerful search engine,
		for searching metadata of GEO database
	
		Example:
		gem bla bla bla
		gem blo blo blo
	"""
		
@cli.resultcallback()
def process_commands(processors):
	""" """
	# Start with an iterable
	stream = ()
	
	# Pipe it through all stream processors
	for processor in processors:
		stream  = processor(stream)
	
	#Evaluate the stream and through away the items
	for _ in stream:
		pass

def generator(f):
	@processor
	""" similar to processors """
	def new_func(stream, *args, **kwargs):
		for item in stream:
			yield item
		for item in f(*args, **kwargs):
			yield item
	return update_wrapper(new_func, f)

def copy_filename(new, old):
	new.filename = old.filename
	return new

@click.command('general')
@click.argument('query', required=False)
@click.option('--from-json')
def search(query, from_json, raw_result, show):
	es = Elasticsearch()
	if from_json:
		matches = es.search(index='metadata',doc_type='paper', q=json.load(from_json), size=show)
	elif query:
		matches = es.search(index='metadata', doc_type='paper', q=query, size=show)
	else:
		return 1
	hits = matches['hits']['hits']
	if not hits:
		click.echo('No matches found')
	else:
		if raw_result:
			click.echo(json.dumps(matches, indent=4))
		for hit in hits:
			click.echo('===========\nGSE:{}\nTitle:{}\nDesign:{}\nSubmission:{}\nContact:{}\n==========='.format(
				hit['_source']['geo'],
				hit['_source']['title'].encode('ascii', 'ignore'),
				hit['_source']['design'].encode('ascii', 'ignore'),
				hit['_source']['submission'],
				hit['_source']['contact'].encode('ascii', 'ignore')
			))
