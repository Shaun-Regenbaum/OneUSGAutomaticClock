# OneUSGAutomaticClock (updated 12-20-20)
This is a little script for Georgia Tech students to be able to automatically clock hours without worrying about forgetting to turn it off.

It can be easily modified to work for any university in the USG system 
(If you have any questions on how to do this, feel free to reach out, I can make a fork that works for any of the universities). 

You need Python 2.7+ (or 3), selenium, and chromedriver_autoinstaller.
To get Python simply click [here](https://www.python.org/downloads/).
Once you have python, go to any terminal and write the following two things:

`pip install selenium`

`pip install chromedriver_autoinstaller`

Finally, go to the *clock_manager.py* file and edit the user_variables to clock how many hours you want. 



Otherwise, simply clone the repo, fill out the details in the script (*clock_manager.py*) for yourself and run the file and it'll work!

You will need to confirm on duo 2fa one time (they dont have an API sadly).

I know that getting code up and running can be very frustrating, so please if you have any problems with python or cloning the repe (or anything else) reach out to me at shaunregenbaum@gmail.com or leave an issue!
If you have any others questions at all, please reach out!

Note: If you want to do this manually, or having problems, you can download the appropriate chromedriver for your OS from [here](https://sites.google.com/a/chromium.org/chromedriver/home). You will need to manually add this driver to your path and and modify the code to correctly reference it [as such](https://chromedriver.chromium.org/getting-started).

