# Hi-Lo 

This is a simple number guessing game BUT with statistics for the local user. The game has 4 major sections, 

A. The game itself, which has the parts for generating a random number and comparing it with the users input to conclude if the user won or lost.

B. Statistics section, where the game will get the current users statistics using their username, from MySQL database.

C. Another section which display statistics but it displays every players statistic who has ever played the game on the local machine.

D. A shop section, where you can spend the money you have acquired from playing the game over a while, which you can show off when others check the leaderboard.





Prerequisites:
1. mysql-connector-python :
One can get mysql-connector-python by opening a command prompt in their python directory, and running the command 'pip install mysql-connector-python'

2. MySQL Database (preferably version 5.5) 
For the development of this project I have used MySQL from this website: https://www.filehorse.com/download-mysql-64/11653/download/, using a different version may affect the working of the program.

4. Python : You can get python from https://www.python.org/downloads/ .

Setting up the game with sql:
To get started, its better if you set the password for MySQL database as 'admin',and username will be 'root' as usual. If you have set a different password for MySQL, you can 
change the line #2 in the code to match with your password which looks like this: 'mydb=ss.connect(host="localhost",user="root",password="admin")'
