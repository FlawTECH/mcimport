from mcstatus import MinecraftServer
import nmap
import socket
import sys
hah

def fetch_hosts(startr, endr):
    found = []
    for x in range(startr, endr + 1):
        found_ports = 0
        nm = nmap.PortScanner()
        ip = socket.gethostbyname('minecraft'+str(x)+'.omgserv.com')
        print('Checking minecraft'+str(x)+'.omgserv.com...')
        nm.scan(ip, '10000-25565','')
        ports = list(nm[ip]['tcp'].keys())
        for port in ports:
            found.append(str(x)+','+str(ip)+':'+str(port))
            found_ports += 1
        print('Found '+str(found_ports)+' open ports.')
    print('Done !')
    return found

def scan_servers(servers, version, is_modded):
    print('Fetching servers details ...')
    server_info = []
    for full_server in servers:
        server_batch = full_server.split(',')[0]
        server = full_server.split(',')[1]
        print('Checking '+server)
        server_ping = MinecraftServer.lookup(server)
        try:
            server_status = server_ping.status()
        except socket.error:
            continue
        if version in server_status.version.name and is_modded == ('modinfo' in server_status.raw):
            server_info.append(str(server_batch)+','+str(server_ping.host)+":"+str(server_ping.port)+","+server_status.version.name+","+str(server_status.players.online)+"/"+str(server_status.players.max))
    print('Done !')
    return server_info


is_modded = False
version = ''

if not len(sys.argv) >= 3:
    print ("Invalid argument. Usage: mcimport.py <range_start> <range_end> [version] [--mods])")
    exit(-1)
if len(sys.argv) >= 4:
    version = str(sys.argv[3])
if len(sys.argv) >= 5:
    is_modded = True

servers = fetch_hosts(int(sys.argv[1]), int(sys.argv[2]))
valid_servers = scan_servers(servers, version, is_modded)
if len(valid_servers) > 0:
    print('Format: BATCH,HOST,VERSION,ONLINE')
else:
    print('No servers found.')
for server in valid_servers:
    print(server)
