Prerequirements packages:
--------------------------
tkinter
threading

Steps to install or create the Desktop Application in windows :
-----------------------------------------------------------------

1 . Download the two files in the repository ( task_manager.py and icon.ico ) into a directory in your local machine
2 . once you done that open the command prompt ( make sure that you have installed python in your local machine and added to PATH of system Environment variables )
3 . Or add if you have dev shell alos , that's fine navigate to the folder where you have saved above two files .
4 . once you are in the folder / directory run this python command : python -m PyInstaller --onefile --windowed --icon=icon.ico task_manager.py

Once you ran the above command , if its successfully executed you would have got two folders created with some additional files in the same directory as you saved the above two files 
Then among the two created two folders , navigate to dist folder and ther eyou have a .exe file ..run it 
IT will open the Application
