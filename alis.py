#!/usr/bin/env python3
from subprocess import *
def cmd(tmp):
    run(tmp, shell=True)
key = input('Enter your keyboard layout (e.g., "de-latin1"): ')
cmd('loadkeys ' + key)
dis = input('Enter your disk path (e.g., "/dev/sda"): ')
cmd('cfdisk ' + dis)
roo = input('Enter your / partition path (e.g., "/dev/sda1"): ')
cmd('mkfs.ext4 -L root ' + roo)
cmd('mount -L root /mnt')
hom = input('Enter your /home partition path (e.g., "/dev/sda2"): ')
if hom != '':
    cmd('mkfs.ext4 -L home ' + hom)
    cmd('mkdir /mnt/home')
    cmd('mount -L home /mnt/home')
else:
    pass
boo = input('Enter your /boot partition path (e.g., "/dev/sda3"): ')
if boo != '':
    cmd('mkfs.fat -F 32 -n boot ' + boo)
    cmd('mkdir /mnt/boot')
    cmd('mount -L boot /mnt/boot')
else:
    pass
swa = input('Enter you swap partition path (e.g., "/dev/sda4"): ')
if swa != '':
    cmd('mkswap -L swap ' + swa)
    cmd('swapon -L swap')
else:
    pass
net = input('Enter your network type (WIFI or LAN): ')
if net == 'WIFI' or net == 'wifi':
    cmd('wifi-menu')
else:
    pass
ran = input('Do you want to sort the mirrors? [Y/n] ')
if ran == '' or ran == 'Y' or ran == 'y':
    cmd('pacman -Syy pacman-contrib --noconfirm')
    cmd('cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak')
    cmd('echo "Sorting mirrors... (this could take a while)"')
    cmd('rankmirrors -n 6 /etc/pacman.d/mirrorlist.bak > /etc/pacman.d/mirrorlist')
    cmd('rm /etc/pacman.d/mirrorlist.bak')
else:
    pass
cmd('pacstrap /mnt base base-devel dialog wpa_supplicant linux-headers virtualbox-guest-utils intel-ucode amd-ucode bash-completion grub efibootmgr dosfstools gptfdisk acpid avahi cups cronie xorg-server xorg-xinit xorg-drivers ttf-dejavu noto-fonts-emoji gnome')
cmd('genfstab -Lp /mnt > /mnt/etc/fstab')
hos = input('Enter your host name: ')
cmd('echo ' + hos + ' > /mnt/etc/hostname')
loc = input('Enter your locale (e.g., "de_DE"): ')
cmd('sed -i "s/^#' + loc + '/' + loc + '/" /mnt/etc/locale.gen')
cmd('echo LANG=' + loc + '.UTF-8 > /mnt/etc/locale.conf')
cmd('echo KEYMAP=' + key + ' > /mnt/etc/vconsole.conf')
tim = '/mnt/usr/share/zoneinfo/' + input('Enter you time zone (e.g., "Europe/Berlin"): ')
cmd('ln -sf ' + tim + ' /mnt/etc/localtime')
cmd('sed -i "s/^ #%wheel ALL=(ALL) ALL/%wheel ALL=(ALL) ALL/" /mnt/etc/sudoers')
cmd('echo pacman -Syyu > /mnt/alis.sh')
#localectl set-x11-keymap de pc105 nodeadkeys
cmd('echo locale-gen >> /mnt/alis.sh')
cmd('echo mkinitcpio -p linux >> /mnt/alis.sh')
cmd('echo "echo Enter the password for root!" >> /mnt/alis.sh')
cmd('echo passwd root >> /mnt/alis.sh')
rea = input('Enter your real name: ')
use = input('Enter your user name (ONLY ONE WORD AND LOWERCASE LETTERS): ')
cmd('echo useradd -m -g users -G wheel,audio,video,games,power -s /bin/bash -c "' + rea + '" ' + use + ' >> /mnt/alis.sh')
#cmd('echo useradd -m -g users -G wheel,audio,video,games,power -s /bin/bash ' + use + ' >> /mnt/alis.sh')
cmd('echo "echo Enter the password for ' + use + '!" >> /mnt/alis.sh')
cmd('echo passwd ' + use + ' >> /mnt/alis.sh')
cmd('echo systemctl enable acpid >> /mnt/alis.sh')
cmd('echo systemctl enable avahi-daemon >> /mnt/alis.sh')
cmd('echo systemctl enable org.cups.cupsd >> /mnt/alis.sh')
cmd('echo systemctl enable cronie >> /mnt/alis.sh')
cmd('echo systemctl enable gdm >> /mnt/alis.sh')
cmd('echo systemctl enable systemd-timesyncd >> /mnt/alis.sh')
#hwclock -w
fir = input('Enter your firmware type (UEFI or BIOS): ')
if fir == 'UEFI' or fir == 'uefi':
    cmd('echo grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ALIS >> /mnt/alis.sh')
elif fir == 'BIOS' or fir == 'bios':
    cmd('echo grub-install ' + dis + ' >> /mnt/alis.sh')
cmd('echo grub-mkconfig -o /boot/grub/grub.cfg >> /mnt/alis.sh')
cmd('echo "echo First enter - exit - into the command prompt!" >> /mnt/alis.sh')
cmd('echo "echo Then enter - shutdown now - into the command prompt!" >> /mnt/alis.sh')
cmd('echo rm /alis.sh >> /mnt/alis.sh')
cmd('arch-chroot /mnt sh /alis.sh')
