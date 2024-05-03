class Interact:
	def __init__(self, client):
		self.client = client


	async def ifconfig(self, command):
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


	async def exec(self, command):
		sessions = await self.client.sessions()

		for session in sessions:
			print(f'[*] Interacting with {session.Username}@{session.Hostname} - {session.RemoteAddress}')
			interact = await self.client.interact_session(session.ID)
			if session.OS == "linux":
				command_args = command.split()
				exe = command_args.pop(0)
				execute = await interact.execute(exe, command_args, True)
			elif session.OS == "windows":
				# TODO: Need to come up with a better way to decide powershell or cmd
				# Maybe just use the same logic as linux?
				execute = await interact.execute("powershell.exe", ["/c", command], True)
			else:
				# Assuming MACOS for now. This might break
				# print(f"OS: {session.OS} not implemented")
				command_args = command.split()
				exe = command_args.pop(0)
				execute = await interact.execute(exe, command_args, True)

			print(execute.Stderr.decode()) # TOOD: print this in red
			print(execute.Stdout.decode())
