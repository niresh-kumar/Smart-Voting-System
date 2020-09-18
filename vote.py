from tkinter import *
import tkinter.messagebox
from PIL import Image,ImageTk
import mysql.connector
import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from Password import passw
from mail import mai,otp

from functools import partial


from tkinter import ttk





#-------------------------------Database------------------------------------------------------------------

def database():
    aa= mysql.connector.connect(host='localhost',port= 3306,user="root",passwd="root",db="votingsystem")
    print('connect')
    return aa
#-------------------------------------------------------------HomePage--------------------------------------------------------------------    

def main():

  
    R1=Tk()
    R1.geometry('900x600')
    R1.title('Home Page')
    image=Image.open('Homepage.png')
    image=image.resize((900,600))
    photo_image=ImageTk.PhotoImage(image)
    label1=tkinter.Label(R1,image=photo_image)
    label1.place(x=0,y=0)
    
    la=Label(R1,text="SMART VOTING SYSTEM WITH FACE RECOGNITION",font=('algerian',15,'bold'))
    la.place(x=200,y=100)
    
    Registerbt = Button(R1,text = "ADMIN",width=17,height=2,font=('algerian',15,'bold'),justify='center',bg="light blue",relief=SUNKEN,command=Admin)
    Registerbt.place(x =180 ,y=475)

    image1=Image.open('Admin-icon.png')
    image1=image1.resize((250,250))
    photo_image1=ImageTk.PhotoImage(image1)
    label2=tkinter.Label(R1,image=photo_image1)
    label2.place(x=170,y=200)

    loginbt = Button(R1,text = "USERS",width=17,height=2,font=('algerian',15,'bold'),justify='center',bg="light blue",relief=SUNKEN,command=login)
    loginbt.place( x =510,y=475)

    image2=Image.open('user.png')
    image2=image2.resize((250,250))
    photo_image2=ImageTk.PhotoImage(image2)
    label3=tkinter.Label(R1,image=photo_image2)
    label3.place(x=500,y=200)

    R1.mainloop()

    

#-----------------------------------------signup------------------------------------------------------------------------------------



