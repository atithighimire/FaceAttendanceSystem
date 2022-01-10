import smtplib

server = smtplib.SMTP('smtp.gmail.com', 25)
server.connect("smtp.gmail.com",587)
server.ehlo()
server.starttls()
server.ehlo()
server.login('atithighimire99@gmail.com', "pwd")
# text = msg.as_string()
server.sendmail('atithighimire99@gmail.com', 'sum.nir1@gmail.com', 'hello')
server.quit()