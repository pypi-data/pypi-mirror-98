# FileController v. 1.0.1 (Updated)
import os
import zipfile
import subprocess
from os.path import basename
from zipfile import ZipFile
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import *

class fileManager:

    def help(self):
        print('--FileController--')
        print('You can find a link to the project here:')
        print('https://pypi.org/project/filecontroller/')

    def readFile(self, filename):
        try:
            with open(filename, 'r') as f:
                i = 1
                for line in f:
                    print(f'{i}) {line.strip()}')
                    i += 1
        except FileNotFoundError:
            filename = filename+'.txt'
            with open(filename, 'r') as f:
                i = 1
                for line in f:
                    print(f'{i}) {line.strip()}')
                    i += 1

    def writeToFile(self, filename, text):
        with open(filename, 'a+') as f:
            f.write(f'{text}\n')

    def editFile(self, filename, noteLine, noteText):
        with open(filename, 'r') as f:
            fList = f.readlines()

        noteLine -= 1
        fList[noteLine] = noteText+'\n'

        with open(filename, 'w') as f:
            f.writelines(fList)

    def deleteFile(self, filename):
        with open(filename, 'r') as f:
            fList = f.readlines()

        del fList[:]

        with open(filename, 'w') as f:
            f.writelines(fList)

    def getList(self, filename):
        with open(filename, 'r') as f:
            list = f.readlines()

        return list

    def writeList(self, filename, list):
        with open(filename, 'w') as f:
            f.writelines(list)

    def deleteLine(self, filename, line):
        with open(filename, 'r') as f:
            fList = f.readlines()

        line -= 1
        fList.remove(line)

        with open(filename, 'w') as f:
            f.writelines(fList)

    def createFile(self, filename):
        f = open(filename, 'x')
        print('-------------------------------------')
        print(f'Successfully created file {filename}')
        print('-------------------------------------')

    def renameFile(self, old_name, new_name):
        print("Is the file in a different directory? [Y/N]")
        uInput = input()

        if uInput.upper() == "Y":
            file_path = input("Enter the path of the file (not including the file): ")
            try:
                os.rename(file_path+'\\'+old_name+'.txt', file_path+'\\'+new_name+'.txt',)
            except:
                os.rename(file_path+'\\'+old_name, file_path+'\\'+new_name+'.txt')
            print('Successfully renamed file')
        elif uInput.upper() == "N":
            try:
                os.rename(old_name+'.txt', new_name+'.txt')

            except:
                os.rename(old_name, new_name)
            print('Successfully renamed file')
        else:
            print('[X] Error: Please enter a valid option.')

    def combine(self, file1, file2, merged_file):
        data = data2 = ""

        try:
            with open(file1+'.txt') as fp:
                data = fp.read()

            with open(file2+'.txt') as fp:
                data2 = fp.read()
        except FileNotFoundError:
            with open(file1) as fp:
                data = fp.read()

            with open(file2) as fp:
                data2 = fp.read()

        data += "\n"
        data += data2

        try:
            with open(merged_file+'.txt', 'x') as fp:
                fp.write(data)
            print('Successfully combined files.')
        except FileExistsError:
            print('[X] Error: Merged file name already exists')

    def credits(self):
        root = Tk()
        root.withdraw()
        showinfo("FileController", "Copyright (C) 2021 Alex M. (alex.m)\nRead full license for more information")

    def replaceWord(self, filename, oldWord, newWord):
        filename = str(filename)
        oldWord = str(oldWord)
        newWord = str(newWord)

        try:
            with open(filename, 'r') as f:
                fList = f.readlines()

            res = [sub.replace(oldWord, newWord) for sub in fList]

            with open(filename, 'w') as f:
                f.writelines(res)
        except FileNotFoundError:
            filename = filename+'.txt'

            with open(filename, 'r') as f:
                fList = f.readlines()

            res = [sub.replace(oldWord, newWord) for sub in fList]

            with open(filename, 'w') as f:
                f.writelines(res)

    def exitFile(self):
        print('Quitting...')
        quit()


