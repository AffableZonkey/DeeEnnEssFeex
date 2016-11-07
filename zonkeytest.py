#!/usr/env/python3

import xmlrpc.client

api = xmlrpc.client.ServerProxy('https://rpc.gandi.net/xmlrpc/')

apikey = 'oAFhVlciLVtLxWHVkcBVItxX'

zonk_info = api.domain.info(apikey, 'zonkey.space')
print(zonk_info)

