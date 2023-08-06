"""
    Test signing to send a transaction

"""
import json
import requests

from eth_utils import to_hex, remove_0x_prefix, to_bytes

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

PRIVATE_TEST_KEY = 0x973f69bcd654b264759170724e1e30ccd2e75fc46b7993fd24ce755f0a8c24d0
PUBLIC_ADDRESS = '5288fec4153b702430771dfac8aed0b21cafca4344dae0d47b97f0bf532b3306'

def get_test_account():
    private_key = Ed25519PrivateKey.from_private_bytes(to_bytes(PRIVATE_TEST_KEY))

    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    public_address = remove_0x_prefix(to_hex(public_key_bytes))
    assert(public_address == PUBLIC_ADDRESS)
    return private_key, public_address


def create_account(convex_url, public_address):
    account_data = {
        'accountKey': public_address,
    }
    print('create_account send', account_data)
    url = f'{convex_url}/api/v1/createAccount'
    response = requests.post(url, data=json.dumps(account_data))
    assert(response.status_code == 200)
    result = response.json()
    return result['address']

def request_funds(convex_url, address):
    faucet_data = {
        'address': address,
        'amount': 10000000
    }
    print('faucet send', faucet_data)
    url = f'{convex_url}/api/v1/faucet'
    response = requests.post(url, data=json.dumps(faucet_data))
    if response.status_code != 200:
        print('error', response.text)
        assert(response.status_code == 200)
    print('faucet response', response.json())


def test_submit_transaction(convex_url):

    private_key, public_address = get_test_account()
    address = create_account(convex_url, public_address)
    request_funds(convex_url, address)
    # faucet request amount

    # prepare
    prepare_data = {
        'address': address,
        'source': '(map inc [1 2 3])'
    }
    url = f'{convex_url}/api/v1/transaction/prepare'
    print('prepare send', prepare_data)
    response = requests.post(url, data=json.dumps(prepare_data))
    if response.status_code != 200:
        print('prepare error', response.text)
        assert(response.status_code == 200)

    result = response.json()

    #submit
    print(result)
    hash_data = to_bytes(hexstr=result['hash'])
    signed_hash_bytes = private_key.sign(hash_data)
    signed_hash = to_hex(signed_hash_bytes)
    submit_data = {
        'address': address,
        'accountKey': public_address,
        'hash': result['hash'],
        'sig': remove_0x_prefix(signed_hash)
    }

    url = f'{convex_url}/api/v1/transaction/submit'
    print('submit send', submit_data)
    response = requests.post(url, data=json.dumps(submit_data))
    if response.status_code != 200:
        print('submit error', response.text, response.status_code)
        assert(response.status_code == 200)
    print(response.json())



def test_query_lisp(convex_url):
    private_key, public_address = get_test_account()
    address = create_account(convex_url, public_address)
    request_funds(convex_url, address)
    query_data = {
        'address': address,
        'lang': 'convex-lisp',
        'source': f'(balance {address})'
    }
    url = f'{convex_url}/api/v1/query'
    print('query send', query_data)
    response = requests.post(url, data=json.dumps(query_data))
    if response.status_code != 200:
        print('query error', response.text)
        assert(response.status_code == 200)
    result = response.json()
    assert(result)
    assert(result['value'] > 0)


def test_query_scrypt(convex_url):
    private_key, public_address = get_test_account()
    address = create_account(convex_url, public_address)
    request_funds(convex_url, address)
    query_data = {
        'address': address,
        'lang': 'convex-scrypt',
        'source': f'balance({address})'
    }
    url = f'{convex_url}/api/v1/query'
    print('query send', query_data)
    response = requests.post(url, data=json.dumps(query_data))
    if response.status_code != 200:
        print('query error', response.text)
        assert(response.status_code == 200)
    result = response.json()
    assert(result)
    print(result)
    assert(result['value'] > 0)