class zipManager():
    def zipFiles(self, number, zipname):
        zipname = zipname+'.zip'
        if number == 2:
            file1 = input("Enter the name/path of file 1: ")
            file2 = input("Enter the name/path of file 2: ")

            file1 = file1+'.txt'
            file2 = file2+'.txt'

            with ZipFile(zipname, 'w') as zip_file:
                zip_file.write(file1)
                zip_file.write(file2)
        elif number == 3:
            file1 = input("Enter the name/path of file 1: ")
            file2 = input("Enter the name/path of file 2: ")
            file3 = input("Enter the name/path of file 3: ")

            file1 = file1+'.txt'
            file2 = file2+'.txt'
            file3 = file3+'.txt'

            with ZipFile(zipname, 'w') as zip_file:
                zip_file.write(file1)
                zip_file.write(file2)
                zip_file.write(file3)
        elif number == 4:
            file1 = input("Enter the name/path of file 1: ")
            file2 = input("Enter the name/path of file 2: ")
            file3 = input("Enter the name/path of file 3: ")
            file4 = input("Enter the name/path of file 4: ")

            file1 = file1+'.txt'
            file2 = file2+'.txt'
            file3 = file3+'.txt'
            file4 = file4+'.txt'

            with ZipFile(zipname, 'w') as zip_file:
                zip_file.write(file1)
                zip_file.write(file2)
                zip_file.write(file3)
                zip_file.write(file4)
        elif number == 5:
            file1 = input("Enter the name/path of file 1: ")
            file2 = input("Enter the name/path of file 2: ")
            file3 = input("Enter the name/path of file 3: ")
            file4 = input("Enter the name/path of file 4: ")
            file5 = input("Enter the name/path of file 5: ")

            file1 = file1+'.txt'
            file2 = file2+'.txt'
            file3 = file3+'.txt'
            file4 = file4+'.txt'
            file5 = file5+'.txt'

            with ZipFile(zipname, 'w') as zip_file:
                zip_file.write(file1)
                zip_file.write(file2)
                zip_file.write(file3)
                zip_file.write(file4)
                zip_file.write(file5)
        print('-------------------------------------')
        print('Successfully zipped files')
        print('-------------------------------------')

    def readZIP(self, filename):
        print('Is the ZIP file in a different directory? [Y/N]')
        uInput = input()

        if uInput.upper() == 'Y':
            file_path = input('Enter the directory of the file (not including the file): ')
            try:
                with ZipFile(file_path+'\\'+filename+'.zip', 'r') as zip:
                    zip.printdir()
            except:
                with ZipFile(file_path+'\\'+filename, 'r') as zip:
                    zip.printdir()
        elif uInput.upper() == 'N':
            try:
                with ZipFile(filename+'.zip', 'r') as zip:
                    zip.printdir()
            except:
                with ZipFile(filename, 'r') as zip:
                    zip.printdir()
        else:
            print('[X] Error: Please enter a valid option.')

    def extract(self, filename):
        try:
            # opening the zip file in READ mode
            with ZipFile(filename, 'r') as zip:
                # printing all the contents of the zip file
                zip.printdir()

                # extracting all the files
                print('Extracting all the files now...')
                zip.extractall()
                print('Done!')
        except FileNotFoundError:
            # opening the zip file in READ mode
            with ZipFile(filename+'.zip', 'r') as zip:
                # printing all the contents of the zip file
                zip.printdir()

                # extracting all the files
                print('Extracting all the files now...')
                zip.extractall()
                print('Done!')


