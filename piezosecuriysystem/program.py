import smtplib,email,os
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from picamera import PiCamera
import RPi.GPIO as GPIO
import datetime
from time import sleep
#*********************************************** GPIO setup *************************************************
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
piezo=20
buzzer=16
fire=7
GPIO.setup(fire,GPIO.IN)
GPIO.setup(piezo,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)
#*********************************************** Email parameters *************************************************
subject='Security Alert'
bodyText1="Hi,\nA motion has been detected"
bodyText2="Hi,\nA flame has been detected"
SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=587
USERNAME='khataubhavik@gmail.com'
PASSWORD='******'
RECIEVER_EMAIL='mauryadeepak9299@gmail.com'
#*********************************************** Video finename and path *************************************************
filename_part1="security_system"
file_ext=".mp4"
now = datetime.datetime.now()
current_datetime = now.strftime("%d-%m-%Y_%H:%M:%S")
filename=filename_part1+"_"+current_datetime+file_ext
filepath="/home/pi/security_system/capture/"

def send_email1():
    message=MIMEMultipart()
    message["From"]=USERNAME
    message["To"]=RECIEVER_EMAIL
    message["Subject"]=subject

    message.attach(MIMEText(bodyText1, 'plain'))
    attachment=open(filepath+filename, "rb")

    mimeBase=MIMEBase('application','octet-stream')
    mimeBase.set_payload((attachment).read())

    encoders.encode_base64(mimeBase)
    mimeBase.add_header('Content-Disposition', "attachment; filename= " +filename)

    message.attach(mimeBase)
    text=message.as_string()

    session=smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()

    session.login(USERNAME, PASSWORD)
    session.sendmail(USERNAME, RECIEVER_EMAIL, text)
    session.quit
    print("Email sent")

def send_email2():
    message=MIMEMultipart()
    message["From"]=USERNAME
    message["To"]=RECIEVER_EMAIL
    message["Subject"]=subject

    message.attach(MIMEText(bodyText2, 'plain'))
    attachment=open(filepath+filename, "rb")

    mimeBase=MIMEBase('application','octet-stream')
    mimeBase.set_payload((attachment).read())

    encoders.encode_base64(mimeBase)
    mimeBase.add_header('Content-Disposition', "attachment; filename= " +filename)

    message.attach(mimeBase)
    text=message.as_string()

    session=smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()

    session.login(USERNAME, PASSWORD)
    session.sendmail(USERNAME, RECIEVER_EMAIL, text)
    session.quit
    print("Email sent")
    
def capture_video():
    camera.start_preview()
    camera.start_recording('/home/pi/security_system/capture/newvideo.h264')
    camera.wait_recording(10)
    camera.stop_recording()
    camera.stop_preview()


def remove_file():
    if os.path.exists("/home/pi/security_system/capture/newvideo.h264"):
        os.remove("/home/pi/security_system/capture/newvideo.h264")
    else:
        print("file does not exist")
#*************************************************** Initiate pi Camera **************************************************************************
camera=PiCamera()
#*************************************************** Main code for method call ********************************************************************
while True:
    piezoin=GPIO.input(piezo)
    firein=GPIO.input(fire)
    print("Piezo sensor     ",piezoin)
    print("IR flame sensor  ",firein)
    sleep(5)
    if piezoin==1:
        print("Motion Detected")
        capture_video()
        sleep(2)
        res=os.system("MP4Box -add /home/pi/security_system/capture/newvideo.h264 /home/pi/security_system/capture/newvideo.mp4")
        os.system("mv /home/pi/security_system/capture/newvideo.mp4 "+filepath+filename)
        GPIO.output(buzzer,GPIO.HIGH)
        send_email1()
        sleep(2)
        remove_file()
    #if firein==1:
        #print("Flame Detected")
        #capture_video()
        #sleep(2)
        #res=os.system("MP4Box -add /home/pi/security_system/capture/newvideo.h264 /home/pi/security_system/capture/newvideo.mp4")
        #os.system("mv /home/pi/security_system/capture/newvideo.mp4 "+filepath+filename)
        #send_email2()
        #sleep(2)
        #remove_file()
        #GPIO.output(buzzer,GPIO.HIGH)
        #sleep(3)
    else:
        GPIO.output(buzzer,GPIO.LOW)
