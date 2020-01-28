import requests
import sys


class RestClient:

    headers = {'Content-type': 'application/json'}

    def __init__(self, base_url):
        self.__base_url = base_url

    def voucher_create(self, payload):
        url = self.__base_url + "/voucher/create"

        try:
            r = requests.post(url, data=payload, headers=RestClient.headers)
            print("POST {url}  STATUS {code}".format(url=url, code=r.status_code))
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)

    def voucher_verify(self, payload):
        url = self.__base_url + "/voucher/verify"

        try:
            r = requests.post(url, data=payload, headers=RestClient.headers)
            print("POST {url}  STATUS {code}".format(url=url, code=r.status_code))
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)

