#!/usr/bin/env python3

import os
import asyncio
from sliver import SliverClientConfig, SliverClient

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".sliver-client", "configs")
DEFAULT_CONFIG = os.path.join(CONFIG_DIR, "default.cfg")

async def main():
	config = SliverClientConfig.parse_config_file(DEFAULT_CONFIG)
	client = SliverClient(config)
	print('[*] Connected to server ...')
	await client.connect()
	sessions = await client.sessions()
	# print(f'[*] Sessions: {sessions}')

	# if len(sessions):
	# 	print(f'[*] Interacting with session {sessions[0].ID}')
	# 	interact = await client.interact_session(sessions[0].ID)
	# 	ls = await interact.ls()
	# 	print('[*] ls: %r' % ls)
	for session in sessions:
		print(f'[*] Interacting with {session.Username}@{session.Hostname} - {session.RemoteAddress}')
		interact = await client.interact_session(session.ID)
		ls = await interact.ls()
		print(ls)

if __name__ == '__main__':
	asyncio.run(main())
