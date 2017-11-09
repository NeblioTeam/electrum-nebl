#!/usr/bin/env python2

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (2, 7, 0):
    sys.exit("Error: Electrum requires Python version >= 2.7.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-nebl.desktop']),
        (os.path.join(usr_share, 'pixmaps/'), ['icons/electrum-nebl.png'])
    ]

setup(
    name="Electrum-NEBL",
    version=version.ELECTRUM_VERSION,
    install_requires=[
        'pyaes',
        'ecdsa>=0.9',
        'pbkdf2',
        'requests',
        'qrcode',
        'ltc_scrypt',
        'protobuf',
        'dnspython',
        'jsonrpclib',
        'PySocks>=1.6.6',
    ],
    packages=[
        'electrum_nebl',
        'electrum_nebl_gui',
        'electrum_nebl_gui.qt',
        'electrum_nebl_plugins',
        'electrum_nebl_plugins.audio_modem',
        'electrum_nebl_plugins.cosigner_pool',
        'electrum_nebl_plugins.email_requests',
        'electrum_nebl_plugins.hw_wallet',
        'electrum_nebl_plugins.keepkey',
        'electrum_nebl_plugins.labels',
        'electrum_nebl_plugins.ledger',
        'electrum_nebl_plugins.trezor',
        'electrum_nebl_plugins.digitalbitbox',
        'electrum_nebl_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum_nebl': 'lib',
        'electrum_nebl_gui': 'gui',
        'electrum_nebl_plugins': 'plugins',
    },
    package_data={
        'electrum_nebl': [
            'currencies.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ]
    },
    scripts=['electrum-nebl'],
    data_files=data_files,
    description="Lightweight Neblio Wallet",
    author="Thomas Voegtlin",
    author_email="thomasv@electrum.org",
    license="MIT Licence",
    url="http://nebl.io",
    long_description="""Lightweight Neblio Wallet"""
)
