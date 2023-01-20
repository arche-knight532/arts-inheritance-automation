import pytesseract
import pyscreenshot as ImageGrab
from PIL import Image

from configparser import ConfigParser


def loadConfig():
    #loads config file "config.ini"
    global x1, x2, x3, x4, y1, y2, y3, y4, tesseractLocation
    config = ConfigParser()
    config.read("config.ini")

    x1 = int(config["DEFAULT"]["x1"])
    x2 = int(config["DEFAULT"]["x2"])
    x3 = int(config["DEFAULT"]["x3"])
    x4 = int(config["DEFAULT"]["x4"])
    y1 = int(config["DEFAULT"]["y1"])
    y2 = int(config["DEFAULT"]["y2"])
    y3 = int(config["DEFAULT"]["y3"])
    y4 = int(config["DEFAULT"]["y4"])
    tesseractLocation = config["DEFAULT"]["tesseractLocation"]


def takeScreenshot():
    #takes screenshot, save to screenshot.png in current directory
    image_name = "screenshot.png"
    screenshot = ImageGrab.grab()
    filepath = f".\\{image_name}"
    screenshot.save(filepath)


def cropImage():
    #crops out the art name and description of the art, saves to corresponding files
    image_name = "screenshot.png"
    img = Image.open(image_name)
    imgCroppedArt = img.crop(box = (x1, y1, x2, y2))
    imgCroppedDescription = img.crop(box = (x3, y3, x4, y4))
    imgCroppedArt.save("artName.png")
    imgCroppedDescription.save("artDescription.png")


def checkArtName():
    #check the name of the art
    pytesseract.pytesseract.tesseract_cmd = tesseractLocation
    artPulled = pytesseract.image_to_string(Image.open('artName.png')).strip()
    return artPulled


def checkArtDescription():
    #check if an art is descriptionless
    pytesseract.pytesseract.tesseract_cmd = tesseractLocation
    artDescription = pytesseract.image_to_string(Image.open('artDescription.png')).strip()
    return artDescription


def main():
    #artsPulledLog and artsPulledCounts to be used for tracking pulls if logging == "enabled"
    global artsPulledLog, artsPulledCounts, artName, desc

    #initialize values
    loadConfig()
    artsPulledLog = []
    artsPulledCounts = []

    #loop for pullLimit iterations
    #check art
    takeScreenshot()
    cropImage()
    artName = checkArtName()
    desc = checkArtDescription()
    print(f"art name: '{artName}'")
    print(f"description: '{desc}'")


if __name__ == '__main__':
    main()






