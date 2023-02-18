import mysql.connector as ss,random,time,pdb
mydb=ss.connect(host="localhost",user="root",password="admin")
c=mydb.cursor()
try:                                                                               #try n except to create database if it doesn't exist
    c.execute("create database hilo;")
except:
    pass                                                                                   #use database and create
c.execute("use hilo;")
try:
    c.execute("create table joe(user varchar(50),won int(5),lost int(5),money int(9),house varchar(60),plane varchar(60),nas varchar(60));")
except:
    pass
usloop,ingame,shloop,sta,rebet=0,0,0,0,0                                                 #make loop to ask for choice again
qq=input("""Hello there! 
Input 'login' if you have played the game once or 'register' to do the obvious, 
or input ctrl+c to terminate the program :D \n""")
#login or register
if qq=='login':
    while usloop<1:
        gname=input("Enter your username (reminder: usernames are case sensitive) \n")
        queery=("select * from joe where user='"+gname+"';")
        c.execute(queery)
        result=c.fetchone()                                                             #to check if user exists
        if result==None:
            print('User not found, make sure spelling is right \n')
        else:
            print("Hi,"+gname+"! \n")
            pname=gname
            usloop=+1
else:
    rname=input('Enter a cool name you would like us to refer you as:(reminder: usernames are case sensitive) \n')
    queery=("select * from joe where user='"+rname+"';")
    c.execute(queery)
    result=c.fetchone()                                                              #to check if user exists
    if result==None:
        rquery=('insert into joe values("'+rname+'"'+',0,0,100,"homeless","no","no");')     
        c.execute(rquery)
        mydb.commit()
        print("Registered user "+rname+'! \n')
        pname=rname
    else:
        print("User already exists, please try logging in")
        exit()
#introduction and initial input            
hi=input(
"""Welcome to Hi-Lo game!

Here's how to play the game:
1.Bet a x amount of money($), and guess if the upcoming number is higher or lower than the previous
one.
2.You start with 100$ in your bank.
3.If your guess is correct, your bet increases by 25-70 percent randomly.If you get one wrong guess, you lose.
4.The number will be in the range [0,10] and amount of money can be bet from [0,99]
5.This game will store your statistics and anyone who plays this game locally in the mySQL database.
6.If you have less money than the amount you have bet, the game will automatically add some money to your bank. \n
                                Press enter to enter main menu""")
#to get the variable 'money' to check if bet is more than money before starting the game
def moni():
    global money
    queery=("select * from joe where user="+"'"+pname+"';")
    c.execute(queery)
    x=c.fetchone()
    money=int(x[3])
