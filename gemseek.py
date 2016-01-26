#!/usr/bin/env python

from elasticsearch import Elasticsearch
from functools import update_wrapper
import json
import click

class Configuration(object):
	def __init__(self):
		self.show = 5
		self.raw_result = False

pass_conf = click.make_pass_decorator(Configuration, ensure = True)

@click.group(chain=True)
@click.option('--raw-result/--no-raw-result', default=False)
@click.option('--show', default=5, help='Number of results to display')
@click.pass_context

def cli(conf, raw_result, show):
	""" This script play as a client of Elasticsearch, one powerful search engine,
		for searching metadata of GEO database
	
		Example:
		gem general John+USA
		gem general GSE10195

	"""
	conf.obj = Configuration()
	conf.obj.raw_result = raw_result
	conf.obj.show = show
		

##########'general' command for searching general, combined terms################
@cli.command('general')
@click.argument('query', required=False)
@click.option('--from-json')
@pass_conf

def general_cmd(conf,query, from_json):
	'''Generally search for combined and individual terms
	'''
	es = Elasticsearch()
	if from_json:
		matches = es.search(index='metadata',doc_type='paper', q=json.load(from_json), size=conf.show)
	elif query:
		matches = es.search(index='metadata', doc_type='paper', q=query, size=conf.show)
	else:
		return 1
	hits = matches['hits']['hits']
	if not hits:
		click.echo('No matches found')
	else:
		if conf.raw_result:
			click.echo(json.dumps(matches, indent=4))
		for hit in hits:
			click.echo('===========\nGSE:{}\nTitle:{}\nDesign:{}\nSubmission:{}\nContact:{}\n==========='.format(
				hit['_source']['geo'],
				hit['_source']['title'].encode('ascii', 'ignore'),
				hit['_source']['design'].encode('ascii', 'ignore'),
				hit['_source']['submission'],
				hit['_source']['contact'].encode('ascii', 'ignore')
			))

@cli.command('AuthornRelevant')
@click.argument('author', required = True)
@click.argument('relevant', required = True)
@pass_conf

def AnR_cmd(conf, author, relevant):
	'''Shows research of <author> that relevant to <relevant>'''
	es = Elasticsearch()
	#Query body
	query = '(contact:%s OR contributors:%s) AND (summary:%s OR design:%s OR title:%s)' %(author, author, relevant, relevant, relevant)
	
	matches = es.search(index='metadata', doc_type='paper', q=query, size=conf.show)
	hits = matches['hits']['hits']
	if not hits:
		click.echo('No matches found')
	else:
		if conf.raw_result:
			click.echo(json.dumps(matches, indent=4))
		for hit in hits:
			click.echo('===========\nGSE:{}\nTitle:{}\nDesign:{}\nSubmission:{}\nContact:{}\n==========='.format(
				hit['_source']['geo'],
                hit['_source']['title'].encode('ascii', 'ignore'),
                hit['_source']['design'].encode('ascii', 'ignore'),
                hit['_source']['submission'],
                hit['_source']['contact'].encode('ascii', 'ignore')
            ))

@cli.command('BeforeAfter')
@click.option('--after', default='2000-01-01')
@click.option('--before', default='2030-01-01')
@click.option('--relevant')
@pass_conf

def fromto(conf, after, before, relevant):
	'''Shows research of <author> that relevant to <relevant>'''
    es = Elasticsearch()
    #Query body , need to check format of datetime
	after = after.replace("-","")
	before = before.replace("-","")
	if relevant:
    	query = 'public:[%s TO %s] AND summary:%s' %(after, before, relevant)
	else:
		query = 'public:[%s TO %s]' %(after, before)

    matches = es.search(index='metadata', doc_type='paper', q=query, size=conf.show)
    hits = matches['hits']['hits']
    if not hits:
        click.echo('No matches found')
    else:
        if conf.raw_result:
            click.echo(json.dumps(matches, indent=4))
        for hit in hits:
            click.echo('===========\nGSE:{}\nTitle:{}\nDesign:{}\nSubmission:{}\nContact:{}\n==========='.format(
                hit['_source']['geo'],
                hit['_source']['title'].encode('ascii', 'ignore'),
                hit['_source']['design'].encode('ascii', 'ignore'),
                hit['_source']['submission'],
				hit['_source']['contact'].encode('ascii', 'ignore')
            ))
