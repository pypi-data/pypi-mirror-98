import os
import zipfile

class fileController:

    def help(self):
        print('--FileController--')
        print('You can find a link to the documentation here:')
        print()

    def readFile(self, filename):
        print('-------------------------------------')
        with open(filename, 'r') as f:
            i = 1
            for line in f:
                print(f'{i}) {line.strip()}')
                i += 1
        print('-------------------------------------')

    def writeToFile(self, filename, text):
        with open(filename, 'a+') as f:
            f.write(f'{text}\n')

        print('-------------------------------------')
        print('Successfully added note')
        print('-------------------------------------')

    def editFile(self, filename, noteLine, noteText):
        with open(filename, 'r') as f:
            fList = f.readlines()

        noteLine -= 1
        fList[noteLine] = noteText+'\n'

        with open(filename, 'w') as f:
            f.writelines(fList)

        print('-------------------------------------')
        print(f'Successfully edited note for line {noteLine}')
        print('-------------------------------------')

    def deleteFile(self, filename):
        with open(filename, 'r') as f:
            fList = f.readlines()

        del fList[:]

        with open(filename, 'w') as f:
            f.writelines(fList)

        print('-------------------------------------')
        print('Successfully deleted file elements')
        print('-------------------------------------')

    def getList(self, filename, list):
        with open(filename, 'r') as f:
            list = f.readlines()

        return list

    def writeList(self, filename, list):
        with open(filename, 'w') as f:
            f.writelines(list)
        print('-------------------------------------')
        print('Successfully written list')
        print('-------------------------------------')

    def deleteLine(self, filename, line):
        with open(filename, 'r') as f:
            fList = f.readlines()

        line -= 1
        fList.remove(line)

        with open(filename, 'w') as f:
            f.writelines(fList)

        print('-------------------------------------')
        print('Successfully deleted line')
        print('-------------------------------------')

    def createFile(self, filename):
        f = open(filename, 'x')
        print('-------------------------------------')
        print(f'Successfully created file {filename}')
        print('-------------------------------------')

    def zipFiles(self, number, zipname):
        zipname = zipname+'.zip'
        if number == 2:
            file1 = input("Enter the name/path of file 1: ")
            file2 = input("Enter the name/path of file 2: ")

            file1 = file1+'.txt'
            file2 = file2+'.txt'

            with zipfile.ZipFile(zipname, 'w') as zip_file:
                zip_file.write(file1)
                zip_file.write(file2)
        elif number == 3:
            file1 = input("Enter the name/path of file 1: ")
            file2 = input("Enter the name/path of file 2: ")
            file3 = input("Enter the name/path of file 3: ")

            file1 = file1+'.txt'
            file2 = file2+'.txt'
            file3 = file3+'.txt'

            with zipfile.ZipFile(zipname, 'w') as zip_file:
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

            with zipfile.ZipFile(zipname, 'w') as zip_file:
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

            with zipfile.ZipFile(zipname, 'w') as zip_file:
                zip_file.write(file1)
                zip_file.write(file2)
                zip_file.write(file3)
                zip_file.write(file4)
                zip_file.write(file5)
        print('-------------------------------------')
        print('Successfully zipped files')
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
            print('-------------------------------------')
            print('Successfully renamed file')
            print('-------------------------------------')
        elif uInput.upper() == "N":
            try:
                os.rename(old_name+'.txt', new_name+'.txt')

            except:
                os.rename(old_name, new_name)
            print('-------------------------------------')
            print('Successfully renamed file')
            print('-------------------------------------')
        else:
            print('[X] Error: Please enter a valid option.')

    def readZIP(self, filename):
        print('Is the ZIP file in a different directory? [Y/N]')
        uInput = input()


        if uInput.upper() == 'Y':
            print('-------------------------------------')
            file_path = input('Enter the directory of the file (not including the file): ')
            try:
                with zipfile.ZipFile(file_path+'\\'+filename+'.zip', 'r') as zip:
                    zip.printdir()
            except:
                with zipfile.ZipFile(file_path+'\\'+filename, 'r') as zip:
                    zip.printdir()
            print('-------------------------------------')
        elif uInput.upper() == 'N':
            print('-------------------------------------')
            try:
                with zipfile.ZipFile(filename+'.zip', 'r') as zip:
                    zip.printdir()
            except:
                with zipfile.ZipFile(filename, 'r') as zip:
                    zip.printdir()
            print('-------------------------------------')
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
            print('-------------------------------------')
            print('Successfully combined files.')
            print('-------------------------------------')
        except FileExistsError:
            print('[X] Error: Merged file name already exists')

    def exitFile(self):
        print('Quitting...')
        quit()

