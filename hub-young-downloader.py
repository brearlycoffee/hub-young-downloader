import os
import shutil
from PIL import Image, ImageOps
import cv2 as cv
import pytesseract
import re 

##########################################################################
# CUSTOM SETTINGS: edit this BEFORE running the program.

# 1. Specify your operating system user name
osuser = "user" # <-- edit this

# 2. Specify Tesseract path
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# 3. (OPTIONAL) Search for page numbers in the last(DEFAULT)/first ?px
bottom_search = True
px_search = 100

# 4. (OPTIONAL) Edit the output path.
#    REMEMBER TO ADD ANOTHER BACKSLASH (\)
out_path = "C:\\Users\\"+osuser+"\\Desktop\\"

# 5. (OPTIONAL) Edit minimum width and height of images
minwidth = 1000
minheight = 1000

# DO NOT EDIT THIS PATH
book_path = "C:\\Users\\"+osuser+"\\AppData\\Local\\HUB young\\"
##########################################################################

print("\nHUB Young Downloader")
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
    print(str(count)+" pages copied.")
print("\nRestoring publication directory...")
try:  
    shutil.move("C:\\Users\\user\\AppData\\Local\\HUB young\\publication",book_path)
except:
    print("Failed!")
    
print("\nProcessing images (renaming + applying borders)...")
print("WARNING: These actions require several minutes, please wait...")
print("Page size: "+str(maxwidth)+" x "+str(maxheight))
WHITE = [255,255,255]

imagelist = os.listdir(out_path)
for i in range(len(imagelist)):
    # stored image name
    name = imagelist[i]
    # imagelist[i] now contains the full path.
    imagelist[i] = out_path+imagelist[i]
    
    page = cv.imread(imagelist[i])
    height, width, channels = page.shape
    
    #RENAMING---------------------------------------------------------------------------------
    if bottom_search == True:
        pagepart = page[(height-px_search):height, 0:width]   # crop 100px from bottom
    else:
        pagepart = page[0:px_search, 0:width]                 # crop 100px from top
    cv.imwrite(out_path+"pagepart.jpg",pagepart)    # create new image called pagepart.jpg
    
    '''
    imagepart = cv.imread(out_path+"pagepart.jpg")
    gray_imagepart = cv.cvtColor(imagepart, cv.COLOR_BGR2GRAY)
    cv.imwrite(out_path+"pagepart.jpg",gray_imagepart)
    '''
    # ocr scan pagepart.jpg
    pagedata = pytesseract.image_to_string(Image.open(out_path+"pagepart.jpg"))
    # detect all numbers
    pageids = re.findall(r'\d+', pagedata)
    
    if len(pageids) == 1:           # 1 number found (probably page number)
        maxid = int(pageids[0])
        idstr = (len(str(count))-len(str(maxid)))*"0"+str(maxid)
        shutil.move(out_path+name, out_path+idstr+".jpg")
    elif len(pageids) >= 2:         # 2+ numbers found (probably page number and chapter)
        maxid = 0
        for j in range(len(pageids)):
            
            # for example:
            # if pageids = ['135' , '2']
            # '135' is the page number
            # '2' is the chapter
            # so the biggest number (135) is the page number.
            if int(pageids[j]) > maxid and int(pageids[j]) <= count:
                maxid = int(pageids[j])
        
        idstr = (len(str(count))-len(str(maxid)))*"0"+str(maxid)
        shutil.move(out_path+name, out_path+idstr+".jpg")
    
    #APPLYING  BORDERS----------------------------------------------------------------
    top = int((maxheight-height)/2)
    bottom = top
    if (maxheight-height)%2 != 0:
        top +=1
    left = int((maxwidth-width)/2)
    right = left
    if (maxwidth-width)%2 != 0:
        left +=1
    
    if top != 0 or bottom != 0 or left != 0 or right != 0:   
        dst = cv.copyMakeBorder(page, top, bottom, left, right, cv.BORDER_REPLICATE, None, WHITE)
        #dst = cv.copyMakeBorder(src, top, bottom, left, right, cv.BORDER_CONSTANT, None, WHITE)
        cv.imwrite(out_path+name,dst)
print("File renaming (almost) completed.")
               
print("\nDeleting pagepart.jpg file...")
os.remove(out_path+"pagepart.jpg")

print("\nDone. Check: "+out_path)
print("I suggest you to check pages numbers.\nIf you find any mistakes, please manually rename them.")

