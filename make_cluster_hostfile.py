#!/usr/bin/python
import os,sys,getopt

"""
    Copyright 2008 Dwight Hubbard

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

###################################################
# Defaults
###################################################
# The base of the server hostname (hostname without
# the node number)
BASE='server'

# Set to your local domain 
DOMAIN=''

# IP range to try (this should never need to be changed)
FIRST=1
LAST=99

def getip(hostname):
        """ Use nslookup command to lookup a hostname, return the IP or none """
	ip='None'
	foundname=False
	command='nslookup %s' % hostname
	for line in os.popen(command).readlines():
		if len(line)>5 and line[0:5] == 'Name:':
			foundname=True
		if len(line) and foundname == True and line[0:8] == 'Address:':
			ip=line.strip().split()[1]
	return(ip)

def usage():
        """ Print the usage information """
	print 'makeclusterhost.py [OPTION]'
	print 'Description:'
	print '\tThis program generates a host file for a cluster based on information stored in DNS.  The output is sent to stdout and can be redirected to a file.'
	print
	print 'Options:'
	print '\t-d, --dnsdomain  \tSet the DNS domain to use'
	print '\t-b, --basename   \tSet the base of the server (hostname without the node number at the end)'
	print '\t-s, --static     \tAdd static address line, format: ipaddr hostname.domain hostname'
	print '\t-h, --help       \tPrint this useful help screen'
	print
	print 'Examples:'
	print '\tmakeclusterhost.py > /etc/hosts --dnsdomain foo.com --basename server --static "192.168.10.3 virtualcenter.foo.com virtualcenter" --static "192.168.10.4 statichost"'
	print
	print '\tThe /etc/host file contains the following:'
	print '\t# Do not edit, changes will be overwritten'
	print '\t127.0.0.1       localhost.foo.com  localhost'
	print '\t192.168.10.3    virtualcenter.foo.com virtualcenter'
	print '\t192.168.10.4    statichost'
	print '\t192.168.10.11   server01.foo.com   server01'
	print '\t192.168.0.12    server02.foo.com   server02'

# Parse the command line parameters
try:
	opts,args = getopt.getopt(sys.argv[1:],"d:b:s:h",["dnsdomain=","basename=","static=","help"])
except getopt.GetoptError:
	usage()
	sys.exit(2)

static=[]
for o,a in opts:
	if o in ("-h","--help"):
		usage()
		sys.exit(0)
	if o in ("-d","--dnsdomain"):
		DOMAIN=a
	if o in ("-b","--basename"):
		BASE=a
	if o in ("-s","--static"):
		static.append(a)

print '# Do not edit, changes will be overwritten'	
print '127.0.0.1\tlocalhost.%s\tlocalhost' % DOMAIN

# Add the static entries
for entry in static:
	print entry

# Start lookup up the rest of the stuff in dns
for num in range(FIRST,LAST+1):
	if DOMAIN == '':
		hostname='%s%2.2d' % (BASE,num)
	else:
		hostname='%s%2.2d.%s' % (BASE,num,DOMAIN)
	ip=getip(hostname)
	if ip != 'None':
		if DOMAIN == '':
			print '%s\t%s' % (ip,hostname)
		else:
			print '%s\t%s\t%s%2.2d' % (ip,hostname,BASE,num)
