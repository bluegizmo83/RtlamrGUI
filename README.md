# RtlamrGUI
Windows GUI interface for the popular Rtlamr command line application used for reading utility meters with an RTL-SDR.

This GUI interface was created in Python 2.7 with PyQt4. To use this GUI interface, you have two options:
1. If you have Python 2.7 and PyQt4 installed on your system, just copy the files RtlamrGUI.pyw and RtlamrGUI.ui into the same folder where you installed Rtlamr to and then run RtlamrGUI.pyw
2. Download the the compiled exe file RtlamrGUI.exe and place it into the same folder you installed Rtlamr to and run it. The compiled exe does not require you to have python installed on your system, as it contains all of the necessary python dependencies packaged within it (hence the larger file size). 

NOTE: At the current time of posting this (9/17/2018), AVG is currently flagging and quarantining RtlamrGUI.exe, which has something to do with it being compiled through Pyinstaller. I have sent a copy of the exe to AVG's false positive team and am currently await review. 
