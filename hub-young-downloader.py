import os
import shutil
from PIL import Image

##########################################################################
# CUSTOM SETTINGS: edit this BEFORE running the program.

# 1. Specify your operating system user name
osuser = "user" # <-- edit this

# 2. (OPTIONAL) Edit the output path.
#    REMEMBER TO ADD ANOTHER BACKSLASH (\)
out_path = "C:\\Users\\"+osuser+"\\Desktop\\"

# 3. (OPTIONAL) Edit minimum width and height of images
minwidth = 1000
minheight = 1000

# DO NOT EDIT THIS PATH
book_path = "C:\\Users\\"+osuser+"\\AppData\\Local\\HUB young\\"
##########################################################################

print("\nMEBook Ripper")
print("(C) brearlycoffee.cf")

book_list = [dI for dI in os.listdir(book_path) if os.path.isdir(os.path.join(book_path,dI))]
print("\n[Your library - About",str(len(book_list)),"books found]")
for i in range(len(book_list)):
    print("["+book_list[i]+"]")
    
notvalid = True
while notvalid:
    codein = input('\nInsert the book directory: ')
    codein = codein.strip()
    for i in range(len(book_list)):
        if codein == book_list[i]:
            notvalid = False
            break
    if notvalid == False:
        if codein.isdigit():
            notvalid = False
        else:
            print("The code does not belong to any book.")
            notvalid = True
    else:
        print("Insert a valid book directory.")

book_path = book_path +codein+"\\"
out_path = out_path + codein+"\\"
os.mkdir(out_path)

print("Moving publication directory...")     
try:  
    shutil.move(book_path+"publication","C:\\Users\\user\\AppData\\Local\\HUB young\\")
except:
    pass

print("\nCopying files...")
print("Selected book: "+str(codein))
print("Source directory: "+book_path)
print("Destination directory: "+out_path)
count = 0
for root, dirs, files in os.walk(book_path):
    for file in files:
        path_file = os.path.join(root,file)
        try:
            page = Image.open(path_file)
        except:
            pass
        else: 
            width, height = page.size
            if width >= minwidth and height >= minheight:
                try:
                    shutil.copy2(path_file,out_path)
                except:
                    pass
                else:
                    count+=1
                    print(str(count)+" copied pages.", end="\r")

if count == 0:
    print("The directory does not contain any good resolution images.")
else:
    print("All pages copied.")
print("\nRestoring publication directory...")
try:  
    shutil.move("C:\\Users\\user\\AppData\\Local\\HUB young\\publication",book_path)
except:
    print("Failed!")
print("Done. Check: "+out_path)

