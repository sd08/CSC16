import urllib
import BeautifulSoup
import urlparse
import mechanize
import socket
import os
# Set the startingpoint for the spider and initialize
# the a mechanize browser object

import dns
import dns.name
import dns.query
import dns.resolver

def get_authoritative_nameserver(domain, log=lambda msg: None):
    n = dns.name.from_text(domain)

    depth = 2
    default = dns.resolver.get_default_resolver()
    nameserver = default.nameservers[0]

    last = False
    while not last:
        s = n.split(depth)

        last = s[0].to_unicode() == u'@'
        sub = s[1]

        #log('Looking up %s on %s' % (sub, nameserver))
        query = dns.message.make_query(sub, dns.rdatatype.NS)
        response = dns.query.udp(query, nameserver)

        rcode = response.rcode()
        if rcode != dns.rcode.NOERROR:
            if rcode == dns.rcode.NXDOMAIN:
                raise Exception('%s does not exist.' % sub)
            else:
                raise Exception('Error %s' % dns.rcode.to_text(rcode))

        rrset = None
        if len(response.authority) > 0:
            rrset = response.authority[0]
        else:
            rrset = response.answer[0]

        rr = rrset[0]
        if rr.rdtype == dns.rdatatype.SOA:
            c=0#log('Same server is authoritative for %s' % sub)
        else:
            authority = rr.target
            #log('%s is authoritative for %s' % (authority, sub))
            nameserver = default.query(authority).rrset[0].to_text()

        depth += 1

    return nameserver


def log(msg):
    print msg


def writeIP(filename,ip,h):
   filename.write(h+'\n')
   filename.write(ip+'\n')
   #filename.write(nameserver+'\n')
   
   #filename.write(ip[0]+'\n')
   #if(len(ip[1]) != 0):
   #   filename.write(ip[1][0]+'\n')
   #else:
   #   filename.write('empty\n')
   #for j in ip[2]:
   #   filename.write(j+'\n')


url = ["google.com","facebook.com", "youtube.com","yahoo.com","baidu.com","wikipedia.org","amazon.com","twitter.com","qq.com","taobao.com","linkedin.com","google.co.in", "live.com","sina.com.cn","hao123.com","blogspot.com","weibo.com","yahoo.co.jp","yandex.ru","tmall.com","vk.com","ebay.com","google.de", "bing.com","sohu.com","pinterest.com","wordpress.com","google.co.uk","google.co.jp","360.cn","instagram.com","ask.com","google.fr", "msn.com","apple.com","google.com.br","tumblr.com","soso.com","reddit.com","mail.ru","paypal.com","xvideos.com","imgur.com", "microsoft.com","google.ru","163.com","google.it","t.co","imdb.com","google.es","aliexpress.com","adcash.com","alibaba.com", "amazon.co.jp","go.com","craigslist.org","stackoverflow.com","xhamster.com","google.com.mx","fc2.com","google.ca","espn.go.com", "bbc.co.uk","akamaihd.net","amazon.de","cnn.com","flipkart.com","netflix.com","onclickads.net","gmw.cn","pornhub.com","google.com.tr", "huffingtonpost.com","people.com.cn","blogger.com","google.com.hk","kickass.to","google.com.au","googleusercontent.com","ebay.de", "google.pl","odnoklassniki.ru","amazon.co.uk","google.co.id","dropbox.com","adobe.com","dailymotion.com","thepiratebay.se", "rakuten.co.jp","indiatimes.com","xinhuanet.com","dailymail.co.uk","amazon.in","xnxx.com","pixnet.net","nytimes.com","ebay.co.uk", "outbrain.com","wordpress.org","buzzfeed.com"]
names=["google.com","facebook.com", "youtube.com","yahoo.com","baidu.com","wikipedia.org","amazon.com","twitter.com","qq.com","taobao.com","linkedin.com","google.co.in","live.com","sina.com.cn", "hao123.com","blogspot.com","weibo.com","yahoo.co.jp","yandex.ru","tmall.com","vk.com","ebay.com","google.de","bing.com","sohu.com", "pinterest.com","wordpress.com","google.co.uk","google.co.jp","360.cn","instagram.com","ask.com","google.fr","msn.com","apple.com","google.com.br","tumblr.com","soso.com","reddit.com","mail.ru","paypal.com","xvideos.com","imgur.com","microsoft.com","google.ru","163.com","google.it","t.co","imdb.com","google.es", "aliexpress.com","adcash.com","alibaba.com","amazon.co.jp","go.com","craigslist.org","stackoverflow.com","xhamster.com","google.com.mx","fc2.com","google.ca","espn.go.com","bbc.co.uk","akamaihd.net","amazon.de","cnn.com","flipkart.com","netflix.com","onclickads.net","gmw.cn","pornhub.com","google.com.tr","huffingtonpost.com","people.com.cn","blogger.com", "google.com.hk","kickass.to","google.com.au","googleusercontent.com","ebay.de","google.pl","odnoklassniki.ru","amazon.co.uk","google.co.id","dropbox.com","adobe.com","dailymotion.com","thepiratebay.se","rakuten.co.jp","indiatimes.com","xinhuanet.com","dailymail.co.uk","amazon.in","xnxx.com","pixnet.net","nytimes.com","ebay.co.uk","outbrain.com","wordpress.org","buzzfeed.com"]
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)
hosts=[]
links=[]
visited=[]
# create lists for the urls in que and visited urls
count=0
limit = 25

for u in url:
   u="http://www."+u
   directory='./'+names[count]+'/'
   tempdir=directory 
   if not os.path.exists(directory):
      os.mkdir(directory)
   try:
      br.open(u)
      tempcount=0
      f = open(directory+names[count]+'.txt', 'a')
      ind=u.index('/')
      ips = socket.gethostbyname(u[(ind+2):])
      #ns=get_authoritative_nameserver(u[(ind+2):])
      writeIP(f,ips,u[(ind+2):])
      f.close() 
      count1=0
      #l=0
      for i in br.links():
         tempcount+=1
         if tempcount<(limit+1):
            links.append(urlparse.urljoin(i.base_url,i.url))
         else:
            break
      for link in links:
         newurl = link
         host=urlparse.urlparse(newurl).hostname
         if True:
            if newurl not in visited:
               #l+=1
               count1+=1
               visited.append(newurl)
               print host+' '+u+' link '+str(count1)
               directory=tempdir+'link '+str(count1)+'/'
               if not os.path.exists(directory):
                  os.mkdir(directory)
               f = open(directory+'link '+str(count1)+'.txt', 'a')
               ips = socket.gethostbyname(host)
               #ns=get_authoritative_nameserver(host)
               writeIP(f,ips,host)
               f.close()
               count2=0
               try:
                  tempcount1=0
                  br.open(newurl)
                  for ii in br.links():
                     tempcount1+=1
                     if tempcount1<(limit1+1):
                        links1.append(urlparse.urljoin(ii.base_url,ii.url))
                     else:
                        break 
               except Exception,e1:
                  print "\n\nerror: "+str(e1)+"\n\n"
                  #count2+=1
            #count1=count1+1
         else:
            print "limit reached for "+u
            break
   except Exception,e:
      print "\n\nerror: "+str(e)+"\n\n"
      #count1=count1+1
   count+=1

print str(count)+' '+str(count1)
