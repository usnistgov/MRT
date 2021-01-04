## PKGBUILDS

PKGBUILD files are used by the arch linux `makepkg` command to build a package. They are provided here to install a few needed components that aren't in the standard repositories. Once they are built, they can be installed with `pacman -U` or using `makepkg -i`


- **python-ptcommon-git** has python libraries to talk to the pytop hub. Most importantly it has systemd units to tell the pitop to power down when the pi is shutdown. Once this is installed it must be enabled using `systemctl enable pt-poweroff-v2`
