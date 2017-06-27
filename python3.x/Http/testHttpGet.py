from http import client
from FundParser import FundParser
import json

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

def do_it():
	code = '070002'
	size = 1

	url = gen_fetch_url(code, size)
	row_data = invoke_http_get(url)
	j_data = gen_json_format(row_data)
	(content, records, pages, curpage) = parse_json(j_data)	
	fund_data = parse_html(content)
	print(fund_data)	
	# print(records)
	# print(pages)
	# print(curpage)

if __name__ == '__main__':
	do_it()