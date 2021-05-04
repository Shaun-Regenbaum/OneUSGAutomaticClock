# ⏰ OneUSGAutomaticClock ⏰
## CURRENT STATUS: WORKING ✅
This is a little script for Georgia Tech students to be able to automatically clock hours without worrying about forgetting to turn it off.

It can be easily modified to work for any university in the USG system 
(If you have any questions on how to do this, feel free to reach out, I can make a fork that works for any of the universities). 

## Requirements + Background Information:
- Python 3.9+ [Find Here](https://www.python.org)
- selenium [Find Here](https://www.selenium.dev/documentation/en/)
- chromedriver_autoinstaller [Find Here](https://pypi.org/project/chromedriver-autoinstaller/)

## Set-Up Instructions: 
To get Python simply click [here](https://www.python.org/downloads/).
**Make sure to install Python 3.9 or Later**
Once you have python, go to any terminal and write the following two things:

`pip3 install selenium`

`pip3 install chromedriver_autoinstaller`

Then clone the repo. For self-help on how to clone a repo click [here](https://www.howtogeek.com/451360/how-to-clone-a-github-repository/), otherwise reach out and I will help you (seriously I will sit down with you and guide you through it)!

Finally, go to the *clock_manager.py* file and edit the User Variables to clock how many hours you want. 
![A screenshot of the User Variables Code](https://github.com/Shaun-Regenbaum/OneUSGAutomaticClock/blob/master/Pictures/User%20Variables.PNG)

After all that, just run the script, sit back and relax (while doing your work).

Just note, you will need to confirm on duo 2fa (two factor authentication) one time.

## Help and Contact Info:
I know that getting code up and running can be very frustrating 😓😖, so please if you have any problems with python or cloning the repo (or anything else) reach out to me at shaunregenbaum@gmail.com or leave an issue 😎😁!
If you have any others questions at all, please reach out!

## Note: 
If you want to get the chromedriver manually, or are having problems, you can download the appropriate chromedriver for your OS from [here](https://sites.google.com/a/chromium.org/chromedriver/home). You will need to manually add this driver to your environment path and and modify the code to correctly reference it [as such](https://chromedriver.chromium.org/getting-started).

