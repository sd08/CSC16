import urllib2
import urlparse
import mechanize
import socket
from geoip import geolite2
import dns
import dns.name
import dns.query
import dns.resolver
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, sniff
from scapy.layers import http



def getAllLinksOnPage(link,breadth,br,flag):
   limitb=0
   newlinks=[]
   try:
      br.open(link)
      for ii in br.links():
         if flag==1:
            if limitb<breadth:
               u=urlparse.urljoin(ii.base_url,ii.url)
               newlinks.append(u)
               host=urlparse.urlparse(u).hostname #hostname
               #print host
               ips = socket.gethostbyname(host) #ip address 
               match = geolite2.lookup(ips)
               country=match.country     #country of the server 
               #print u
               #print str(ips)+" "+str(country)
               limitb+=1
            else:
               break
         else:
            u=urlparse.urljoin(ii.base_url,ii.url)
            newlinks.append(u)
            
            host=urlparse.urlparse(u).hostname #hostname
            #print host
            ips = socket.gethostbyname(host) #ip address
            match = geolite2.lookup(ips)
            country=match.country     #country of the server
            #print u
            #print str(ips)+" "+str(country)
            #limitb+=1
   except Exception,e:
      print "\nerror: "+str(e)+"\n"
   print len(newlinks)
   return newlinks



def crawl(seed,depth,breadth,br,flag):
   global crawled
   #crawled = set()
   limitd=0
   def crawl_recursively(link,limitd,depth,breadth,br,flag):
      if limitd==depth:
         return
      if link in crawled:
         return
      if limitd==0:
         host=urlparse.urlparse(link).hostname #hostname for the primary seed
         ips = socket.gethostbyname(host) #ip address of its server
         print host
         match = geolite2.lookup(ips)
         country=match.country  #country of the server
         print str(ips)+" "+str(country)
         host=host.split('.')
         host=host[-2]+'.'+host[-1]
         answers = dns.resolver.query(host,'NS')
         for server in answers:
            print str(server)+" "+socket.gethostbyname(str(server))
                 
      #print("\n"+str(limitd))
      print link+"\n"
      newLinks = getAllLinksOnPage(link,breadth,br,flag)
      crawled.add(link)#seed
      for link in newLinks:
         crawl_recursively(link,limitd+1,depth,breadth,br,flag)
      return
   crawl_recursively(seed,limitd,depth,breadth,br,flag)
   return crawled



def process_tcp_packet(packet):
    '''
    Processes a TCP packet, and if it contains an HTTP request, it prints it.
    '''
    if not packet.haslayer(http.HTTPRequest):
        # This packet doesn't contain an HTTP request so we skip it
        return
    f_log = open('log.csv','w' 'r+')
    http_layer = packet.getlayer(http.HTTPRequest)
    ip_layer = packet.getlayer(IP)
    f_log.write( '\n{0[src]},{1[Method]},{1[Host]}{1[Path]}'.format(ip_layer.fields, http_layer.fields))
    f_log.close()


#main code 

global crawled
crawled = set()

depth=1
breadth=20
flag=1
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)

f = open('top-100.txt', 'r')

Url_num=input('No of URLs to crawl') #no of alexa sites you want to crawl 
print Url_num

for j in range(Url_num):
   url=f.readline()
   url="http://www."+url[1:-1]
   out=crawl(url,depth,breadth,br,breadthflag)

# Start sniffing the network.
sniff(filter='tcp', prn=process_tcp_packet)
f.close()






   
