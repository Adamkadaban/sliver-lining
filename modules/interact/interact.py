class Interact:
	def __init__(self, client):
		client = client


	async def ifconfig():
		sessions = await self.client.sessions()

		for session in sessions:
			print(f'[*] Interacting with {session.Username}@{session.Hostname} - {session.RemoteAddress}')
			interact = await self.client.interact_session(session.ID)
			ls = await interact.ls()

			# First step to pivot information
			ifconfig = await interact.ifconfig()
			ifconfig_fields = ifconfig.ListFields()[0][1]
			print(' --- Interfaces ---')
			for iface in ifconfig_fields:
				print(f'\t{iface.Name} - {iface.IPAddresses}')