class fileGUI:
    def __init__(self, master):
        global window
        window = master
        # Basic tkinter loop
        master.title("Untitled - Notepad")
        master.geometry("644x788")

        # Add TextArea (Text Label)
        self.TextArea = Text(master, font="lucida 13")
        self.file = None
        self.TextArea.pack(expand=True, fill=BOTH)

        # Add MenuBar
        self.MenuBar = Menu(master)
        # Add "File" menu
        self.FileMenu = Menu(self.MenuBar, tearoff=0)
        # New File
        self.FileMenu.add_command(label="New", command=self.newFile)

        # Already existing file
        self.FileMenu.add_command(label="Open", command=self.openFile)

        # Save current file
        self.FileMenu.add_command(label="Save", command=self.saveFile)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Exit", command=self.quitApp)
        self.MenuBar.add_cascade(label="File", menu=self.FileMenu)

        # Add "Edit" menu
        self.EditMenu = Menu(self.MenuBar, tearoff=0)
        # Cut / Copy / Paste
        self.EditMenu.add_command(label="Cut", command=self.cut)
        self.EditMenu.add_command(label="Copy", command=self.copy)
        self.EditMenu.add_command(label="Paste", command=self.paste)

        self.MenuBar.add_cascade(label="Edit", menu=self.EditMenu)

        # Add "Help" menu
        self.HelpMenu = Menu(self.MenuBar, tearoff=0)
        self.HelpMenu.add_command(label="About Notepad", command=self.about)
        self.MenuBar.add_cascade(label="Help", menu=self.HelpMenu)

        master.config(menu=self.MenuBar)

        # Adding Scrollbar
        Scroll = Scrollbar(self.TextArea)
        Scroll.pack(side=RIGHT, fill=Y)
        Scroll.config(command=self.TextArea.yview)
        self.TextArea.config(yscrollcommand=Scroll.set)

    def newFile(self):
        global file
        window.title("Untitled - Notepad")
        file = None
        self.TextArea.delete(1.0, END)

    def openFile(self):
        global file
        file = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if file == "":
            file = None
        else:
            window.title(basename(file) + " - Notepad")
            self.TextArea.delete(1.0, END)
            with open(file, "r") as f:
                self.TextArea.insert(1.0, f.read())

    def saveFile(self):
        global file
        if file is None:
            file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                     filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

            if file == "":
                file = None
            else:
                # Saves as a new file
                with open(file, "w") as f:
                    f.write(self.TextArea.get(1.0, END))

                window.title(basename(file) + " - Notepad")
        else:
            # Save the file
            with open(file, "w") as f:
                f.write(self.TextArea.get(1.0, END))

    def quitApp(self):
        window.destroy()

    def cut(self):
        window.event_generate("<<Cut>>")

    def copy(self):
        window.event_generate("<<Copy>>")

    def paste(self):
        window.event_generate("<<Paste>>")

    def about(self):
        showinfo("Notepad", "Notepad v. 1.0.0")