moni()
while ingame<1:
    shloop,sta=0,0
    choice=input("""Would you like to:
    1. Play a new game
    2. Review your statistics
    3. See the high score board
    4. Open Shop
    5. See celebrities who have played this game
    6. Close this wonderful game \n""")
    if choice=='1':                #new bet,new game
        while rebet<1:
            bet=int(input("Enter an amount to bet(not more than 2 digits) \n"))
            if bet<0:
                print("You cannot have money in negative \n")
                break
            elif bet>money:                                                                      #work
                beg=print("You don't have enough money. Finding work, please wait \n")
                duh=random.randint(2,7)
                time.sleep(5)
                print("A shop accepted you for some hours, you earned "+str(duh*100)+" finally. \n")
                mquery=("update joe set money=money+"+str(duh)+" where user='"+pname+"';")
                moni()    
                break
            elif bet>=100:
                print("Read the instructions and retry \n")
                break
            else:
                print("Nice!,"+str(bet)+"($)"+"are placed on the table \n")
                rebet=rebet+1
                mquery=("update joe set money=money-"+str(bet)+" where user='"+pname+"';")
                c.execute(mquery)
                mydb.commit()
                break
        ai=random.randint(0,10)                     #choosing first number
        num=str(ai)
        print("Guess if the next random number will be lower/higher by typing 'l' and 'h' respectively \n")
        game=0
        while game<5:                               # game can be played 5 times to win
            ai2=random.randint(0,10)
            print("The number is,",ai)
            guess=input()
            pbet=int(bet)
            ppbet=str(pbet)
            if game==4:                             #condition to check if 5 times are over
                inbet=int(bet)
                wonm=str(inbet)
                print("You won! Your total amount is",inbet)
                game=+5
                wonquery=("update joe set won=won+1 where user='"+pname+"';")#add to sql
                betquery=("update joe set money=money+"+wonm+" where user='"+pname+"';")
                c.execute(wonquery)
                c.execute(betquery)
                rebet=0
                mydb.commit()
                print("Statistics updated")
            elif ai<ai2 and guess=='h':             #if guess is high and it is correct
                betinc=random.randint(25,70)
                print("Correct guess!,bet increased by",str(betinc)+"%",".")
                game=game+1
                bet=bet+(bet*betinc)/100
                ai=ai2
            elif ai>ai2 and guess=='l':             #if guess is low and it is correct
                betinc=random.randint(25,70)
                print("Correct guess!,bet increased by",str(betinc)+"%",".")
                game=game+1
                bet=bet+(bet*betinc)/100
                ai=ai2
            elif ai==ai2:                               #if the second number generated is the same as first number
                print('Generated number was same, no reward/loss')
            else:                                       #terminate loop if user loses and add to database
                print("Wrong guess, the number was",ai2," you lost! \n")
                print("Better luck next time!!!")
                lossquery=("update joe set lost=lost+1 where user='"+pname+"';")
                mquery="update joe set money=money-"+ppbet+" where user='"+pname+"';"
                c.execute(lossquery)
                mydb.commit()
                rebet=0
                game=game+100
        
        
    elif choice=='2':                                   #display statistics from sql for player
        while sta<1:
            c.execute(queery)
            x=c.fetchone()
            sta=+1
            print(pname+"'s statistics")    
            print("Player name:",x[0])
            print("Won:",x[1])
            print("Lost:",x[2])
            print("Bank:",x[3])
            print("Has a house?:",x[4])
            print("Has a plane?:",x[5])
            print("Owns NASA?:",x[6])
    elif choice=='3':                                   #display top on local leaderboard
        hquery="select * from joe order by won desc"
        c.execute(hquery)
        hrank=c.fetchall()
        for x in hrank:
            print(x[0]+"'s statistics")
            print("Player name:",x[0])
            print("Won:",x[1])
            print("Lost:",x[2])
            print("Bank:",x[3])
            print("Has a house?",x[4])
            print("Has a plane?:",x[5])
            print("Owns NASA?:",x[6])
            print()
    elif choice=='5':
        print('''
Player name: friedcheese
Won: 1000000
Lost: 21
Bank: 89 million
Has a house?:one big beautiful house
Owns NASA?:Owned

Player name: melanie martinez
Won: 2222222
Lost: 0
Bank: 88 million
Has a house?:one big beautiful house
Owns NASA?:Owned

Player name: olivia rodrigo
Won: 1
Lost: 2
Bank: 44
Has a house?:one big beautiful house
Owns NASA?:no

Player name:alec benjamin 
Won: 4
Lost: 6
Bank: 466
Has a house?:homeless
Owns NASA?:no

Player name: arjit singh
Won: 0
Lost: 2
Bank: 21
Has a house?:homeless
Owns NASA?:no
''')   
    elif choice=='6':                                           #exittttt
        print("Bye,",pname,"! closing the game.")
        ingame=+1
    elif choice=='4':                                           #enter shop
            while shloop<1:
                shoppe=input("""Welcome to the In-game shop!
        1. Buy a house
            cost=10,000 cash
        2. Buy a plane
            cost=30,000 cash
        3. Buy a cheese burger
            cost=10 cash
        4. Buy NASA
            cost=100,000
        5 Buy happiness
            cost=0
        6. Quit Shop \n""")
                if shoppe=='1':
                    moni()
                    if money<10000:
                        print("You can't afford a house yet,come back after earning money :P \n")
                    else:
                        print("Congrats, you're no longer homeless \n")
                        mquery=("update joe set money=money-10000 where user='"+pname+"';")
                        hquery="update joe set house='one big beautiful house' where user='"+pname+"';"
                        c.execute(hquery)
                        c.execute(mquery)
                        mydb.commit()
                elif shoppe=='2':
                    if money<30000:
                        print("You can't afford a plane yet, come back after earning money :P \n")
                    else:
                        print("Now you can fly to school")
                        mquery="update joe set money=money-30000 where user='"+pname+"';"
                        pquery="update joe set plane='one big plane' where user='"+pname+"';"
                        c.execute(pquery)
                        c.execute(mquery)
                        mydb.commit()
                elif shoppe=='3':
                    print("okay, delivering in 10 mins, leave the front door open \n")
                    mquery=("update joe set money=money-10 where user='"+pname+"';")
                    c.execute(mquery)
                    mydb.commit()
                elif shoppe=='4':
                    if money<100000:
                        print("You can't buy NASA yet,come back after earning money :P \n")
                    else:
                        naquery="select * from joe where user='"+pname+"';"
                        c.execute(naquery)
                        resultt=c.fetchone()
                        resulti=resultt[6]
                        if resulti=='no':
                            print("NASA is yours now")
                            mquery=("update joe set money=money-100000 where user='"+pname+"';")
                            nquery="update joe set nas='Owned' where user='"+pname+"';"
                            c.execute(mquery)
                            c.execute(nquery)
                            mydb.commit()
                        else:
                            print("You already own NASA \n")
                elif shoppe=='5':
                    print("You can't buy happiness. \n")
                elif shoppe=='6':
                    print("Quitting shop \n")
                    shloop=+1
                else:
                    print("Invalid choice,closing shop \n")
                    shloop=+1
            
                     
    else:
        print('Invalid choice, closing game \n')
        ingame=+1
mydb.close()



            
            
            
            
        
        
    
    
            

             