#----------------------------face Detection-----------------------------------------------------------
def faceDetect(vcn,un,ei):
    
    def TakeImages(vcn,un,ei):
        R6.destroy()
        Id=vcn
        name=un
        eid=ei
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+str(Id) +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        #res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name, eid]
        with open('VoterDetails\VoterDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        TrainImages()  
    
    def TrainImages():
        recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector =cv2.CascadeClassifier(harcascadePath)
        faces,Id = getImagesAndLabels("TrainingImage")
        recognizer.train(faces, np.array(Id))
        recognizer.save("TrainingImageLabel\Trainner.yml")
        #res = "Image Trained"#+",".join(str(f) for f in Id)
        print('completed')
        tkinter.messagebox.showinfo("Face","Captured and sucessfully registered")
        tkinter.messagebox.showinfo("Mail","Upassword send to Registred Mail")
        

    def getImagesAndLabels(path):
        #get the path of all the files in the folder
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        #print(imagePaths)
        
        #create empth face list
        faces=[]
        #create empty ID list
        Ids=[]
        #now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            #loading the image and converting it to gray scale
            pilImage=Image.open(imagePath).convert('L')
            #Now we are converting the PIL image into numpy array
            imageNp=np.array(pilImage,'uint8')
            #getting the Id from the image
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces.append(imageNp)
            Ids.append(Id)        
        return faces,Ids

    
    R6 = tkinter.Toplevel()
    R6.geometry('800x600')
    R6.title("Face Capture")
    image=Image.open('Homepage.png')
    image=image.resize((800,600))
    photo_image=ImageTk.PhotoImage(image)
    label1=tkinter.Label(R6,image=photo_image)
    label1.place(x=0,y=0)
    image1=Image.open('face.jpg')
    image1=image1.resize((200,200))
    photo_image1=ImageTk.PhotoImage(image1)
    label3=tkinter.Label(R6,image=photo_image1)
    label3.place(x=280,y=150)
    btn = Button(R6, text="Capture Face Here", width=25, height=2,fg="black",font=('algerian',15,'bold'),justify='center',bg="light blue",command=partial(TakeImages,vcn,un,ei))
    btn.place(x=280, y=400)
    R6.mainloop()



#---------------------------Register Page--------------------------------------------------------------------
def Admin():
    def table():
        aa= mysql.connector.connect(host='localhost',port= 3306,user="root",passwd="root",db="votingsystem")
        query1=aa.cursor()
        query1.execute("SELECT usernames,Votercardnos,emails FROM `facerec")
        rows=query1.fetchall()
        total=query1.rowcount
        print(str(total))


        win=Tk()
        frm=Frame(win)
        frm.pack(side=tk.LEFT,padx=20)

        tv=ttk.Treeview(frm,columns=(1,2,3),show="headings",height="5")
        tv.pack()
        tv.heading(1,text="Name")
        tv.heading(2,text="Voter ID")
        tv.heading(3,text="Email")
        for i in rows:
            print(i)
            tv.insert('','end',values=i)

    

        win.geometry('630x400')
        win.title('VoterList')
        win.mainloop()
        
    def signup():
        R1.destroy()
        def Signup_db():
            username = usernames.get()
            password = passwords.get()
            Uniquepass=passw()
            Userid= Userids.get()
            Votercardno= Votercardnos.get()
            emails=email_s.get()
            phoneno=phonenos.get()
            Adreses=Adresess.get()
            LoginAuth='no'
            FaceAuth='no'
            VoteAuth='no'
            votecardnum=""
            emailid=""
            if username == "" or password ==" " or Userid == "" or Votercardno == "" or emails == "" or phoneno == "" or Adreses == "" :
                    tkinter.messagebox.showinfo("sorry","Pease fill the required information")
            else:
                
                q1=database()
                query1=q1.cursor()
                query1.execute("SELECT * FROM facerec WHERE Votercardnos = %s", (Votercardno, ))
                result=query1.fetchall()
                for row in result:
                    votecardnum=row[4]
                    emailid=row[5]
                        
                print('votecardnum',votecardnum,emailid)
                        
                if(Votercardno==votecardnum):
                    print('eee')
                    tkinter.messagebox.showinfo("sorry","AllredyExist")
                else:
                    if username == "" or password=="" or Userid == "" or Votercardno == "" or emails == "" or phoneno == "" or Adreses == "" :
                        tkinter.messagebox.showinfo("sorry","Pease fill the required information")
                    else:
                        q2=database()
                        query2 = q2.cursor()
                        query2.execute("INSERT INTO facerec VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(username,password,Uniquepass,Userid,Votercardno,emails,phoneno,Adreses,LoginAuth,FaceAuth,VoteAuth))
                        q2.commit()
                        R2.destroy()
                        mai(emails,Uniquepass)
                        faceDetect(Votercardno,username,emails)
                        R2.destroy()
                            
                       
              
        R2=tkinter.Toplevel()
        R2.geometry('800x600')
        R2.title('Register Page')
        image=Image.open('Homepage.png')
        image=image.resize((800,600))
        photo_image=ImageTk.PhotoImage(image)
        label1=tkinter.Label(R2,image=photo_image)
        label1.place(x=0,y=0)
            
        la=Label(R2,text="REGISTER HERE",font=('algerian',15,'bold'))
        la.place(x=300,y=100)

        lblInfo=Label(R2,text="USERNAME",fg="black",font=("bold",15))
        lblInfo.place(x=200,y=140)

        lblInfo=Label(R2,text="PASSWORD",fg="black",font=("bold",15))
        lblInfo.place(x=200,y=190)

        lblInfo=Label(R2,text="USER ID",fg="black",font=("bold",15))
        lblInfo.place(x=200,y=240)

        lblInfo=Label(R2,text="VOTERCARD ID",fg="black",font=("bold",15))
        lblInfo.place(x=200,y=290)

        lblInfo=Label(R2,text="EMAIL",fg="black",font=("bold",15))
        lblInfo.place(x=200,y=340)

        lblInfo=Label(R2,text="PHONE NUM",fg="black",font=("bold",15))
        lblInfo.place(x=200,y=390)

        lblInfo=Label(R2,text="ADDRESS",fg="black",font=("bold",15))
        lblInfo.place(x=200,y=440)

        usernames=Entry(R2,width=20,font=("bold",15),highlightthickness=2)
        usernames.place(x=360,y= 140 )
            
        passwords=Entry(R2,show="**",width=20,font=("bold",15),highlightthickness=2)
        passwords.place(x=360,y=190 )
            
        Userids=Entry(R2,width=20,font=("bold",15),highlightthickness=2)
        Userids.place(x=360,y= 240 )
            
        Votercardnos=Entry(R2,width=20,font=("bold",15),highlightthickness=2)
        Votercardnos.place(x=360,y= 290 )

        email_s=Entry(R2,width=20,font=("bold",15),highlightthickness=2)
        email_s.place(x=360,y= 340 )

        phonenos=Entry(R2,width=20,font=("bold",15),highlightthickness=2)
        phonenos.place(x=360,y= 390 )

        Adresess=Entry(R2,width=20,font=("bold",15),highlightthickness=2)
        Adresess.place(x=360,y= 440 )
            

        signUpbt = Button(R2,text = "SignUp",width=10,height=2,fg="black",font=('algerian',15,'bold'),justify='center',bg="light blue",command=Signup_db)
        signUpbt.place( x =350,y=490)
              
        R2.mainloop()


    

    R1=tkinter.Toplevel()
    R1.geometry('800x600')
    R1.title('Home Page')
    image=Image.open('Homepage.png')
    image=image.resize((800,600))
    photo_image=ImageTk.PhotoImage(image)
    label1=tkinter.Label(R1,image=photo_image)
    label1.place(x=0,y=0)
    
    la=Label(R1,text="Hello Admin!!!",font=('algerian',15,'bold'))
    la.place(x=200,y=100)
    
    Registerbt = Button(R1,text = "REGISTER HERE",width=20,height=2,font=('algerian',15,'bold'),justify='center',bg="light blue",relief=SUNKEN,command=signup)
    Registerbt.place(x =140 ,y=475)

    image1=Image.open('register1.png')
    image1=image1.resize((250,250))
    photo_image1=ImageTk.PhotoImage(image1)
    label2=tkinter.Label(R1,image=photo_image1)
    label2.place(x=140,y=200)

    loginbt = Button(R1,text = "VIEW VOTER LIST",width=17,height=2,font=('algerian',15,'bold'),justify='center',bg="light blue",relief=SUNKEN,command=table)
    loginbt.place( x =450,y=475)

    image2=Image.open('docu.png')
    image2=image2.resize((250,250))
    photo_image2=ImageTk.PhotoImage(image2)
    label3=tkinter.Label(R1,image=photo_image2)
    label3.place(x=450,y=200)

    R1.mainloop()
#-----------------------------------------------------Login------------------------------------------------------------------------------------------------------    
def login():
    def login_db():
        Username_entryyy=''
        VoterId_entryyy=''
        Password_entryyy=''
        q3=database()
        query3 = q3.cursor()
        Username_entry = Username_entryy.get()
        VoterId_entry = VoterID_entryy.get()
        Password_entry = Password_entryy.get()
        if Username_entry == "" or Password_entry == "" or VoterId_entry=="":
            tkinter.messagebox.showinfo("sorry", "Please complete the required field")
            R3.destroy()
        else:
            query3.execute('SELECT * FROM facerec WHERE usernames = %s AND password = %s AND Votercardnos = %s ', (Username_entry, Password_entry, VoterId_entry))
            result1=query3.fetchall()
            for row1 in result1:
                Username_entryyy=row1[0]
                Password_entryyy=row1[1]
                VoterId_entryyy=row1[4]
            #print(Username_entry,Password_entry)
            if(Username_entry==Username_entryyy and Password_entry==Password_entryyy and VoterId_entry==VoterId_entryyy):
                tkinter.messagebox.showinfo("Welcome %s" % Username_entry, "Logged in successfully")
                R3.destroy()
                verification_frame(VoterId_entryyy)
                    
                    
            else:
                tkinter.messagebox .showinfo("Sorry", "Wrong Password")
      
        
    R3 = tkinter.Toplevel()
    R3.geometry('800x600')
    R3.title("LOGIN NOW")

    image=Image.open('Homepage.png')
    image=image.resize((800,600))
    photo_image=ImageTk.PhotoImage(image)
    label1=tkinter.Label(R3,image=photo_image)
    label1.place(x=0,y=0)
        
    la=Label(R3,text="LOGIN HERE",font=('algerian',20,'bold'))
    la.place(x=300,y=100)
        
    lblInfo1=Label(R3,text="USERNAME",fg="black",font=("bold",15))
    lblInfo1.place(x=230,y=200)
       
    lblInfo2=Label(R3,text="VOTERCARD ID",fg="black",font=("bold",15))
    lblInfo2.place(x=230,y=250)
        
    lblInfo2=Label(R3,text="PASSWORD",fg="black",font=("bold",15))
    lblInfo2.place(x=230,y=300)

    Username_entryy= Entry(R3,width=15,font=("bold",17),highlightthickness=2,bg="WHITE",relief=SUNKEN)
    Username_entryy.place(x=400, y=190)

    VoterID_entryy= Entry(R3,width=15,font=("bold",17),show="*",highlightthickness=2,bg="WHITE",relief=SUNKEN)
    VoterID_entryy.place(x=400, y=240)

    Password_entryy= Entry(R3,width=15,font=("bold",17),show="*",highlightthickness=2,bg="WHITE",relief=SUNKEN)
    Password_entryy.place(x=400, y=290)

    btn = Button(R3, text="LOGIN", width=10, height=2,fg="black",font=('algerian',15,'bold'),justify='center',bg="light blue",command=login_db)
    btn.place(x=380, y=400)
        
    R3.mainloop()
   

    


#-----------------------------Verication Id----------------------------------------

def system():

    
    def main1():
        R8.destroy()
        
    R8=tkinter.Toplevel()
    R8.geometry('900x600')
    R8.title('Thank you')
    image=Image.open('system.jpg')
    #path = "ThankYou.jpg"
    image1=image.resize((900,600))
    img = ImageTk.PhotoImage(image1)
    
    panel = Label(R8, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")


    
    la=Label(R8,text="",font=('algerian',15,'bold'))
    la.place(x=150,y=100)
    
    btn = Button(R8, text="Logout", width=10, height=2,fg="black",font=('algerian',15,'bold'),justify='center',bg="light blue",command=main1)
    btn.place(x=380, y=450)

    R8.mainloop()

def verification_frame(VoterId_entryyy):
    
    LoginAuth=""
    Uname_ver=""
    vote_ver=""
    email_ver=""
    uni_ver=""
    VoteAuth=""
    q4=database()
    query4 = q4.cursor()
    query4.execute('SELECT * FROM facerec WHERE Votercardnos = %s  ', (VoterId_entryyy, ))
    result2=query4.fetchall()
    for row2 in result2:
        Uname_ver=row2[0]
        uni_ver=row2[2]
        vote_ver=row2[4]
        email_ver=row2[5]
        LoginAuth=row2[8]
        VoteAuth=row2[10]
        
    print(VoteAuth)
    if(LoginAuth=='yes' and VoteAuth=='yes'):
        tkinter.messagebox.showinfo("Alredy Verified","Alredy Voted")
        system()

        
    elif(LoginAuth=='yes'):
        
        tkinter.messagebox.showinfo("Alredy Verified","Alredy Verified")
        voting_frame(Uname_ver,vote_ver,email_ver,uni_ver)
        
        
    else:
        def verification_db():
            Username_Verify=''
            U_password_Verify=''
            UserId_Verify=''
            VoterId_Verify=''
            Email_Verify=''

            q3=database()
            query3 = q3.cursor()
            User_ID_entry = User_ID.get()
            Voter_ID_entry = Voter_ID.get()
            Passwrd_U_ID_entry=Passwrd_U_ID.get()
        
        
            if User_ID_entry == "" or Voter_ID_entry == "" or Passwrd_U_ID_entry==''  :
                tkinter.messagebox.showinfo("sorry", "Please complete the required field")
            
            else:
                query3.execute('SELECT * FROM facerec WHERE Userids = %s AND Votercardnos = %s AND passwords = %s ', (User_ID_entry,Voter_ID_entry, Passwrd_U_ID_entry))
                result1=query3.fetchall()
                for row1 in result1:
                    Username_Verify=row1[0]
                    U_password_Verify=row1[2]
                    UserId_Verify=row1[3]
                    VoterId_Verify=row1[4]
                    Email_Verify=row1[5]
                
                print(Username_Verify,VoterId_Verify,Email_Verify)
                if(User_ID_entry==UserId_Verify and Voter_ID_entry==VoterId_Verify and Passwrd_U_ID_entry == U_password_Verify):
                    tkinter.messagebox.showinfo("Welcome %s" % Username_Verify, "Verified  successfully")
                    q5=database()
                    query5 = q5.cursor()
                    query5.execute("UPDATE facerec SET LoginAuth = 'yes' WHERE Votercardnos = %s",(Voter_ID_entry,))
                    q5.commit()
                    
                    R4.destroy()
                    voting_frame(Username_Verify,VoterId_Verify,Email_Verify,U_password_Verify)
                
                else:
                    tkinter.messagebox .showinfo("Sorry", "Wrong Password")
    
        
        
        R4 = tkinter.Toplevel()
        R4.geometry('800x600')
        R4.title("verification_Me")

        image=Image.open('Homepage.png')
        image=image.resize((800,600))
        photo_image=ImageTk.PhotoImage(image)
        label1=tkinter.Label(R4,image=photo_image)
        label1.place(x=0,y=0)
        
        lblInfo1=Label(R4,text="USER ID",fg="black",font=("bold",15))
        lblInfo1.place(x=230,y=200)
       
        lblInfo2=Label(R4,text="VOTER ID",fg="black",font=("bold",15))
        lblInfo2.place(x=230,y=250)

        lblInfo3=Label(R4,text="UPASSWORD",fg="black",font=("bold",15))
        lblInfo3.place(x=230,y=300)

        User_ID= Entry(R4,width=15,font=("bold",17),highlightthickness=2,bg="WHITE",relief=SUNKEN)
        User_ID.place(x=360, y=190)

        Voter_ID= Entry(R4,width=15,font=("bold",17),show="*",highlightthickness=2,bg="WHITE",relief=SUNKEN)
        Voter_ID.place(x=360, y=240)

        
        Passwrd_U_ID= Entry(R4,width=15,font=("bold",17),show="*",highlightthickness=2,bg="WHITE",relief=SUNKEN)
        Passwrd_U_ID.place(x=360, y=290)

        btn = Button(R4, text="VERIFYME", width=10, height=2,fg="black",font=('algerian',15,'bold'),justify='center',bg="light blue",command=verification_db)
        btn.place(x=380, y=400)
        
        R4.mainloop()

#-------------------------------------------------------Voting Session---------------------------------------------------------------------

def TrackImages(un,votev):
        FaceAuth=""
        Uname_ver=""
        vote_ver=""
        email_ver=""
        uni_ver=""
        Vote_Auth=""
        q4=database()
        query4 = q4.cursor()
        query4.execute('SELECT * FROM facerec WHERE Votercardnos = %s  ', (votev, ))
        result2=query4.fetchall()
        for row2 in result2:
            Uname_ver=row2[0]
            uni_ver=row2[2]
            vote_ver=row2[4]
            email_ver=row2[5]
            FaceAuth=row2[9]
            Vote_Auth=row2[10]
            
        print(FaceAuth)
        if(FaceAuth=='yes'):
            tkinter.messagebox.showinfo("Verified","Face  Allredy Verified")
        else:
    
            tt2=votev
            tt1=""
            recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
            recognizer.read("TrainingImageLabel\Trainner.yml")
            harcascadePath = "haarcascade_frontalface_default.xml"
            faceCascade = cv2.CascadeClassifier(harcascadePath);    
            df=pd.read_csv("VoterDetails\VoterDetails.csv", error_bad_lines=False)
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_SIMPLEX        
            col_names =  ['Id','name','Date','Time']
            attendance = pd.DataFrame(columns = col_names)
            #print(attendance)
            while True:
                ret, im =cam.read()
                gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                faces=faceCascade.detectMultiScale(gray, 1.2,5)    
                for(x,y,w,h) in faces:
                    cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                    Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                    if(conf < 50):
                        ts = time.time()      
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            
                        a1=df.loc[df['Id'] == Id]['name'].values
                            
                        tt=str(Id)+"-"+str(a1)
                        tt1=str(Id)
                        attendance.loc[len(attendance)] = [Id,a1,date,timeStamp]
                         
                            
                    else:
                        Id='Unknown'                
                        tt=str(Id)
                        tt1=str(Id)
                    if(conf > 75):
                        noOfFile=len(os.listdir("ImagesUnknown"))+1
                        cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
                    cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
                attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
                cv2.imshow('im',im) 
                if (cv2.waitKey(1)==ord('q')):
                    break
                elif (tt1==tt2):
                    print('detected')
                    tkinter.messagebox.showinfo("Face","Face Recogisation succesfull")
                    q6=database()
                    query6 = q6.cursor()
                    query6.execute("UPDATE facerec SET FaceAuth = 'yes' WHERE Votercardnos = %s",(tt1,))
                    q6.commit()
                    
                    break
                
            ts = time.time()      
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour,Minute,Second=timeStamp.split(":")
            fileName="list\list_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
            attendance.to_csv(fileName,index=False)
            cam.release()
            cv2.destroyAllWindows()
            #print(attendance)
            



def Thank_you(votev):
    q7=database()
    query7 = q7.cursor()
    query7.execute("UPDATE facerec SET VoteAuth = 'yes' WHERE Votercardnos = %s", (votev,))
    q7.commit()
    
    def main1():
        R6.destroy()
        
    R6=tkinter.Toplevel()
    R6.geometry('900x600')
    R6.title('Thank you')
    image=Image.open('ThankYou.jpg')
    #path = "ThankYou.jpg"
    image1=image.resize((900,600))
    img = ImageTk.PhotoImage(image1)
    
    panel = Label(R6, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")

    
    btn = Button(R6, text="Logout", width=10, height=2,fg="black",font=('algerian',15,'bold'),justify='center',bg="light blue",command=main1)
    btn.place(x=380, y=450)

    R6.mainloop()


def voting_frame(Username_Verify,VoterId_Verify,Email_Verify,U_password_Verify):
    un=Username_Verify
    votev=VoterId_Verify
    email_ver=Email_Verify
    def otp_frame(un,votev,email_ver):

        My_otp1=""
        FaceAuth=""
        Uname_ver=""
        vote_ver=""
        email_ver=""
        uni_ver=""
        Vote_Auth=""
        q4=database()
        otp_num=""
        query4 = q4.cursor()
        query4.execute('SELECT * FROM facerec WHERE Votercardnos = %s  ', (votev, ))
        result2=query4.fetchall()
        for row2 in result2:
            Uname_ver=row2[0]
            uni_ver=row2[2]
            vote_ver=row2[4]
            email_ver=row2[5]
            FaceAuth=row2[9]
            Vote_Auth=row2[10]
            
        print(FaceAuth)
        if(FaceAuth=='yes' and Vote_Auth=='yes'):
            tkinter.messagebox.showinfo("Verified","Voted Allredy!!!")
            system()
            
        
        elif(FaceAuth=='yes' and Vote_Auth=='no'):
                My_otp=otp(un,votev,email_ver)
                My_otp1=str(My_otp)
                def main1():
                    otp_num=otp1.get()
                    if(otp_num==My_otp1):
                        R9.destroy()
                        vote_here(un,votev)
                        
                    else:
                        tkinter.messagebox.showinfo("Verified","Wrong Otp")
                R9=tkinter.Toplevel()
                R9.geometry('400x400')
                R9.title('otp')
                image=Image.open('Homepage.png')
                #path = "ThankYou.jpg"
                image1=image.resize((400,400))
                img = ImageTk.PhotoImage(image1)
        
                panel = Label(R9, image = img)
                panel.pack(side = "bottom", fill = "both", expand = "yes")


                otpla=Label(R9,text="Enter OTP",font=('algerian',15,'bold'))
                otpla.place(x=150,y=100)
        
                otp1= Entry(R9,width=15,font=("bold",17),show="*",highlightthickness=2,bg="WHITE",relief=SUNKEN)
                otp1.place(x=100, y=150)
        
                btn = Button(R9, text="Verify OTP", width=10, height=2,fg="black",font=('algerian',15,'bold'),justify='center',bg="light blue",command=main1)
                btn.place(x=120, y=250)

                R9.mainloop()
        else:
            tkinter.messagebox.showinfo("Alredy","Face Registration Not verified")
        
        

    def vote_here(un,votev):
               
        FaceAuth=""
        Uname_ver=""
        vote_ver=""
        email_ver=""
        uni_ver=""
        Vote_Auth=""
        q4=database()
        query4 = q4.cursor()
        query4.execute('SELECT * FROM facerec WHERE Votercardnos = %s  ', (votev, ))
        result2=query4.fetchall()
        for row2 in result2:
            Uname_ver=row2[0]
            uni_ver=row2[2]
            vote_ver=row2[4]
            email_ver=row2[5]
            FaceAuth=row2[9]
            Vote_Auth=row2[10]
            
        print(FaceAuth)
        if(FaceAuth=='yes' and Vote_Auth=='yes'):
            tkinter.messagebox.showinfo("Verified","Voted Allredy!!!")
            system()
            
        
        elif(FaceAuth=='yes' and Vote_Auth=='no'):
            R5.destroy()

            global bjp,cong,jds,bjpcount,congcount,jdscount
            f = open("bjp.txt", "r")
            bjpcount=int(f.read())
            f.close()

            f = open("cong.txt", "r")
            congcount=int(f.read())
            f.close()

            f = open("jds.txt", "r")
            jdscount=int(f.read())
            f.close()

            print(bjpcount)



            def bjp():
                #bjp.configure(bg="red")
                #cong.configure(bg="green")
                #jds.configure(bg="green")
                window1.destroy()
                global bjpcount
                print("am in bjp")
                bjpcount+=1
                print(bjpcount)
                f = open("bjp.txt", "w")
                f.write(str(bjpcount))
                f.close()
                tkinter.messagebox.showinfo("DONE","Thank You For Voting....!!")
                Thank_you(vote_ver)
                
                
            def cong():
                #bjp.configure(bg="green")
                #cong.configure(bg="red")
                #jds.configure(bg="green")
                window1.destroy()
                global congcount
                print("am in cong")
                congcount+=1
                print(congcount)
                f = open("cong.txt", "w")
                f.write(str(congcount))
                f.close()
                tkinter.messagebox.showinfo("DONE","Thank You For Voting....!!")
                Thank_you(vote_ver)
               
                
            def jds():
                #bjp.configure(bg="green")
                #cong.configure(bg="green")
                #jds.configure(bg="red")
                global jdscount
                print("am in jds")
                jdscount+=1
                print(jdscount)
                f = open("jds.txt", "w")
                f.write(str(jdscount))
                f.close()
                tkinter.messagebox.showinfo("DONE","Thank You For Voting....!!")
                window1.destroy()
                Thank_you(vote_ver)

            window1=tkinter.Toplevel()
            window1.geometry('800x600')
            
            image4=Image.open('Homepage.png')
            window1.title('Vote')
            image=image4.resize((800,600))
            photo_image4=ImageTk.PhotoImage(image4)
            label4=tkinter.Label(window1,image=photo_image4)
            label4.place(x=0,y=0)
            
            l1=tkinter.Label (window1, text="BE PREPARED TO VOTE",font=("Helvetica", 18, "bold"))  
            l1.place(x=200,y=10)

            
            lbjp=tkinter.Label (window1, text="BJP",font=("Helvetica", 18, "bold"))  
            lbjp.place(x=80,y=110)

            lcon=tkinter.Label (window1, text="CONGRESS",font=("Helvetica", 18, "bold"))  
            lcon.place(x=80,y=210)

            ljds=tkinter.Label (window1, text="JDS",font=("Helvetica", 18, "bold"))  
            ljds.place(x=80,y=310)

            bjp=tkinter.Button(window1,text = "BJP",width=15,height=3,bg="green",command=bjp)
            bjp.place(x=300,y=100)

            cong=tkinter.Button(window1,text = "CONGRESS",width=15,height=3,bg="green",command=cong)
            cong.place(x=300,y=200)

            jds=tkinter.Button(window1,text = "JDS",width=15,height=3,bg="green",command=jds)
            jds.place(x=300,y=300)

            image=Image.open('b.png')
            print(image)
            image=image.resize((80,60))
            photo_image=ImageTk.PhotoImage(image)
            label1=tkinter.Label(window1,image=photo_image)
            label1.place(x=500,y=100)

            image1=Image.open('c.jpg')
            image1=image1.resize((80,60))
            photo_image1=ImageTk.PhotoImage(image1)
            label2=tkinter.Label(window1,image=photo_image1)
            label2.place(x=500,y=200)

            image2=Image.open('jds.jpg')
            image2=image2.resize((80,60))
            photo_image2=ImageTk.PhotoImage(image2)
            label3=tkinter.Label(window1,image=photo_image2)
            label3.place(x=500,y=300)

            window1.mainloop()

            
        else:
            
            tkinter.messagebox.showinfo("Alredy","Face Registration Not verified")
        

    

    R5=tkinter.Toplevel()
    R5.geometry('800x600')
    R5.title('Voting Desk Table')
    image=Image.open('Homepage.png')
    image=image.resize((800,600))
    photo_image=ImageTk.PhotoImage(image)
    label1=tkinter.Label(R5,image=photo_image)
    label1.place(x=0,y=0)
    
    la=Label(R5,text="VOTING DESK TABLE",font=('algerian',20,'bold'))
    la.place(x=250,y=50)
    
    image1=Image.open('face.jpg')
    image1=image1.resize((200,200))
    photo_image1=ImageTk.PhotoImage(image1)
    label3=tkinter.Label(R5,image=photo_image1)
    label3.place(x=100,y=100)
    
    image2=Image.open('vote.jpg')
    image2=image2.resize((200,200))
    photo_image2=ImageTk.PhotoImage(image2)
    label3=tkinter.Label(R5,image=photo_image2)
    label3.place(x=100,y=330)
    
    btn = Button(R5, text="FACE AUTHENTICATION", width=20, height=2,fg="black",font=('algerian',15,'bold'),justify='center',bg="light blue", command=partial(TrackImages,un,votev))
    btn.place(x=450, y=170)

    btn1 = Button(R5, text="VOTE_HERE", width=20, height=2,fg="black",font=('algerian',15,'bold'),justify='center',bg="light blue",command=partial(otp_frame,un,votev,email_ver))
    btn1.place(x=450, y=350)
    R5.mainloop()
    
#-------------------------------------------------------------------------------------------------------------------------
    
    
    
main()
