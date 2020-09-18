import smtplib
import math, random
def mai(maid,passw):
    
    usermail=maid
    msg=passw
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("nireshkumar.jkr@gmail.com", "eieniicydjrdjyaw")
    s.sendmail("nireshkumar.jkr@gmail.com",usermail,msg)
    s.quit()
    print("sent successfully")

def otp(un,votev,email_ver):
    digits = "0123456789"
    OTP=""
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)]
    print("this is otp generated",OTP)
    
    usermail=email_ver
    msg=OTP
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("nireshkumar.jkr@gmail.com", "eieniicydjrdjyaw")
    s.sendmail("nireshkumar.jkr@gmail.com",usermail,msg)
    s.quit()
    print("sent successfully")
    return OTP

    
    
