import socket
import sys
import subprocess
import csv
import re

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host='148.93.50.254'
port=5432
server_address = (host, port)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind((host,port))
sock.listen(5)
while True:
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()
        try:
                print >>sys.stderr, 'connection from', client_address
                while True:
                        data = connection.recv(16)
                        data.strip()
                        print >>sys.stderr, 'received "%s"' % data
                        try: 
                                socket.inet_aton(data)
                                #data.strip()
                                print >>sys.stderr, 'sending data back to the client'
                                name = subprocess.Popen(["nbtscan " + data], stdout=subprocess.PIPE, shell=True)
                                (out, err) = name.communicate()
                                out = out.split('IP')
                                out = out[1]
                                out = "IP " + out
                                connection.sendall(out+'\n')
                                ip = data
                                ip = ip.split('.')
                                ip2 = ip[0]+"."+ip[1]+"."+ip[2]+".0"
                                ip = ip[0]+"."+ip[1]+".0.0"
                                print >>sys.stderr, ip2, ip
                                location=[]
                                with open('IP_Space.csv') as f:
                                        reader = csv.reader(f, delimiter=',')
                                        for row in reader:
                                                if ip in row:
                                                        print >> sys.stderr, row
                                                        location.append(row)
                                with open('IP_Space.csv') as f:
                                        reader = csv.reader(f, delimiter=',')
                                        for row in reader:
                                                if ip2 in row:
                                                        print >> sys.stderr, row
                                                        location.append(row)
                                #location = ",".join(location)
                                #location = location.replace(",", '\t')
                                print >>sys.stderr, location
                                #connection.sendall(out)
                                header = ["Region","Country or Group","10. Client","Guest","Block","Size","Site","Remarks"]
                                header = '{:15}{:25}{:15}{:15}{:6}{:7}{:12}{:20}'.format(*header)
                                connection.sendall(header+"\n")
                                connection.sendall("-----------------------------------------------------------------------------------------------------------\n")
                                for line in location:
                                        connection.sendall('{:15}{:25}{:15}{:15}{:6}{:7}{:12}{:15}'.format(*line)+'\n')
                                #print >>sys.stderr, header
                                #connection.sendall(header)
                                #connection.sendall("\n"+location)
                                #connection.sendall(location)
                                #location = ""
                                break
                        except:
                                print >>sys.stderr, 'Not a valid IP from', client_address
                                break
        finally:
                connection.close()
