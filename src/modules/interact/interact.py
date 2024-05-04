class Interact:
	def __init__(self, client):
		self.client = client


	async def ifconfig(self):
		sessions = await self.client.sessions()

		for session in sessions:
			print(f'[*] Interacting with {session.Username}@{session.Hostname} - {session.RemoteAddress}')
			interact = await self.client.interact_session(session.ID)

			# First step to pivot information
			ifconfig = await interact.ifconfig()
			ifconfig_fields = ifconfig.NetInterfaces
			print(' --- Interfaces ---')
			for iface in ifconfig_fields:
				print(f'\t{iface.Name} - {iface.IPAddresses}')


	async def netstat(self):
		sessions = await self.client.sessions()

		for session in sessions:
			print(f'[*] Interacting with {session.Username}@{session.Hostname} - {session.RemoteAddress}')
			interact = await self.client.interact_session(session.ID)

			# TCP, UDP, IPv4, IPv6
			netstat = await interact.netstat(True, False, True, False) # TODO: I need to make this customizable by the user

			for connection in netstat.Entries:
				# I think default should be to show all listening connections.
				if connection.SkState == "LISTEN":
					print(f"Listening on {connection.LocalAddr.Ip}:{connection.LocalAddr.Port}")
					if connection.Process.Pid:
						print(f"\t{connection.Process.Executable} ({connection.Process.Pid})")


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
