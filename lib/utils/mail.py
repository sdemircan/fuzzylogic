import smtplib

def sendInformationMail(suspiciousHost):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login("apacheddos@gmail.com", "ddos111111")
    server.sendmail("apacheddos@gmail.com", "demircan.serhat@gmail.com", "From: apacheddos@gmail.com\nTo: demircan.serhat@gmail.com\nSubject: Suspicious Activity\n\n Host: %s" % suspiciousHost)
    
    server.quit()

if __name__ == "__main__":
    sendInformationMail("127.0.0.1")
