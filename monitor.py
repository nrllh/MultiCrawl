from datetime import datetime
from DBOps import DBOps
import time
db=DBOps()
 


def alarm(src): 
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = "hiv@mailton.de"
    receiver_email = "demir@internet-sicherheit.de"
    password = "-Hiv12345-"

    message = MIMEMultipart("alternative")
    message["Subject"] ="ERROR: "+ src
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
            Hi,
            Please check the measurement, there may be an error.<br> 
"""
    html = """\
    <html>
    <body>
        <p>Hi,<br>
        Please check the measurement, there may be an error.<br> 
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.strato.de", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

                

def start(): 
    gcp_pre=0
    gcp_now=0
    ifis_pre=0
    ifis_now=0
    while(True):
        try:
            gcp_now=db.select("select max(id) from sites where id<15000 and ready=true;") 
            if gcp_now==gcp_pre:
                alarm('gcp')
                print('mail sent. gcp')
            ifis_now=db.select("select max(id) from sites where id<15000 and ready=true;") 
            if ifis_pre == ifis_now:
                alarm('ifis')
                print('mail sent. ifis')
            gcp_pre=gcp_now
            ifis_pre= ifis_now
            print('check done.' + str(datetime.now()))
            time.sleep(12000) 
        except Exception as e:
            print('error:' + str(e))


start()