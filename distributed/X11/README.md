## Xorg setting

This folder contains settings files for Xorg.

The following files go in `/etc/X11/xorg.conf.d`:
- **20-modesetting.conf** This file turns on software cursor to prevent weird graphical errors on some systems
- **50-zap.conf** This enables the X11 ctrl-alt-backspace key combo to kill X11. This is only needed in development
- **90-monitor.conf** This disables power saving on the display to prevent it from going to sleep and not waking up

The following file go in ~/
- **.xinitrc** this file tells xorg to start openbox on init

