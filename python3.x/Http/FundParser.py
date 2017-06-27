from html.parser import HTMLParser

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
			if len(self.item) > 0:				
				self.content.append(self.item)

	def handle_data(self, data):
		if self.lasttag == 'td':
			self.item.append(data)
