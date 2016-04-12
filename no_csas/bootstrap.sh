#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y git build-essential wget
sudo apt-get remove -y php5
sudo apt-get install -y apache2 apache2-dev
sudo apt-get install -y graphviz
sudo apt-get install valgrind
sudo apt-get install unzip
sudo apt-get install -y \
    libxml2-dev \
    libcurl4-openssl-dev \
    libjpeg-dev \
    libpng-dev \
    libxpm-dev \
    libmysqlclient-dev \
    libpq-dev \
    libicu-dev \
    libfreetype6-dev \
    libldap2-dev \
    libxslt-dev \
    autoconf
/usr/bin/wget -nv http://php.net/get/php-5.4.45.tar.gz/from/this/mirror -O php-5.4.45.tar.gz
tar -xzvf php-5.4.45.tar.gz
cd php-5.4.45
export PHPDIR=`pwd`
/bin/echo "export PHPDIR=`pwd`"  | sudo /usr/bin/tee --append /home/vagrant/.bashrc
/bin/echo 'export PATH=$PATH:$PHPDIR/php-install-directory/bin/'  | sudo /usr/bin/tee --append /home/vagrant/.bashrc
/bin/echo "alias build-php='cd $PHPDIR;$PHPDIR/configure --enable-debug --enable-maintainer-zts --prefix=$PHPDIR/php-install-directory --with-apxs2=/usr/bin/apxs'"  | sudo /usr/bin/tee --append /home/vagrant/.bashrc
$PHPDIR/configure --enable-debug \
    --enable-maintainer-zts \
    --prefix=$PHPDIR/php-install-directory \
    --with-mysqli \
    --with-openssl \
    --with-mysql-sock=/var/run/mysqld/mysqld.sock \
    --with-apxs2=/usr/bin/apxs
/usr/bin/make
sudo /usr/bin/make install
sudo mv $PHPDIR/php.ini-development $PHPDIR/php-install-directory/lib/php.ini
/bin/echo "AddType application/x-httpd-php  .php"  | sudo /usr/bin/tee --append /etc/apache2/apache2.conf
export PATH=$PATH:$PHPDIR'/php-install-directory/bin/'

#set php ini locatation
sudo $PHPDIR/php-install-directory/bin/pecl config-set php_ini $PHPDIR/php-install-directory/lib/php.ini
#install xdebug profiler
sudo $PHPDIR/php-install-directory/bin/pecl install xdebug

#install other directories
git clone https://github.com/php-csas/php-csas.git ~/php-csas

#create profiler output directory
cd ~/php-csas && sh ~/php-csas/build_extension.sh
#modify the php.ini file
sudo /bin/sed -i "1828i extension=csas.so"  $PHPDIR/php-install-directory/lib/php.ini
sudo /bin/sed -i "1830i csas.enable = 0"  $PHPDIR/php-install-directory/lib/php.ini
#add profiler extension
echo 'zend_extension = "/home/vagrant/php-5.4.45/php-install-directory/lib/php/extensions/debug-zts-20100525/xdebug.so"' >> $PHPDIR/php-install-directory/lib/php.ini
echo 'xdebug.profiler_enable = 1' >> $PHPDIR/php-install-directory/lib/php.ini
echo 'xdebug.profiler_output_dir = "/home/vagrant/xdebug"' >> $PHPDIR/php-install-directory/lib/php.ini
echo 'xdebug.profiler_output_name = cachegrind.out.%t.%p' >> $PHPDIR/php-install-directory/lib/php.ini

cd ~
mkdir prof_out
sudo chmod 777 prof_out
mkdir xdebug
sudo chmod 777 xdebug

#create link between lib/php and var/www/xhprof

#clone the demonstration
sudo rm -rf /var/www/html
sudo git clone https://github.com/php-csas/demo-site /var/www/html

git clone https://github.com/perftools/xhgui.git /var/www
sudo $PHPDIR/php-install-directory/bin/php /var/www/xhgui/install.php

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password csas'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password csas'

#install webgrind
sudo /usr/bin/wget https://github.com/michaelschiller/webgrind/archive/master.zip
sudo unzip master.zip -d /var/www/html
sudo mv /var/www/html/webgrind-master /var/www/html/webgrind
sudo rm /home/vagrant/master.zip
sudo /bin/sed -i "s|storageDir = ''|storageDir = '/home/vagrant/prof_out'|" /var/www/html/webgrind/config.php

#install sql
sudo apt-get -y install mysql-server libapache2-mod-auth-mysql php5-mysql
sudo mysql_install_db

MYSQL=`which mysql`

Q1="CREATE DATABASE IF NOT EXISTS csas;"
Q2="GRANT ALL ON *.* TO 'root'@'localhost' IDENTIFIED BY 'csas';"
Q3="FLUSH PRIVILEGES;"
Q4="USE csas;"
Q5="CREATE TABLE post (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, text VARCHAR(1000), link VARCHAR(500), name VARCHAR(500), date TIMESTAMP);"
SQL="${Q1}${Q2}${Q3}${Q4}${Q5}"

$MYSQL -uroot -pcsas -e "$SQL"
sudo service apache2 restart
