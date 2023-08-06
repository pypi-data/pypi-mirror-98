import poplib
from email.header import decode_header
from email.mime.text import MIMEText
import email
def read_by_subject(server,user_,pass__):
 read = poplib.POP3(server)
 read.user(user_)
 read.pass_(pass__)
 tongji = read.stat()
 str = read.top(tongji[0],0
 str2 = []
 for x in str[1]:
     try:
         str2.append(x.decode())
     except:
         try:
             str2.append(x.decode('gbk'))
         except:
             str2.append(x.decode('big5'))
 msg = email.message_from_string('\n'.join(str2))
 biaoti = decode_header(msg['subject'])
 if biaoti[0][1]:
     biaoti2 = biaoti[0][0].decode(biaoti[0][1])
 else:
     biaoti2 = biaoti[0][0]
 return biaoti2