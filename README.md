cluster_hostfile_generator
==========================

makeclusterhost.py [OPTION]
Description:
        This program generates a host file for a cluster based on information stored in DNS.  The output is sent to stdout and can be redirected to a file.

Options:
        -d, --dnsdomain         Set the DNS domain to use
        -b, --basename          Set the base of the server (hostname without the node number at the end)
        -s, --static            Add static address line, format: ipaddr hostname.domain hostname
        -h, --help              Print this useful help screen

Examples:
        makeclusterhost.py > /etc/hosts --dnsdomain foo.com --basename server --static "192.168.10.3 virtualcenter.foo.com virtualcenter" --static "192.168.10.4 statichost"

        The /etc/host file contains the following:
        # Do not edit, changes will be overwritten
        127.0.0.1       localhost.foo.com  localhost
        192.168.10.3    virtualcenter.foo.com virtualcenter
        192.168.10.4    statichost
        192.168.10.11   server01.foo.com   server01
        192.168.0.12    server02.foo.com   server02
