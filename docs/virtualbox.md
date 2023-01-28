# Virtual Machine Setup

  This document contains information on how to set up the Ubuntu virtual machine for the programming of the Arduino microcontroller

## Virtual Machine Creation

  Open VirtualBox and click on `New`. 
  
  Under `Name and Operating System`, name the VM and select the Ubuntu .iso image. Under `Unattended Install`, set your username and password. Under `Hardware`, select the amount of RAM and CPUs to give the VM. Under `Hard Disk`, select the amount of storage to give the VM.
  
  Click "Finish" to create and launch the VM. Upon booting, you can skip all of the setup options the OS presents.
  
## Setting up VM

  You'll need to give your user `sudo` and install the Guest Additions CD in order to hook up the required devices to the Virtual Machine. The steps to do this are listed below.
  
### Getting sudo Access
  
  Go to `Show Applications` from the left-sidebar and open terminal. Run the below commands to login to the root user and give your user sudo access:
  
  ```bash
  su -
  sudo adduser <username> sudo
  exit
  ```
  
  Provide the password you entered during the creation of the Virtual Machine when prompted. The Virtual Machine may need to be restarted for this permission change to take effect.

## Setting up Shared Folders/USB Ports  

  In order to have shared folders and USB inputs be accessible to the Virtual Machine, you will need to both install guest additions and configure the shared folders and USB devices. The steps for these are below.

### Adding Guest Additions

  Open the `Devices` tab from the top toolbar and select `Insert Guest Additions CD Image`.
  
  Open `Files` from the left-sidebar and open the CD directory. Right-click -> "Open in terminal" to open the CD directory in a terminal session. Run the command below command to install the Guest Additions to Ubuntu.
  
  ```bash
  ./autorun.sh
  ```
  
  Provide the password you entered during the creation of the Virtual Machine when prompted.
  
  After the script is finished running, you are free to eject the CD. Run the below command to give the user access to the shared folders once those are added.
  
  ```bash
  sudo adduser <username> vboxsf
  ```
  
  Provide the password you entered during the creation of the Virtual Machine when prompted. The Virtual Machine may need to be restarted for this permission change to take effect.

### Adding Shared Folders and USBs

  From the VirtualBox Manager, select your VM and click on `Settings`.
  
  Go to the `Shared Folders` section and click the add folder button (has a + symbol on it). Select the folder on your device you want to give the VM access to. For the purpose of this project, you will need to add both the folder for this repository and the folder for ascottile's switch-microcontroller repository. Check the `Auto-mount` box for each folder to be added.
  
  Go to the `USB` section and click the add USB device button (has a + symbol on it). Select the USB device you want to give the VM access to. For the purpose of this project, you will need to add the Arduino microcontroller while in programming mode. The microcontroller is treated as a separate device while in programming mode, so ensure you add it while in programming mode. Additionally, if you intend to run the script from the VM, also add the UART to USB converted.
