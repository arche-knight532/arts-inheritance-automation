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
    global x1, x2, x3, x4, y1, y2, y3, y4, arts, description, pullLimit, logging
    print("loading config")
    config = ConfigParser()
    config.read("config.ini")
    #print(config.sections())
    x1 = int(config["DEFAULT"]["x1"])
    x2 = int(config["DEFAULT"]["x2"])
    x3 = int(config["DEFAULT"]["x3"])
    x4 = int(config["DEFAULT"]["x4"])
    y1 = int(config["DEFAULT"]["y1"])
    y2 = int(config["DEFAULT"]["y2"])
    y3 = int(config["DEFAULT"]["y3"])
    y4 = int(config["DEFAULT"]["y4"])
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
    imgCroppedArt = img.crop(box = (x1, y1, x2, y2))
    imgCroppedDescription = img.crop(box = (x3, y3, x4, y4))
    #imgCropped.show()
    imgCroppedArt.save("artName.png")
    imgCroppedDescription.save("artDescription.png")
    print("cropped image saved")

def checkArtName():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    artPulled = pytesseract.image_to_string(Image.open('artName.png')).strip()
    print(f"Art pulled: '{artPulled}'")
    return artPulled

def checkArtDescription():
    #Code for checking if an art is descriptionless
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    artDescription = pytesseract.image_to_string(Image.open('artDescription.png')).strip()
    print(f"Art description: '{artDescription}'")
    return artDescription

def countArtPulls():
    pass
    #Code for counting art pulls goes here

def writeLogFile():
    pass
    #Code for output log file on art pulls goes here

def main():
    #artsLog to be dict data type, only used if logging == "enabled"
    global artsLog, artName, description
    iteration = 1
    loadConfig()
    while iteration <= pullLimit:
        print(f"iteration = {iteration}")
        takeScreenshot()
        cropImage()
        artName = checkArtName()
        description = checkArtDescription()
        #if artName in arts:
        #    print("Art pulled in requested arts")
        #else:
        #    print("Art pulled not in requested arts")
        time.sleep(1)
        if logging == "enable":
            countArtPulls()
        iteration += 1

    if logging == "enable":
        writeLogFile()

if __name__ == '__main__':
    main()





#print(pytesseract.image_to_string('test_image.png'))
#print(pytesseract.get_languages(config=''))
#print(pytesseract.image_to_boxes(Image.open('test.png')))

#schedule.every(5).seconds.do(takeScreenshot)
#while True:
#    schedule.run_pending()
#    time.sleep(1)
