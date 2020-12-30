## Lightdm

lightdm is used to automatically log in to openbox on startup. A bit of setup is required to make lightdm work. 

- **install accountsservice** this is listed as an optional dependancy for lightdm but, it won't work for us without it
- **create user** the auto login user in the examples is named `mrt`. This user must belong to the autologin and nopasswdlogin groups which also must be created. Run the following as root:
`
# groupadd -r nopasswdlogin
# groupadd -r autologin
# useradd -mG autologin,nopasswdlogin -s /bin/bash mrt
`
- **update lightdm.conf** update `/etc/lightdm/lightdm.conf` with the following
`
autologin-usr=mrt
autologin-session=openbox
autologin-user-timeout=0
`

