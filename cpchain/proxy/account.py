from msgpack import packb, unpackb

from cpchain.account import set_default_account, lock_account, unlock_account
from cpchain.crypto import ECCipher

def set_proxy_account():
    global _proxy_account # pylint: disable=global-variable-undefined

    _proxy_account = set_default_account()

def get_proxy_id():
    return ECCipher.get_address_from_public_key(
        _proxy_account.public_key)

def lock_proxy_account():
    lock_account(_proxy_account)

def unlock_proxy_account():
    unlock_account(_proxy_account)

def sign_proxy_data(data):
    public_key = _proxy_account.public_key
    private_key = _proxy_account.private_key

    signature = ECCipher.create_signature(
        private_key,
        data
        )

    msg = {
        'data': data,
        'public_key': ECCipher.serialize_public_key(public_key),
        'signature': signature
    }

    return packb(msg, use_bin_type=True)


def derive_proxy_data(msg):

    msg = unpackb(msg, raw=False)

    public_key = ECCipher.create_public_key(msg['public_key'])
    data = msg['data']
    signature = msg['signature']

    valid = ECCipher.verify_sign(public_key, signature, data)
    if valid:
        return data
