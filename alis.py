#!/usr/bin/env python3
from subprocess import *
def cmd(tmp):
    run(tmp, shell=True)
key = input('Enter your keyboard layout (e.g., "de-latin1"): ')
if key == '':
    while key == '':
        key = input('Enter your keyboard layout (e.g., "de-latin1"): ')
else:
    pass
cmd('loadkeys ' + key)
dis = input('Enter your disk path (e.g., "/dev/sda"): ')
if dis == '':
    while dis == '':
        dis = input('Enter your disk path (e.g., "/dev/sda"): ')
else:
    pass
cmd('cfdisk ' + dis)
roo = input('Enter your / partition path (e.g., "/dev/sda1"): ')
if roo == '':
    while roo == '':
        roo = input('Enter your / partition path (e.g., "/dev/sda1"): ')
else:
    pass
hom = input('Enter your /home partition path (e.g., "/dev/sda2"): ')
boo = input('Enter your /boot partition path (e.g., "/dev/sda3"): ')
swa = input('Enter you swap partition path (e.g., "/dev/sda4"): ')
set = input('Do you want to setup WIFI? [Y/n] ')
if set == '' or set == 'Y' or set == 'y':
    cmd('wifi-menu')
else:
    pass
sor = input('Do you want to sort the mirrors? [Y/n] ')
hos = input('Enter your host name: ')
if hos == '':
    while hos == '':
        hos = input('Enter your host name: ')
else:
    pass
loc = input('Enter your locale (e.g., "de_DE"): ')
if loc == '':
    while loc == '':
        loc = input('Enter your locale (e.g., "de_DE"): ')
else:
    pass
tim = input('Enter you time zone (e.g., "Europe/Berlin"): ')
if tim == '':
    while tim == '':
        tim = input('Enter you time zone (e.g., "Europe/Berlin"): ')
else:
    pass
rea = input('Enter your real name: ')
if rea == '':
    while rea == '':
        rea = input('Enter your real name: ')
else:
    pass
use = input('Enter your user name (ONLY ONE WORD AND LOWERCASE LETTERS): ')
if use == '':
    while use == '':
        use = input('Enter your user name (ONLY ONE WORD AND LOWERCASE LETTERS): ')
else:
    pass
pas = input('Enter your password (INCLUDE LOWERCASE LETTERS, UPPERCASE LETTERS AND NUMBERS): ')
if pas == '':
    while pas == '':
        pas = input('Enter your password (INCLUDE LOWERCASE LETTERS, UPPERCASE LETTERS AND NUMBERS): ')
else:
    pass
fir = input('Enter your firmware type (UEFI or BIOS): ')
while fir != 'UEFI' and fir != 'uefi' and fir != 'BIOS' and fir != 'bios':
    fir = input('Enter your firmware type (UEFI or BIOS): ')
ins = input('Do you really want to start the installation? [y,N] ')
if ins != 'Y'and ins != 'y':
    exit()
else:
    pass
cmd('mkfs.ext4 -L root ' + roo)
cmd('mount -L root /mnt')
if hom != '':
    cmd('mkfs.ext4 -L home ' + hom)
    cmd('mkdir /mnt/home')
    cmd('mount -L home /mnt/home')
else:
    pass
if boo != '':
    cmd('mkfs.fat -F 32 -n boot ' + boo)
    cmd('mkdir /mnt/boot')
    cmd('mount -L boot /mnt/boot')
else:
    pass
if swa != '':
    cmd('mkswap -L swap ' + swa)
    cmd('swapon -L swap')
else:
    pass
if sor == '' or sor == 'Y' or sor == 'y':
    cmd('cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak')
    cmd('echo "Sorting mirrors... (this could take a while)"')
    cmd('rankmirrors -n 6 /etc/pacman.d/mirrorlist.bak > /etc/pacman.d/mirrorlist')
    cmd('rm /etc/pacman.d/mirrorlist.bak')
else:
    pass
cmd('pacstrap /mnt base base-devel dialog wpa_supplicant linux-headers virtualbox-guest-utils intel-ucode amd-ucode bash-completion grub os-prober efibootmgr dosfstools gptfdisk acpid cronie avahi cups networkmanager xorg-server xorg-xinit xorg-drivers ttf-dejavu noto-fonts-emoji gnome')
cmd('genfstab -Lp /mnt > /mnt/etc/fstab')
cmd('arch-chroot /mnt echo ' + hos + ' > /etc/hostname')
cmd('arch-chroot /mnt echo KEYMAP=' + key + ' > /etc/vconsole.conf')
cmd('arch-chroot /mnt echo LANG=' + loc + '.UTF-8 > /etc/locale.conf')
cmd('arch-chroot /mnt sed -i "s/^#' + loc + '/' + loc + '/" /etc/locale.gen')
cmd('arch-chroot /mnt locale-gen')
cmd('arch-chroot /mnt ln -sf /usr/share/zoneinfo/' + tim + ' /etc/localtime')
cmd('arch-chroot /mnt sed -i "s/^ #%wheel ALL=(ALL) ALL/%wheel ALL=(ALL) ALL/" /etc/sudoers')
cmd('arch-chroot /mnt useradd -m -g users -G wheel,audio,video,games,power -s /bin/bash -p ' + pas + ' -c "' + rea + '" ' + use)
cmd('arch-chroot /mnt yes ' + pas + ' | passwd ' + use)
cmd('arch-chroot /mnt passwd -d root')
cmd('arch-chroot /mnt systemctl enable acpid')
cmd('arch-chroot /mnt systemctl enable cronie')
cmd('arch-chroot /mnt systemctl enable avahi-daemon')
cmd('arch-chroot /mnt systemctl enable org.cups.cupsd')
cmd('arch-chroot /mnt systemctl enable systemd-timesyncd')
cmd('arch-chroot /mnt systemctl enable NetworkManager')
cmd('arch-chroot /mnt systemctl enable bluetooth')
cmd('arch-chroot /mnt systemctl enable gdm')
if fir == 'UEFI' or fir == 'uefi':
    cmd('arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ALIS')
elif fir == 'BIOS' or fir == 'bios':
    cmd('arch-chroot /mnt grub-install ' + dis)
else:
    pass
cmd('arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg')
cmd('reboot')
