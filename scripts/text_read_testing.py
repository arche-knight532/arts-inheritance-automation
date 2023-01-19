import pytesseract
import pyscreenshot as ImageGrab
from PIL import Image
#import schedule

import time
from configparser import ConfigParser


#TODO:
# - Add descriptionless art checker
# - Add actual code to control the Switch
# - Have code stop pulling after pullLimit art pulls
#Bonus features:
# - If logging is set to "enabled", log data on pulls into a dict object, load into a file at end of run

def loadConfig():
    global x1, x2, y1, y2, arts, description, pullLimit, logging
    print("loading config")
    config = ConfigParser()
    config.read("config.ini")
    #print(config.sections())
    x1 = int(config["DEFAULT"]["x1"])
    x2 = int(config["DEFAULT"]["x2"])
    y1 = int(config["DEFAULT"]["y1"])
    y2 = int(config["DEFAULT"]["y2"])
    #potentially strip each item in arts to user-proof this?
    arts = config["DEFAULT"]["arts"].split(",")
    description = config["DEFAULT"]["description"].split(",")
    pullLimit = int(config["DEFAULT"]["pullLimit"])
    logging = config["DEFAULT"]["logging"]

def takeScreenshot():
    print("taking screenshot")
    image_name = "screenshot.png"
    screenshot = ImageGrab.grab()
    filepath = f".\\{image_name}"
    screenshot.save(filepath)
    print("screenshot saved")
    return filepath

def cropImage():
    print("cropping image")
    image_name = "screenshot.png"
    img = Image.open(image_name)
    imgCropped = img.crop(box = (x1, y1, x2, y2))
    #imgCropped.show()
    imgCropped.save("screenshot.png")
    print("cropped image saved")

def checkArtName():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    #print(pytesseract.image_to_string(Image.open('test2.png')))
    artPulled = pytesseract.image_to_string(Image.open('screenshot.png')).strip()
    print(f"Art pulled: {artPulled}")
    return artPulled in arts

def checkDescriptionless():
    pass
    #Code for checking if an art is descriptionless

def countArtPulls():
    pass
    #Code for counting art pulls goes here

def writeLogFile():
    pass
    #Code for output log file on art pulls goes here

def main():
    #artsLog to be dict data type, only used if logging == "enabled"
    global artsLog
    loadConfig()
    takeScreenshot()
    cropImage()
    isInArtList = checkArtName()
    if isInArtList:
        print("Art pulled in requested arts")
    else:
        print("Art pulled not in requested arts")

if __name__ == '__main__':
    main()





#print(pytesseract.image_to_string('test_image.png'))
#print(pytesseract.get_languages(config=''))
#print(pytesseract.image_to_boxes(Image.open('test.png')))

#schedule.every(5).seconds.do(takeScreenshot)
#while True:
#    schedule.run_pending()
#    time.sleep(1)
