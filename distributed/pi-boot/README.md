## Boot configuration for raspberry pi 3

These are boot configuration files for the raspberry pi 3. They are as follows:
- **cmdline.txt** linux kernel command line options. Place in `/boot/`
- **config.txt** boot configuration file. Place in `/boot/`
- **i2c.conf** kernel modules to load on boot for I2C. Place in `/etc/modules-load.d/`
- **snd-blacklist.conf** blakclist kernel modules for onboard soundcard. This makes a USB soundcard default. Place in `/etc/modprobe.d/`
- **fstab** This will mount the data partition so it can be read and written by users of the `mrt-data` group. This requires that a 3rd partition be added to the SD card when the OS is installed

