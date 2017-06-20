from HTMLParser import HTMLParser
import httplib
import Fund

class FundParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.links = []
		self.item = []

	def handle_starttag(self, tag, attrs):
		if tag == 'tr':
			self.item = []

	def handle_endtag(self, tag):
		if tag == 'tr':
			fund = Fund.Fund(self.item[0], self.item[1], self.item[3])
			self.links.append(fund)


	def handle_data(self, data):
		if self.lasttag == 'td':
			self.item.append(data)			



code = '070002'
size = 1
def getData(code, size):
	conn = None
	try:
		url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=%s&page=1&per=%i&sdate=&edate=&rt=0.3053546294856555' % (code, size)
		# print url
		conn = httplib.HTTPConnection('fund.eastmoney.com')
		conn.request(method='GET', url=url)
		response = conn.getresponse()
		res = response.read()
		return res.decode('utf-8').encode('gbk')
	except Exception, e:
		pass
	finally:
		if conn:
			conn.close()

def parse(content):
	lines = content.split(',')
	records = lines[1].split(':')[1]
	pages = lines[2].split(':')[1]
	currentPage = lines[3].split(':')[1].strip(';').strip('}')
	
	table = lines[0]
	body_pos = table.find('<tbody>')
	body_endpos = table.find('</tbody>')+len('</tbody)')
	tbody = table[body_pos:body_endpos]

	return (tbody, records, pages, currentPage)

# res = getData(code, size)
# print res