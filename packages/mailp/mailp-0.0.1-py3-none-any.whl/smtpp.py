from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
def send(from_addr,password,to_addr,smtp_server,post,msg)
 server = smtplib.SMTP(smtp_server, post)
 server.starttls()
 server.set_debuglevel(1)
 server.login(from_addr, password)
 server.sendmail(from_addr, [to_addr], msg.as_string())
 server.quit()
def by_text(text,from_,to_,subject)
 msg = MIMEText(text, 'plain', 'utf-8')
 msg['From'] = _format_addr(from_+' <%s>' % from_addr)
 msg['To'] = _format_addr('收件人昵称 <%s>' % to_)
 msg['Subject'] = Header(subject, 'utf-8').encode()
 return msg