#!/usr/bin/python3

import requests
import json

def get_my_dns():
    my_home_dns = requests.get('https://icanhazip.com')
    my_home_ptr = requests.get('https://icanhazptr.com')
    if my_home_dns.status_code == 200 and my_home_ptr.status_code == 200:
        return(my_home_ptr.text, my_home_dns.text)
    else:
        print("No records retrieved.")

def get_gandi_key():
    with open('/home/zach/.python.secrets.json', 'r') as secrets:
        secret_info = json.load(secrets)
        gandi_key = secret_info['secret_keys']['gandi_api']
    if gandi_key:
        return(gandi_key)
    else:
        print("Could not retreive key")

def get_zone_info(zone):
    zone_headers = {"X-Api-Key": get_gandi_key()}
    zone_info_get = requests.get(('https://dns.api.gandi.net/api/v5/domains/' + zone + '/records'), headers=zone_headers)
    print(zone_info_get.json())

def get_zone_sngl_record(zone, dom_rec_name):
    zone_headers = {"X-Api-Key": get_gandi_key()}
    zone_parms = {"rrset_type": dom_rec_name}
    zone_rec_get = requests.get(('https://dns.api.gandi.net/api/v5/domains/' + zone + '/records/' + dom_rec_name), headers=zone_headers, params=zone_parms)
    print(zone_rec_get.json())

def update_zone_sngl_record(zone, dom_rec_name, dom_rec_type, rec_new_val):
    # Headers required - Apikey
    zone_headers = {"Content-Type": "application/json", "X-Api-Key": get_gandi_key()}
    # data is body data - requires rrset_type - A record, etc
    # requires - rrset_values as a list
    zone_data = {"rrset_name": dom_rec_name, "rrset_type": dom_rec_type, "rrset_values": [rec_new_val]}
    zone_rec_chg = requests.put(('https://dns.api.gandi.net/api/v5/domains/' + zone + '/records/' + dom_rec_name + '/' + dom_rec_type),
                                headers=zone_headers, json=zone_data)
    print(zone_rec_chg.json())

## try the record update with the zone uuid

myptr, myip = get_my_dns()
#print("My PTR record is {}, and my IP is {}".format(myptr, myip))
get_zone_info("segfawlty.space")
#get_zone_sngl_record("segfawlty.space", "@")
#update_zone_sngl_record("segfawlty.space", "@", "A", myip)

