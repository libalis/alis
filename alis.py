#!/usr/bin/env python3
from subprocess import *
def cmd(tmp):
    run(tmp, shell=True)
key = input('Enter your keyboard layout (e.g., "de-latin1"): ')
cmd('loadkeys ' + key)
dis = input('Enter your disk path (e.g., "/dev/sda"): ')
cmd('cfdisk ' + dis)
cmd('mkfs.ext4 -L root ' + input('Enter your / partition path (e.g., "/dev/sda1"): '))
cmd('mkfs.fat -F 32 -n boot ' + input('Enter your /boot partition path (e.g., "/dev/sda2"): '))
cmd('mkswap -L swap ' + input('Enter you swap partition path (e.g., "/dev/sda3"): '))
cmd('mount -L root /mnt')
cmd('mkdir /mnt/boot')
cmd('mount -L boot /mnt/boot')
cmd('swapon -L swap')
net = input('Enter your network type (WIFI or LAN): ')
if net == 'WIFI' or net == 'wifi':
    cmd('wifi-menu')
else:
    pass
cmd('pacman -Syy pacman-contrib')
cmd('cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak')
cmd('rankmirrors -n 6 /etc/pacman.d/mirrorlist.bak > /etc/pacman.d/mirrorlist')
cmd('rm /etc/pacman.d/mirrorlist.bak')
cmd('pacstrap /mnt base base-devel dialog wpa_supplicant linux-headers virtualbox-guest-utils intel-ucode amd-ucode bash-completion grub efibootmgr dosfstools gptfdisk acpid avahi cups cronie xorg-server xorg-xinit xorg-drivers ttf-dejavu noto-fonts-emoji gnome')
cmd('genfstab -Lp /mnt > /mnt/etc/fstab')
cmd('echo ' + input('Enter your host name: ') + ' > /mnt/etc/hostname')
loc = input('Enter your locale (e.g., "de_DE"): ')
cmd('sed -i "s/^#' + loc + '/' + loc + '/" /mnt/etc/locale.gen')
cmd('echo LANG=' + loc + '.UTF-8 > /mnt/etc/locale.conf')
cmd("echo KEYMAP=' + key + ' > /mnt/etc/vconsole.conf")
cmd('ln -sf /usr/share/zoneinfo/' + input('Enter you time zone (e.g., "Europe/Berlin"): ') + ' /mnt/etc/localtime')
cmd('sed -i "s/^ #%wheel ALL=(ALL) ALL/%wheel ALL=(ALL) ALL/" /mnt/etc/sudoers')
#multilib
cmd('echo pacman -Syyu >> /mnt/setup.sh')
#localectl set-x11-keymap de pc105 nodeadkeys
cmd('echo locale-gen >> /mnt/setup.sh')
cmd('echo mkinitcpio -p linux >> /mnt/setup.sh')
cmd("echo Enter root's password: >> /mnt/setup.sh")
cmd('echo passwd root >> /mnt/setup.sh')
use = input('Enter your user name (ONLY ONE WORD AND LOWERCASE LETTERS): ')
cmd('echo useradd -m -g users -G wheel,audio,video,games,power -s /bin/bash -c "' + input('Enter your real name: ') + '" ' + use + ' >> /mnt/setup.sh')
cmd("echo Enter " + use + "'s password: >> /mnt/setup.sh")
cmd('echo passwd ' + use + ' >> /mnt/setup.sh')
cmd('echo systemctl enable acpid >> /mnt/setup.sh')
cmd('echo systemctl enable avahi-daemon >> /mnt/setup.sh')
cmd('echo systemctl enable org.cups.cupsd >> /mnt/setup.sh')
cmd('echo systemctl enable cronie >> /mnt/setup.sh')
cmd('echo systemctl enable gdm >> /mnt/setup.sh')
cmd('echo systemctl enable systemd-timesyncd >> /mnt/setup.sh')
#hwclock -w
fir = input('Enter your firmware type (UEFI or BIOS): ')
if fir == 'UEFI' or fir == 'uefi':
    cmd('echo grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ALIS >> /mnt/setup.sh')
elif fir == 'BIOS' or fir == 'bios':
    cmd('echo grub-install ' + dis + ' >> /mnt/setup.sh')
cmd('echo grub-mkconfig -o /boot/grub/grub.cfg >> /mnt/setup.sh')
cmd('echo First enter "exit" into the command prompt! >> /mnt/setup.sh')
cmd('echo Then enter "shutdown now" into the command prompt! >> /mnt/setup.sh')
cmd('echo rm /setup.sh >> /mnt/setup.sh')
cmd('echo Enter "sh setup.sh" into the command prompt!')
cmd('arch-chroot /mnt')
