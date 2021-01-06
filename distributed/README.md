## Distributed MRT configuration files

These files are used to configure a Linux machine to do distributed MRT tests. They may not all be needed if a non dedicated MRT setup is used.  Testing was done on a pi 3 inside a pi-top 3, most of the files here are widely applicable to any Linux system or not needed. For the setup Arch Linux was used.

The files are organized into folders as follows:

- **PKGBUILDs** files to create packages that are not in the usual repositories.
- **X11** config files for the xorg server to setup a couple of things for the graphical interface
- **command-line** config files to make the command line more pleseant to use. Not needed in the final system but, is nice during setup
- **lightdm** Instructions on how to setup lightdm to automatically run openbox on boot
- **openbox** config files for openbox to run the MRT gui on startup and make it fullscreen 
- **pi-boot** config files to setup the Raspberry Pi hardware to work with the display sound and other things.
