# 制作文件系统镜像

sudo mkdir ubuntu-rootfs

sudo tar -xvpf ubuntu-base-18.04.5-base-arm64.tar.gz -C ubuntu-rootfs

sudo apt-get install qemu-user-static

sudo cp /usr/bin/qemu-arm-static ubuntu-rootfs/usr/bin/

sudo cp /usr/bin/qemu-aarch64-static ubuntu-rootfs/usr/bin/

sudo cp -b /etc/resolv.conf ubuntu-rootfs/etc/resolv.conf

## 修改镜像源

sudo gedit ubuntu-rootfs/etc/apt/sources.list

```bash
# See http://help.ubuntu.com/community/UpgradeNotes for how to upgrade to
# newer versions of the distribution.
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic main restricted
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic main restricted

## Major bug fix updates produced after the final release of the
## distribution.
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-updates main restricted
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-updates main restricted

## N.B. software from this repository is ENTIRELY UNSUPPORTED by the Ubuntu
## team. Also, please note that software in universe WILL NOT receive any
## review or updates from the Ubuntu security team.
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic universe
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic universe
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-updates universe
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-updates universe

## N.B. software from this repository is ENTIRELY UNSUPPORTED by the Ubuntu
## team, and may not be under a free licence. Please satisfy yourself as to
## your rights to use the software. Also, please note that software in
## multiverse WILL NOT receive any review or updates from the Ubuntu
## security team.
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic multiverse
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-updates multiverse
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-updates multiverse

## N.B. software from this repository may not have been tested as
## extensively as that contained in the main release, although it includes
## newer versions of some applications which may provide useful features.
## Also, please note that software in backports WILL NOT receive any review
## or updates from the Ubuntu security team.
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-backports main restricted universe multiverse
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-backports main restricted universe multiverse

## Uncomment the following two lines to add software from Canonical's
## 'partner' repository.
## This software is not part of Ubuntu, but is offered by Canonical and the
## respective vendors as a service to Ubuntu users.
# deb http://archive.canonical.com/ubuntu bionic partner
# deb-src http://archive.canonical.com/ubuntu bionic partner

deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-security main restricted
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-security main restricted
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-security universe
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-security universe
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-security multiverse
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-security multiverse
```

## 添加制作镜像脚本

vi mount.sh #挂载镜像脚本

```bash
#!/bin/bash
# Mount function
function mnt() {
  echo "MOUNTING"
  
  # Check if /proc is already mounted
  if ! mount | grep -q "on ${2}proc "; then
    sudo mount -t proc /proc ${2}proc
  else
    echo "/proc already mounted"
  fi

  # Check if /sys is already mounted
  if ! mount | grep -q "on ${2}sys "; then
    sudo mount -t sysfs /sys ${2}sys
  else
    echo "/sys already mounted"
  fi

  # Check if /dev is already mounted
  if ! mount | grep -q "on ${2}dev "; then
    sudo mount -o bind /dev ${2}dev
  else
    echo "/dev already mounted"
  fi

  # Check if /dev/pts is already mounted
  if ! mount | grep -q "on ${2}dev/pts "; then
    sudo mount -o bind /dev/pts ${2}dev/pts
  else
    echo "/dev/pts already mounted"
  fi

  # Enter chroot environment
  sudo chroot ${2}
}

# Unmount function
function umnt() {
  echo "UNMOUNTING"
  
  # Ensure the full paths are correctly formed
  sudo umount ${2}proc
  sudo umount ${2}sys
  sudo umount ${2}dev/pts
  sudo umount ${2}dev
}

# Main script logic
if [ "$1" == "-m" ] && [ -n "$2" ]; then
  mnt $1 $2
elif [ "$1" == "-u" ] && [ -n "$2" ]; then
  umnt $1 $2
else
  echo ""
  echo "Either 1st, 2nd or both parameters were missing"
  echo ""
  echo "1st parameter can be one of these: -m (mount) OR -u (umount)"
  echo "2nd parameter is the full path of rootfs directory (with trailing '/')"
  echo ""
  echo "For example: ./mount.sh -m /media/sdcard/"
  echo ""
  echo "1st parameter: ${1}"
  echo "2nd parameter: ${2}"
fi
```

## 挂载镜像到指定脚本

./mount.sh -m ubuntu-rootfs/

## 进入镜像系统

apt update

apt upgrade

## 安装相关库

apt install pciutils安装lspci
安装insmod module-init-tools

安装apt install dialog vim sudo bash-completion net-tools iputils-ping ifupdown ssh udev pciutils module-init-tools
apt install cmake resolvconf

apt install locales tzdata

## 时区选择

```bash

Asia/Shanghai
dpkg-reconfigure locales
```

## 勾选英文和中文环境

```bash
en_US.UTF-8 UTF-8
```

## 主机名

echo "rk3568" > /etc/hostname

## 主机IP地址

echo "127.0.0.1 localhost rk3568" > /etc/hosts

## 添加用户

```bash
useradd -s '/bin/bash' -m -G adm,sudo user 
添加新用户命令，-s 指定用户默认登陆shell为/bin/bash;
-m 自动创建用户的主目录/home/username 
-G adm,sudo 将用户添加到adm和sudo两个用户组中;
(adm用于监控和查看日志权限,sudo赋予用户使用sudo命令的权限)
user 新用户的名称;

usermod -aG adm,sudo ym
-a 追加模式，将用户添加到新的组，同时保留用户当前的附加组
-G adm,sudo 指定用户加入的附加组
ym 用户名
备注:如需创建home下文件夹还可以加入-m
```

