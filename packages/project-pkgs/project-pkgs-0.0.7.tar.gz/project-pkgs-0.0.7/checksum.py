'''
Date: 2020-12-24 08:43:30
LastEditors: Rustle Karl
LastEditTime: 2020-12-24 09:46:50
'''
import hashlib

__methods = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha224': hashlib.sha224,
    'sha256': hashlib.sha256,
    'sha384': hashlib.sha384,
    'sha512': hashlib.sha512,
}


def checksum(path, method='md5', block_size=1 << 20, byte=False):
    _hasher = __methods.get(method, None)
    if _hasher is None:
        raise NotImplementedError(method)

    hasher = _hasher()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            hasher.update(chunk)

    return hasher.digest() if byte else hasher.hexdigest()


def md5(path, block_size=1 << 20, byte=False):
    return checksum(path, 'md5', block_size, byte)


if __name__ == "__main__":
    md5(r'd:\airdrop\go1.15.2.linux-amd64.tar.gz')
