#!/usr/bin/python3

import requests
import json
import typer

'''
@click.command()
@click.option('--check', help='Requires one of --zone, --record, or --ip. Default is --ip')
@click.option('--update', help='Requires one of --zone or --record')
@click.option('--delete', help='Requires one of --zone or --record')
@click.argument('ip')
@click.argument('zone')
@click.argument('key')
@click.argument('rec')
@click.argument('rrtype')
'''

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
    zone_info_get = requests.get(('https://dns.api.gandi.net/api/v5/domains/' + zone + '/records'),
                                 headers=zone_headers)
    zone_json = zone_info_get.json()
    for item in zone_json:
        typer.echo(json.dumps(item))


@naymzap.command()
def get_record(zone: str, dom_rec_name: str):
    zone_headers = {"X-Api-Key": get_gandi_key()}
    zone_parms = {"rrset_type": dom_rec_name}
    zone_rec_get = requests.get(('https://dns.api.gandi.net/api/v5/domains/' + zone + '/records/' + dom_rec_name),
                                headers=zone_headers, params=zone_parms)
    typer.echo(zone_rec_get.json())


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


if __name__ == "__main__":
    naymzap()

