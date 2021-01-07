## Openbox Files
These files configure the openbox window manager. They should be located in `~/.config/openbox/` 
- **autostart** file needed to run the MRT test when openbox starts
- **menu.xml** menu, not so useful for MRT testing but, removes a lot of things that aren't needed
- **rc.xml** main configuration for openbox, configures all tk application windows to be full screen. This is used to ensure the MRT GUI is full screen. Also included are some keybindings for volume keys. This assumes that the sound device used is the Sound Blaster x-Fi HD USB. If you are using a diffrent card, use `aplay -l` to list the available sound cards and find the name of the one you want to use. Below is some example output of `aplay -l` with the Sound Blaster x-Fi HD USB:
```
$ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: vc4hdmi [vc4-hdmi], device 0: MAI PCM vc4-hdmi-hifi-0 [MAI PCM vc4-hdmi-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 1: HD [USB Sound Blaster HD], device 0: USB Audio [USB Audio]
  Subdevices: 0/1
  Subdevice #0: subdevice #0
card 1: HD [USB Sound Blaster HD], device 1: USB Audio [USB Audio #1]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 1: HD [USB Sound Blaster HD], device 2: USB Audio [USB Audio #2]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```
Based on this output, the name of the card we want to use is "HD". The keybinding for `XF86AudioLowerVolume` and `XF86AudioRaiseVolume` pass `-c HD` to `amixer` to select this card. If your card has a diffrent name replace HD with it.
