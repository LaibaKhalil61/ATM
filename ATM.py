from os import system
import re
import mysql.connector
import sys
import time
try:
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="atm",
    charset="utf8"
    )
    if db.is_connected():
       print("DB is connected")
    mycursor = db.cursor()
except Exception as e:
   print("SQL Error:",e)
   sys.exit(1)
balance = 0
# Implementing the above functionalities in switch case using dictionaries
def transaction_history():
   global uID
   mycursor.execute("SELECT * FROM transaction WHERE SenderID=%s OR ReceiverID=%s",(uID,uID))
   result = mycursor.fetchall()
   if result:
    for x in result:
        if uID == x[1]:
           print("SenderID = ",x[1]," (You)")
           print("ReceiverID = ",x[2]) 
        else:
            print("SenderID = ",x[1])    
            print("ReceiverID = ",x[2]," (You)")    
        print("AmountTransfered = ",x[3])    
        print("--------------------------------")
def withdraw():
   global uID
   global balance
   amountToWithdraw = int(input("How much would you like to withdraw ?"))
   if amountToWithdraw<0:
       print("Invalid amount entered")
   elif amountToWithdraw <= balance:
      balance -= amountToWithdraw
      mycursor.execute("UPDATE user SET Balance=%s WHERE UserID=%s",(balance,uID))
      db.commit()
      print("Withdrawal successful")
   else:
      print("Balance is insufficient to make this withdrawal")
def Deposit():
    global balance
    amountToDeposit = int(input("How much would you like to deposit?"))
    if amountToDeposit>0:
        balance += amountToDeposit
        mycursor.execute("UPDATE user SET Balance=%s WHERE UserID=%s",(balance,uID))
        db.commit()
        print("Deposit successful")
    else:
       print("Invalid amount entered")
def Transfer():
    global uID
    global balance 
    # uID and balance are sender's 
    amountToTransfer = int(input("How much would you like to transfer ?"))
    if amountToTransfer<0:
        print("Invalid amount entered")
    elif amountToTransfer <= balance:
      accToTransfer = int(input("Enter accountNo. you want to transfer to :"))
      mycursor.execute("SELECT * FROM user WHERE AccountNo=%s",(accToTransfer,))
      result = mycursor.fetchone()
      if result:
        ReceiverBalance = result[3]
        receiverID = result[0]
        balance -= amountToTransfer
        mycursor.execute("UPDATE user SET Balance=%s WHERE UserID=%s",(balance,uID))
        db.commit()
        mycursor.execute("UPDATE user SET Balance=%s WHERE UserID=%s",(ReceiverBalance+amountToTransfer,receiverID))
        db.commit()
        mycursor.execute("INSERT INTO transaction(SenderID,ReceiverID,AmountTransfered) VALUES(%s,%s,%s)",(uID,receiverID,amountToTransfer))
        db.commit()
        print("Transfer successful")
      else:
        print("Receiver Account does not exist")
    else:
      print("Balance is insufficient to make this transaction")
   
switcher = {
   1:transaction_history,
   2:withdraw,
   3:Deposit,
   4:Transfer,
}
# USER MENU
print("Insert your Card")
time.sleep(5)
totalAttempts = 3
# Function to authenticate the user
def checkInDB(accNo,pin):
   global uID
   global mycursor
   global balance
   mycursor.execute("SELECT * FROM user WHERE AccountNo=%s AND Pin=%s",(accNo,pin))
   result = mycursor.fetchone()
   if result:
    uID = result[0]
    balance = result[3]
   return result
while totalAttempts>0:
    system("cls")
    while True:
        AccountNo = input("Enter your Account No. :")
        if len(AccountNo)>8 or len(AccountNo)<8:
            print("Error : AccountNo must be 8 characters long")
        elif re.search('r[a-z]',AccountNo):
            print("Error : AccountNo must contain numbers only")
        else:
            break
    while True:
        EnteredPin = input("Enter your pin :")
        if len(EnteredPin)>4 or len(EnteredPin)<4:
            print("Error : Pin must be 4 characters long")
        elif re.search('r[a-z]',EnteredPin):
                print("Error : Pin must contain numbers only")
        else:
            break
    if checkInDB(AccountNo,EnteredPin):
        break
    else:
     print("Error: Incorrect Credentials")
     totalAttempts -= 1
     if totalAttempts > 0:
        print("Remaining Attemps : ",totalAttempts)
     else:
        print("Your card is blocked")
        sys.exit()
    time.sleep(3)
while True:
    try:
        # Choices
        print("----------------------DASHBOARD-------------------------")
        print("Enter your choice")
        print("1.Transactions History")
        print("2.Withdraw")
        print("3.Deposit")
        print("4.Transfer")
        print("5.Quit")
        choice = int(input())
        if choice == 5:
            print("See you soon")
            sys.exit()
        else:
            switcher.get(choice,lambda:print("Please Enter a valid Choice :("))()
    except ValueError:
       print("Please Enter a valid Number")
   
   

