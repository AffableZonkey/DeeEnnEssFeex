#!/usr/bin/python3

import requests
import json
import click

@click.command()
@click.option('--check', help='Requires one of --zone, --record, or --ip. Default is --ip')
@click.option('--update', help='Requires one of --zone or --record')
@click.option('--delete', help='Requires one of --zone or --record')
@click.argument('ip')
@click.argument('zone')
@click.argument('key')
@click.argument('rec')
@click.argument('rrtype')
def naymz():
    pass

def get_my_ip():
    my_home_dns = requests.get('https://icanhazip.com')
    my_home_ptr = requests.get('https://icanhazptr.com')
    if my_home_dns.status_code == 200 and my_home_ptr.status_code == 200:
#       click.echo(my_home_ptr.text, my_home_dns.text)
        return(my_home_ptr.text, my_home_dns.text)
    else:
#       click.echo("No records retrieved.")
        pass

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
    zone_json = zone_info_get.json()
    for item in zone_json:
        print(json.dumps(item))

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

myptr, myip = get_my_ip()
#print("My PTR record is {}, and my IP is {}".format(myptr, myip))
get_zone_info("segfawlty.space")
#get_zone_sngl_record("segfawlty.space", "@")
#update_zone_sngl_record("segfawlty.space", "@", "A", myip)

