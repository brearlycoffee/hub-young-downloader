import os
import shutil
from PIL import Image, ImageOps
import cv2 as cv

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

print("\nMEBook Image Downloader")
print("(C) brearlycoffee.cf")

# list all directories in path
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

book_path = book_path + codein + "\\"
out_path = out_path + codein + "\\"
os.mkdir(out_path)

# publication directory may contain images named like others files in other directories
# so i'm moving the folder and then restoring it.
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
maxwidth = 0
maxheight = 0
for root, dirs, files in os.walk(book_path):
    for file in files:
        path_file = os.path.join(root,file)
        try:
            page = Image.open(path_file)
        except: # the file is not an image
            pass
        else: 
            # acquiring width and height of every image
            width, height = page.size
            if width >= minwidth and height >= minheight:
                if width > maxwidth:
                    maxwidth = width
                if height > maxheight:
                    maxheight = height
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
else:
    print("Done.")

print("\nApplying borders to pages...")
print("Page size: "+str(maxwidth)+" x "+str(maxheight))
WHITE = [255,255,255]

imagelist = os.listdir(out_path)
for i in range(len(imagelist)):
    # stored image name
    name = imagelist[i]
    # imagelist[i] now contains the full path.
    imagelist[i] = out_path+imagelist[i]
    try:
        page = Image.open(imagelist[i])
    except: # the file is not an image
        pass
    else:
        width, height = page.size
        
        # calculating borders
        top = int((maxheight-height)/2)
        bottom = top
        if (maxheight-height)%2 != 0:
            top +=1
        left = int((maxwidth-width)/2)
        right = left
        if (maxwidth-width)%2 != 0:
            left +=1
        
        if top != 0 or bottom != 0 or left != 0 or right != 0:   
            src = cv.imread(cv.samples.findFile(imagelist[i]), cv.IMREAD_COLOR)
            dst = cv.copyMakeBorder(src, top, bottom, left, right, cv.BORDER_REPLICATE, None, WHITE)
            #dst = cv.copyMakeBorder(src, top, bottom, left, right, cv.BORDER_CONSTANT, None, WHITE)
            cv.imwrite(out_path+name,dst)

print("Done. Check: "+out_path)

