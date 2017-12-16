#!/usr/bin/env python3
import requests
import os
import sys


class Dozens:
    def __init__(self, user, key):
        headers = {'X-Auth-User': user, "X-Auth-Key": key}
        r = requests.get(url="http://dozens.jp/api/authorize.json", headers=headers)
        r.raise_for_status()

        self._auth_token = r.json()["auth_token"]

    def call_get(self, url):
        headers = {'X-Auth-Token': self._auth_token}
        r = requests.get(url=url, headers=headers)
        r.raise_for_status()
        return r.json()

    def call_post(self, url, json_body):
        headers = {'X-Auth-Token': self._auth_token}
        r = requests.post(url=url, headers=headers, json=json_body)
        r.raise_for_status()
        return r.json()

    def call_delete(self, url):
        headers = {'X-Auth-Token': self._auth_token}
        r = requests.delete(url=url, headers=headers)
        r.raise_for_status()
        return r.json()


def find_record(dozens: Dozens, name: str, domain: str, type: str):
    records = dozens.call_get("http://dozens.jp/api/record/{0}.json".format(domain))

    if name is None:
        fqdn = domain
    else:
        fqdn = "{0}.{1}".format(name, domain)

    return next( (r["id"] for r in records["record"]
                  if r["name"] == fqdn and r["type"]==type), None)


def present_record(dozens: Dozens, name: str, domain: str, type: str, content: str):
    id = find_record(dozens, name, domain, type)
    if id is None:
        json = {"domain": domain,
        "name": name,
        "type": type,
        "prio": 10,
        "content": content,
        "ttl": "7200"}

        results = dozens.call_post("http://dozens.jp/api/record/create.json", json_body=json)
    else:
        json = {"prio": 10,
                "content": content,
                "ttl": 7200}
        results = dozens.call_post("http://dozens.jp/api/record/update/{0}.json".format(id), json_body=json)


def absent_record(dozens: Dozens, name: str, domain: str, type: str):

    while True:
        id = find_record(dozens, name, domain, type)
        if id is None:
            break
        results = dozens.call_delete("http://dozens.jp/api/record/delete/{0}.json".format(id))