class zipGUI:
    def __init__(self, master):
        # Variables
        self.file_sel = ""

        master.title("FileController - ZIP Editor")
        # General structure of the window
        self.frame1 = ttk.LabelFrame(master, height=100, width=400, text="Actions")
        self.frame1.pack(padx=10, pady=10)
        self.frame2 = ttk.LabelFrame(master, height=100, width=400, text="Information about zip file")
        self.frame2.pack(padx=10, pady=10)
        self.frame3 = ttk.LabelFrame(master, height=100, width=400, text="List of files and folders inside zip file")
        self.frame3.pack(padx=10, pady=10)
        # Frame 1 : buttons
        # Button 1
        self.button1 = ttk.Button(self.frame1, text="Browse zip file", command=self.button_file)
        self.button1.pack(side=LEFT, padx=10, pady=10)
        self.logo1 = PhotoImage(file="res\\zipfile.png")
        self.small_logo1 = self.logo1.subsample(6, 6)
        self.button1.config(image=self.small_logo1, compound=LEFT)
        # Button 2
        self.button2 = ttk.Button(self.frame1, text="Unzip directory", command=self.change_dir)
        self.button2.pack(side=LEFT, padx=10, pady=10)
        self.logo2 = PhotoImage(file="res\\folder.png")
        self.small_logo2 = self.logo2.subsample(6, 6)
        self.button2.config(image=self.small_logo2, compound=LEFT)
        # Button 3
        self.button3 = ttk.Button(self.frame1, text="ExtractAll")
        self.button3.pack(side=LEFT, padx=10, pady=10)
        self.logo3 = PhotoImage(file="res\\extract_all.png")
        self.small_logo3 = self.logo3.subsample(6, 6)
        self.button3.config(image=self.small_logo3, compound=LEFT, state="disabled", command=self.button_extract_all)
        # Button 4
        self.button4 = ttk.Button(self.frame1, text="Extract Selection")
        self.button4.pack(side=LEFT, padx=10, pady=10)
        self.logo4 = PhotoImage(file="res\\select.png")
        self.small_logo4 = self.logo4.subsample(12, 12)
        self.button4.config(image=self.small_logo4, compound=LEFT, state="disabled", command=self.button_extract_sel)
        # Frame 2 : data
        self.label_frame_2 = ttk.Label(self.frame2, text="Select a zip file", width=100)
        self.label_frame_2.pack(padx=10, pady=10)
        # Frame 3 : files list
        self.treeview = ttk.Treeview(self.frame3, show="tree", selectmode="extended")
        self.treeview.pack(padx=10, pady=10)
        self.treeview["column"]=("one")
        self.treeview.column("one", width=400)
        self.treeview.bind("<<TreeviewSelect>>", self.callback)
        # Bottom label
        self.label1 = ttk.Label(master)
        self.label1.pack()


    def callback(self, event):
        """ Enable the button 4 """
        self.button4.config(state="enabled")
        print(self.treeview.selection())

    def button_file(self):
        """ Select zip file """
        self.file_sel = self.find_file("file")
        if self.is_zip(self.file_sel):
            zip1 = ZipData(self.file_sel)
            self.update_label(1)
            self.label_frame_2.config(text="You have selected the zip file " + self.file_sel + "\n" + str(zip1.len_zip()) + " items found in the zip file")
            self.button3.config(state="enabled")
            print(zip1.info())
            for elt in zip1.info():
                elt_split = elt.split("/")
                if "" in elt_split:
                    elt_split.remove("")
                if len(elt_split)==1:
                    self.treeview.insert("", "end", elt_split[0], text=elt_split[0])
                elif len(elt_split)>1:
                    self.treeview.insert("/".join(elt_split[0:-1]), "end", "/".join(elt_split), text=elt_split[-1])

    def button_extract_all(self):
        """ Extract all files in the zip file """
        if self.file_sel != "":
            zip1 = ZipData(self.file_sel)
            zip1.extract_all()
            self.clean_window()
        else:
            messagebox.showerror("Zip file missing", "You need to select a zip file")

    def button_extract_sel(self):
        """ Extract selected files in the zip file """
        if self.file_sel != "":
            zip1 = ZipData(self.file_sel)
            zip1.extract_sel(self.treeview.selection())
            self.clean_window()
        else:
            messagebox.showerror("Zip file missing", "You need to select a zip file")

    def clean_window(self):
        """ Clean the main window after extraction """
        self.update_label(2)
        self.label_frame_2.config(text="")
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        subprocess.Popen("explorer " + os.getcwd())

    @staticmethod
    def find_file(f_type):
        """ Return the path of the zip file or folder """
        f_name = ""
        if f_type == "file":
            file_name = filedialog.askopenfile()
            f_name = file_name.name
        if f_type == "folder":
            f_name = filedialog.askdirectory()
        return f_name

    @staticmethod
    def find_dir():
        """ Find the current directory """
        cwd = os.getcwd()
        return cwd

    @staticmethod
    def is_zip(zip_path):
        """ Check if the selected file is a zip file """
        if zip_path[-4:]!=".zip":
            messagebox.showerror("Type file error", "You need to select a zip file")
            return False
        else:
            return True

    def change_dir(self):
        """ Change the current directory """
        dir_path = self.find_file("folder")
        os.chdir(dir_path)
        self.update_label(1)

    def update_label(self, val):
        """ Update the text of the label at the bottom of the window """
        if val==1:
            self.label1.config(text="The zip file will be extracted in the directory " + self.find_dir())
        if val==2:
            self.label1.config(text="Zip file successfully extracted")

class ZipData:
    def __init__(self, file):
        self.file = file

    def extract_all(self):
        """ Extract all the files of the zip folder """
        with zipfile.ZipFile(self.file, 'r') as z:
            z.extractall()

    def extract_sel(self, file_name):
        """ Extract selected files """
        with zipfile.ZipFile(self.file, 'r') as z:
            for f_name in file_name:
                z.extract(f_name)

    def len_zip(self):
        """ Count the number of items in the zip file """
        with zipfile.ZipFile(self.file, 'r') as z:
            nb_items = len(z.namelist())
            return nb_items

    def info(self):
        """ Return the list of items inside the zip file """
        with zipfile.ZipFile(self.file, 'r') as z:
            return z.namelist()


if __name__ == '__main__':
    root = Tk()
    win = zipGUI(root)
    root.mainloop()