## 设置密码

```bash
passwd user
passwd root
```
<!-- 无法ping通网络 -->

## 固定IP(如果安装别的网络管理工具可以使用别的方法来固定)

vi /etc/network/interfaces

```bash

# interfaces(5) file used by ifup(8) and ifdown(8)
# Include files from /etc/network/interfaces.d:
<!-- source-directory /etc/network/interfaces.d -->

auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4
auto eth1
iface eth1 inet static
    address 192.168.1.101
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4
```
<!-- export PATH=/home/tronlong/rk3568/rk3/rk356x_linux_release_v1.3.1_20221120/buildroot/output/rockchip_rk3568/host/bin:$PATH -->

## 修改DNS

```bash
vi /etc/resolvconf/resolv.conf.d/base

nameserver 8.8.8.8
nameserver 223.5.5.5
nameserver 114.114.114.114
```

## 挂载点设置

修改vi etc/fstab

```bash
<file system> <mount point>   <type>  <options>       <dump> <pass>

/dev/mmcblk0p6   /               ext4    defaults        0       1
/dev/mmcblk0p9   /home           ext4    defaults        0       2
```

## 系统首次启动脚本

vi etc/init.d/firstboot.sh

```bash
#!/bin/bash
# Resize root and home filesystems on first boot

LOGFILE="/var/log/firstboot.log"

echo "Starting first boot script..." > $LOGFILE

# 调整根文件系统大小
echo "Resizing root filesystem (/dev/mmcblk0p6)..." >> $LOGFILE
resize2fs /dev/mmcblk0p6 >> $LOGFILE 2>&1
if [ $? -eq 0 ]; then
    echo "Root filesystem resized successfully." >> $LOGFILE
else
    echo "Error resizing root filesystem." >> $LOGFILE
fi

# 调整 home 文件系统大小
echo "Resizing home filesystem (/dev/mmcblk0p9)..." >> $LOGFILE
resize2fs /dev/mmcblk0p9 >> $LOGFILE 2>&1
if [ $? -eq 0 ]; then
    echo "Home filesystem resized successfully." >> $LOGFILE
else
    echo "Error resizing home filesystem." >> $LOGFILE
fi

# 移除脚本自身，防止再次运行
echo "Cleaning up firstboot script..." >> $LOGFILE
rm /home/200frames_count.h264
rm /home/belle-nuit-testchart-1080p.png
rm /home/piano2-CoolEdit.mp3
rm -r /home/lost+found
mkdir /home/user
chown user:user /home/user
rm -f /etc/init.d/firstboot.sh
update-rc.d -f firstboot.sh remove

echo "First boot script completed." >> $LOGFILE
exit 0
```

chmod +x /etc/init.d/firstboot.sh

## 添加系统启动服务

vi lib/systemd/system/firstboot.service

```bash
[Unit]
Description=Setup rockchip platform environment

[Service]
Type=simple
ExecStart=/etc/init.d/firstboot.sh

[Install]
WantedBy=multi-user.target
```

systemctl enable firstboot.service

<!-- update-rc.d firstboot.sh defaults  设置开机自启 -->

vi /etc/ssh/sshd_config #打开ssh连接

```bash
PermitRootLogin yes
PasswordAuthentication yes
```

vi /lib/systemd/system/serial-getty\@.service #打开串口调试

```bash
ExecStart=-/sbin/agetty --autologin root --noclear %I $TERM
```

exit

## 卸载镜像

./mount.sh -u ubuntu-rootfs

## 编写mkimage.sh(镜像打包脚本)

vi mkimage.sh

```bash
#!/bin/bash
rootfs_dir=$1
rootfs_file=$2
rootfs_mnt="mnt"

if [ ! $rootfs_dir ] || [ ! $rootfs_file ]; then
  echo "Folder or target is empty."
  exit 0
fi

if [ -f "$rootfs_file" ]; then
  echo "-- Delete existing $rootfs_file ..."
  rm -f "$rootfs_file"
fi

# Calculate rootfs size and add 20% extra space
rootfs_size=$(sudo du -sm "$rootfs_dir" | cut -f1)
extra_space=$(echo "$rootfs_size * 0.2" | bc)
total_size=$(echo "$rootfs_size + $extra_space" | bc)
total_size=${total_size%.*}

echo "-- Create $rootfs_file with size ${total_size} MB..."
dd if=/dev/zero of="$rootfs_file" bs=1M count=$total_size
sudo mkfs.ext4 -F -L linuxroot "$rootfs_file"

if [ ! -d "$rootfs_mnt" ]; then
  mkdir $rootfs_mnt
fi

echo "-- Copy data to $rootfs_file ..."
sudo mount $rootfs_file $rootfs_mnt

# Use rsync to avoid copying /proc, /sys, and /dev
sudo rsync -a --exclude=/proc --exclude=/sys --exclude=/dev $rootfs_dir/ $rootfs_mnt

sudo sync
sudo umount $rootfs_mnt
rm -r $rootfs_mnt

echo "-- Resize $rootfs_file ..."
/sbin/e2fsck -p -f "$rootfs_file"
/sbin/resize2fs -M "$rootfs_file"

echo "-- Done."
```

## 打包镜像

./mkimage.sh ubuntu-rootfs rootfs.img

cp rootfs.img ../ubuntumy/mkimage/output/Image/

systemctl status firstboot.service进入可以查看启动服务是否正常运行
