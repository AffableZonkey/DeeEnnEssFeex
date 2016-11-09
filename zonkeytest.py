#!/usr/env/python3

import xmlrpc.client

api = xmlrpc.client.ServerProxy('https://rpc.gandi.net/xmlrpc/')

apikey = 'oAFhVlciLVtLxWHVkcBVItxX'

#zonk_info = api.domain.info(apikey, 'zonkey.space')
#print(zonk_info)

#zonk_zones = api.domain.zone.record.list(apikey, 2357283, 2)
#print(zonk_zones)


def zone_clone(zone_id):
    clone_result = api.domain.zone.clone(apikey, zone_id)
    return clone_result

def zone_change_ip(zone_id, ip_address, version):
    zone_ip_res = api.domain.zone.record.set(apikey, zone_id, version,
            [
                { "type" : "A", "name": "@", "value": ip_address }
            ])
    return zone_ip_res

def zone_add_record(zone_id, version, record_dict):
    zone_recadd_res = api.domain.zone.record.add(apikey, zone_id, version, record_dict)
    return zone_recadd_res


    
