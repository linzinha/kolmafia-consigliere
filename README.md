A mafia updater for either MacOS or Windows!

# Installation and setup

## Clone the project and run it
`git clone https://github.com/linzinha/kolmafia-consigliere.git`

`cd kolmafia-consigliere`

`pip3 install -r requirements.txt`

`python3 consigliere.py`
```
## Run the setup script to map the tool to either a new or existing Mafia location
=
╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭╮
┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃
┃┃ ╰╋━━┳━━━╮╭━━┳┳━━┫┃╭┳━━━┳━━┳━━━╮
┃┃ ╭┫╭╮┃ ╭╮ ┫━━╋┫╭╮┃┃┣┫ ┃━┫╭━┫ ┃━┫
┃╰━╯┃╰╯┃ ┃┃ ┣━━┃┃╰╯┃╰┫┃ ┃━┫┃ ┃ ┃━┫
╰━━━┻━━┻━╯╰━┻━━┻┻━╮┣━┻┻━━━┻╯ ╰━━━╯
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯

 Consigliere is a tool for updating your KoLmafia jar file, optimized for MacOS

Menu:
1: Run the setup script
2: Update Mafia
3: Run MacOS Patch fix
0: Exit
```
Select: `1`

The default folder will be your user's root folder:
```
#########################################
####      Installation    Setup      ####
#########################################

Menu:
1: Set destination folder [CURRENTLY /Users/linzinha]
2: Update Mafia
3: Run MacOS Patch fix
0: Exit
```

Select: `1`

```
Fill in the path, 
Enter the destination folder path (or c to [c]ancel)
--------------
```
Set New Destination Folder Path: /Users/linzinha/`Documents/KoLmafia`

You entered /Users/linzinha/Documents/KoLmafia, is this correct? ([y]es/[n]o/[c]ancel): `y`
```
Mafia folder has been set!

Menu:
1: Set destination folder [CURRENTLY /Users/linzinha/Documents/KoLmafia]
2: Update Mafia
3: Run MacOS Patch fix
0: Exit
```
Select: `0`

Goodbye!

# Running the updater
```
Menu:
1: Run the setup script
2: Update Mafia
3: Run MacOS Patch fix
0: Exit
```
Select: `2`

```
No JAR file found in the specified folder. Downloading a new one...
Downloaded and updated to the latest version.
```
You can also run the updater script independently, after `option1` **or** the `configure.py` script has been run **at least once**:
```
python3 updater.py
Latest version of Mafia is already installed.
```

# Running the Mac Patch script
When updating mafia, the script automatically runs chmod on the downloaded file to make it executable. 
However, if you don't need to update and have a manually downloaded .jar file you can use `mac_patch.py` to do this as well

Additionally, the Mac patch file has an option to create a sym link between the installed Mafia content and the location of the .jar file
This is to give you a folder structure like as in Windows, and does this by:
1. Temporarily moving the .jar file into a another folder named after its perent with `_tmp` appended at the end
2. Deleting the .jar file's containing folder
3. Creating a symlink named the same as the origina folder
4. Moving the .jar file into the symlink folder
5. Deleting the `_tmp` folder

**WARNING**: this might be a very dumb thing to do if you have the Mafia .jar file in your root directory, or if there are any other files the same folder as your .jar that you don't want deleted.
**Consider yourself warned!!**

## If additional files are found in the .jar file location:

```
################################
####      Mac    Patch      ####
################################

The MacOS patch can be used to create a symlink between: 

     a) the Mafia files in the Application Support folder 
     b) the location of the Jar file This is helpful for accessing script files and user logs.

It can also make an existing Jar file executable

Menu:
1: Create symlink
2: Make Jar executable
3: Run both
0: Return to the main menu
```

Select: `1`

```
found 4 additional files in that location
important_file.txt
important_file4.txt
important_file3.txt
important_file2.txt
```
Are you sure you want to continue? (y/n): `n`

*When selecting `n` at this step, the  Mac Patch menu is returned*
```
The MacOS patch can be used to create a symlink between: 

     a) the Mafia files in the Application Support folder 
     b) the location of the Jar file This is helpful for accessing script files and user logs.

It can also make an existing Jar file executable

Menu:
1: Create symlink
2: Make Jar executable
3: Run both
0: Return to the main menu
```
## If you attempt to run this on any operating system other than MacOS:
```
Menu:
1: Set destination folder [CURRENTLY C:\Users\Linzinha\Documents\KoLmafia]
2: Update Mafia
3: Run MacOS Patch fix
0: Exit
```
Select: `3`
```
################################
####      Mac    Patch      ####
################################

This patch is NOT meant to be run on Windows computers,
returning to the main menu.
```
