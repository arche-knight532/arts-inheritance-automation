# arts-inheritance-automation
 A project to automate the process of pulling arts from Arts Gacha for the Arts Inheritance glitch in XC:DE.
 
 This project will be updated over time with new features and quality of life improvements. This is currently a personal project and will not be accepting assistance from other collaborators. If you have any feedback or questions, please feel free to reach out to me over Discord. I can be easily found in the [Xeno Speedrun Discord server](https://discord.gg/RTVDKhp).

## Prerequisites (Hardware/Software)
 Below are the required hardware to run this project and control the Nintendo Switch. Combined these components come to ~$25:
  - Arduino Microcontroller: [Pre-pinned](https://www.cytron.io/p-arduino-pro-micro-compatible-pre-soldered-headers) or [non-pre-pinned](https://amzn.to/3rpb36r) versions of the microcontroller I used. 
    - If you purchase the non-pre-pinned version, you will have to solder the pins on yourself. If you do not have access to a soldering iron, I recommend the pre-pinned version. I personally purchased the non-pre-pinned one so I cannot speak to the quality of the pre-pinned version linked above.
  - [UART to USB converter](https://www.amazon.com/IZOKEE-CP2102-Converter-Adapter-Downloader/dp/B07D6LLX19/ref=sr_1_4?keywords=usb+to+uart&qid=1674486848&sr=8-4)
    - You may need to manually install the driver, which can be found [here](https://www.usb-drivers.org/cp2102-usb-to-uart-bridge-driver.html)
  - [USB-A to Micro USB-B cable](https://www.amazon.com/AmazonBasics-Male-Micro-Cable-Black/dp/B07232M876?th=1)
    - Can probably be gotten for cheaper at Walmart or similar stores
  - Depending on how you want to hook it up, a breadboard and some short wires
 
 Below are the required software to run this project:
  - [Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)
  - [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
  - [Python 3](https://www.python.org/downloads/) (any version of python 3 will work, I used 3.11.1)
  - [Ubuntu iso](https://ubuntu.com/#download) (I used the LTS version, but any recent release should work)
  - [Git CLI](https://git-scm.com/downloads) (not required but recommended for ease of cloning repositories)

## How to Use
 This section will explain how to setup and run this script.

### Installation
 Clone this repository to your personal machine. Additionally, clone [ascottile's switch-microcontroller repo](https://github.com/asottile/switch-microcontroller). Finally, clone the [lufa repository](https://github.com/abcminiuser/lufa/tree/597fbf47cd2551423a231ac747e2f1405cf9306a) over the lufa directory of the switch-microcontroller repository.
 
 Use `pip` to install the below Python libraries:
  - pytesseract
  - pyscreenshot
  - pyserial
 
 Setup your Ubuntu virtual machine. If you use a Linux operating system, this step can be skipped. Documentation for how to do this can be found [here](docs/virtualbox.md).
 
 A [guide by anthonywritescode](https://youtu.be/chvgQUX7QaI) explains the process of programming the Arduino to act as a controller. I plan to make my own guide at some point, but for now his works well and was how I set up my own. It is worth mentioning that the Arduino is a different device while in programming mode, so this version of the device will need to be passed into the Virtal Machine to be programmable.

### Configuration
 Take a screenshot of your screen and open it in a program such as Paint which lets you see the pixel positions of the image. Find the X/Y positions of the art name and description on your screen and make note of them
 
 Open the [config.ini](scripts/config.ini) file with your text editor of choice and modify the following fields with these values:
  - x1/y1: the top-left corner of the art name screenshot
  - x2/y2: the bottom-right corner of the art name screenshot
  - x3/y3: the top-left corner of the art description screenshot
  - x4/y4: the bottom-right corner of the art description screenshot
  - arts: the list of arts that you want to pull; the program will stop execution if one of these arts is found; capitalization matters
    - it is recommended to use the output from [test_run.py](scripts/test_run.py) to verify the art name will be what you expect, as sometimes the Tesseract library can slightly misread art names; if an art name is not an exact match, the program will not stop upon pulling it
  - description: y/n flag for each art you want for whether you want it to have a description or not
    - ex: Sword Drive + y = descriptionless Sword Drive/p.Sword Drive
  - pullLimit: the maximum number of art pulls before the program stops execution; the program currently runs at a rate of ~1250 art pulls per hour
  - logging: set to `enable` if you would like a file containing the list of all arts pulled and their counts
  - tesseractLocation: the path to Tesseract on your local machine
  - port: device port of your UART to USB converter

At some point I intend to add a script to automate this process for the user. When this is done, this documentation will be updated.

### Program Execution
  Have the menu open with the cursor over "Arts" before beginning program execution. Then, simply run the below command from the [scripts](scripts) directory. This script can be run from either your main OS or from the Virtual Machine.
  
  ```bash
python arts_inheritance_automation.py
```

  This program will use the main monitor of your computer and your Switch for as long as it takes to execute. If one of the requested arts is found, the program will return to the arts list (rather than the art level list) and end execution. If the art is not found, the program will end by closing out of the arts menu.

  If you need to input individual button presses for menu navigation without switching controllers, you can use the `press.py` script. Syntax for using the script can be found below. Additionally, the characters and their corresponding button inputs can be found below or in [ascottile's readme](https://github.com/asottile/switch-microcontroller).

  ```
  python press.py <char>
  ```

  ```
0: empty state (no buttons pressed)
A: A is pressed
B: B is pressed
X: X is pressed
Y: Y is pressed
H: Home is pressed
+: + is pressed
-: - is pressed
L: left trigger is pressed
R: right trigger is pressed
l: ZL is pressed
r: ZR is pressed

directions:
 LEFT STICK            RIGHT STICK

      w                     u
   q     e               y     i
      ║                     ║
a ══╬═══  d         h  ═══╬═══  k
      ║                     ║
   z     c               n     m
      s                     j
```
