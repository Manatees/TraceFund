from html.parser import HTMLParser
from http import client
import json
import time
from .httplib import geturl

class FundParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.content = []
		self.item = []

	def handle_starttag(self, tag, attrs):
		if tag == 'tr':
			self.item = []

	def handle_endtag(self, tag):
		if tag == 'tr':
			if len(self.item) > 1:				
				self.content.append(self.item)

	def handle_data(self, data):
		if self.lasttag == 'td':
			self.item.append(data)


def gen_fetch_url(code, size):
	return 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=%s&page=1&per=%i&sdate=&edate=&rt=0.3053546294856555' % (code, size)

def invoke_http_get(url):
	conn = client.HTTPConnection('fund.eastmoney.com')
	conn.request('get', url)
	response = conn.getresponse()
	row_data = response.read()
	return row_data.decode()

def gen_json_format(content):
	j = content[12:-1].replace('content', '"content"').replace('records', '"records"').replace('pages', '"pages"').replace('curpage', '"curpage"')
	return j

def parse_json(json_content):
	j_data = json.loads(json_content)
	return (
		j_data['content'],
		j_data['records'],
		j_data['pages'],
		j_data['curpage'],
	)

def parse_html(html_content):
	parser = FundParser()
	parser.feed(html_content)
	return parser.content

def do_it(code, size):	
	url = gen_fetch_url(code, size)
	row_data = invoke_http_get(url)
	j_data = gen_json_format(row_data)
	(content, records, pages, curpage) = parse_json(j_data)	
	fund_data = parse_html(content)
	
	# print(fund_data[0][0])
	# print(len(fund_data[0]))	

	# print('records: %s' % records)
	# print('pages: %s' % pages)
	# print('curpage: %s' % curpage)
	return fund_data

def estimated_value(fund_code): 	
	url = 'http://fundgz.1234567.com.cn/js/%s.js?rt=1499740350966' % fund_code
	d = geturl(url).decode()
	valid_data = d[d.find('{'):d.find('}')+1]
	dt = json.loads(valid_data)
	return dt