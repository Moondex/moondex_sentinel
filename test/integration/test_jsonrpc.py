import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from moondexd import MoondexDaemon
from moondex_config import MoondexConfig


def test_moondexd():
    config_text = MoondexConfig.slurp_config_file(config.moondex_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000002a5a6865778ac64a6697448ac5e5c0c77c776a8184721202751f1382177'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000002a5a6865778ac64a6697448ac5e5c0c77c776a8184721202751f1382177'

    creds = MoondexConfig.get_rpc_creds(config_text, network)
    moondexd = MoondexDaemon(**creds)
    assert moondexd.rpc_command is not None

    assert hasattr(moondexd, 'rpc_connection')

    # Moondex testnet block 0 hash == 0000000f350d9039575f6446584f4ae4317bed76aae26ef1f2381ff73f7cd68d
    # test commands without arguments
    info = moondexd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert moondexd.rpc_command('getblockhash', 0) == genesis_hash
