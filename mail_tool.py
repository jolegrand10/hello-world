""" mail-tool.py """
import imaplib
from email.parser import HeaderParser
server="***"
username="***"
password="***"
m = imaplib.IMAP4(server)
m.login(username,password)
# get list of mailboxes
list = m.list();
# select which mail box to process
m.select("Inbox") 
resp, data = m.uid('search',None, "ALL") # search and return Uids
uids = data[0].split()    
mailparser = HeaderParser()
for uid in uids:
    resp,data = m.uid('fetch',uid,"(BODY[HEADER])")        
    msg = mailparser.parsestr(data[0][1])       
    print (msg['From'],msg['Date'],msg['Subject'])
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if filename is None:
            #
            # this happens when attachment is made of a retransferred email
            #
            continue
        print "Attach: ",filename
        
    print m.uid('STORE',uid, '+FLAGS', '(\\Deleted)')
print m.expunge()
#
#
m.close() # close the mailbox
m.logout()# logout 
