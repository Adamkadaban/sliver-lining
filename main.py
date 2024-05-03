#!/usr/bin/env python3

from sliver import SliverClientConfig, SliverClient

import os
import asyncio
import argparse

from modules.spray import Spray
from modules.interact import Interact
from modules.persist import Persist
from modules.move import Move

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".sliver-client", "configs")
DEFAULT_CONFIG = os.path.join(CONFIG_DIR, "default.cfg")

async def main():
	config = SliverClientConfig.parse_config_file(DEFAULT_CONFIG)
	client = SliverClient(config)
	print('[*] Connected to server ...')
	await client.connect()

	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()

	spray_parser = subparsers.add_parser('spray')
	interact_parser = subparsers.add_parser('interact')
	persist_parser = subparsers.add_parser('persist')
	move_parser = subparsers.add_parser('move')

	args = parser.parse_args()

if __name__ == '__main__':
	asyncio.run(main())
