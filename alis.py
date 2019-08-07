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
cmd('arch-chroot /mnt echo ' + hos + ' > /etc/hostname')
loc = input('Enter your locale (e.g., "de_DE"): ')
cmd('arch-chroot /mnt sed -i "s/^#' + loc + '/' + loc + '/" /etc/locale.gen')
cmd('arch-chroot /mnt echo LANG=' + loc + '.UTF-8 > /etc/locale.conf')
cmd('arch-chroot /mnt echo KEYMAP=' + key + ' > /etc/vconsole.conf')
tim = input('Enter you time zone (e.g., "Europe/Berlin"): ')
cmd('arch-chroot /mnt ln -sf /usr/share/zoneinfo/' + tim + ' /etc/localtime')
cmd('arch-chroot /mnt sed -i "s/^ #%wheel ALL=(ALL) ALL/%wheel ALL=(ALL) ALL/" /etc/sudoers')
cmd('arch-chroot /mnt pacman -Syyu')
#localectl set-x11-keymap de pc105 nodeadkeys
cmd('arch-chroot /mnt locale-gen')
cmd('arch-chroot /mnt mkinitcpio -p linux')
cmd('arch-chroot /mnt echo "Enter the password for root!"')
cmd('arch-chroot /mnt passwd root')
rea = input('Enter your real name: ')
use = input('Enter your user name (ONLY ONE WORD AND LOWERCASE LETTERS): ')
cmd('arch-chroot /mnt useradd -m -g users -G wheel,audio,video,games,power -s /bin/bash -c "' + rea + '" ' + use)
cmd('arch-chroot /mnt echo "Enter the password for ' + use + '!"')
cmd('arch-chroot /mnt passwd ' + use)
cmd('arch-chroot /mnt systemctl enable acpid')
cmd('arch-chroot /mnt systemctl enable avahi-daemon')
cmd('arch-chroot /mnt systemctl enable org.cups.cupsd')
cmd('arch-chroot /mnt systemctl enable cronie')
cmd('arch-chroot /mnt systemctl enable gdm')
cmd('arch-chroot /mnt systemctl enable systemd-timesyncd')
#hwclock -w
fir = input('Enter your firmware type (UEFI or BIOS): ')
if fir == 'UEFI' or fir == 'uefi':
    cmd('arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ALIS')
elif fir == 'BIOS' or fir == 'bios':
    cmd('arch-chroot /mnt grub-install ' + dis)
cmd('arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg')
cmd('reboot')
