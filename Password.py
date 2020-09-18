import random 
import array
from password_generator import PasswordGenerator

# maximum length of password needed 
# this can be changed to suit your password length 
def passw():
      

      pwo = PasswordGenerator()
      passw=pwo.generate()
      print(passw)
      return passw
