#!/usr/bin/python3

import requests
import json
import typer
import sys

naymzap = typer.Typer()


@naymzap.command()
def get_ip():
    home_dns = requests.get('https://icanhazip.com')
    home_ptr = requests.get('https://icanhazptr.com')
    if home_dns.status_code == 200 and home_ptr.status_code == 200:
        typer.echo(f"IP {home_dns.text} and PTR {home_ptr.text} found")
        return (home_ptr.text, home_dns.text)
    else:
        typer.echo("No records retrieved.")
        pass


def get_gandi_key():
    with open('/home/zach/.python.secrets.json', 'r') as secrets:
        secret_info = json.load(secrets)
        gandi_key = secret_info['secret_keys']['gandi_api']
    if gandi_key:
        return (gandi_key)
    else:
        print("Could not retreive key")


@naymzap.command()
def get_zone_info(zone: str):
    zone_headers = {"X-Api-Key": get_gandi_key()}
    try:
        zone_info_get = requests.get(('https://dns.api.gandi.net/api/v5/domains/' + zone + '/records'),
                                     headers=zone_headers)
    except requests.exceptions.RequestException as e:
        typer.echo(e, f'Naymzap Failed: {} ')
        sys.exit(1)
    if zone_info_get.status_code == 200:
        return zone_info_get.json()
    else:
        typer.echo('Not my fault, the internet fell over.')
#   for item in zone_json:
#       typer.echo(json.dumps(item))


@naymzap.command()
def get_record(zone: str, dom_rec_name: str):
    zone_headers = {"X-Api-Key": get_gandi_key()}
    zone_parms = {"rrset_type": dom_rec_name}
    try:
        zone_rec_get = requests.get(('https://dns.api.gandi.net/api/v5/domains/' + zone + '/records/' + dom_rec_name),
                                    headers=zone_headers, params=zone_parms)
    except requests.exceptions.RequestException as e:
        typer.echo(e, f'Naymzap Failed: {} ')
        sys.exit(1)
    if zone_rec_get.status_code == 200:
        return zone_rec_get.json()
    else:
        typer.echo('Not my fault, there was a hole in the bits bucket.')


@naymzap.command()
def update_record(zone: str, dom_rec_name: str, dom_rec_type: str, rec_new_val: str):
    # Headers required - Apikey
    zone_headers = {"Content-Type": "application/json", "X-Api-Key": get_gandi_key()}
    # data is body data - requires rrset_type - A record, etc
    # requires - rrset_values as a list
    zone_data = {"rrset_name": dom_rec_name, "rrset_type": dom_rec_type, "rrset_values": [rec_new_val]}
    zone_rec_chg = requests.put(
        ('https://dns.api.gandi.net/api/v5/domains/' + zone + '/records/' + dom_rec_name + '/' + dom_rec_type),
        headers=zone_headers, json=zone_data)
    typer.echo(zone_rec_chg.json())

@naymzap.command()
def auto_dns_fix(domain: str,):
    zone_records = get_zone_info(domain)
    ptr, ip_addr = get_ip()
    for record in zone_records:
        if record.rrset_type and record.rrset_type == "A":
            if ip_addr not in record.rrset_values.iteritems() and len(record.rrset_values) <= 1:
                update_record(domain, record.dom_rec_nam, dom_rec_type, ip_addr)
            else:
                typer.echo('I oopsied')
        else:
            continue

if __name__ == "__main__":
    naymzap()

