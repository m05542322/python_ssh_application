def GetServerList (inputfile):
	with open(inputfile) as input:
		server_list = input.readlines()

	a = dict()

	for item in server_list:
		item = item.split("\n")[0]
		if item[0] != '#':
			#print item
			if len(item.split("=")) == 2:
				server_name = item.split("=")[0]
				server_addr = item.split("=")[1]
				if server_name in a:
					continue
				else:
					a[server_name] = server_addr

	#print a
	return a


#serverList = GetServerList('config/server_list.txt')

#for item in serverList:
	#print item
	#print serverList[item]
