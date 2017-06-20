import json

config = open('Fund.conf')
jsonConfig = json.load(config)
config.close()

sections = jsonConfig.keys()
for s in sections:
	print s, jsonConfig[s]['name'], jsonConfig[s]['code']


