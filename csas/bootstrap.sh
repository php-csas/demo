#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y git build-essential wget
sudo apt-get remove -y php5
sudo apt-get install -y apache2 apache2-dev
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
    --with-mysql-sock=/var/run/mysqld/mysqld.sock \
    --with-apxs2=/usr/bin/apxs
/usr/bin/make
sudo /usr/bin/make install
sudo mv $PHPDIR/php.ini-development $PHPDIR/php-install-directory/lib/php.ini 
/bin/echo "AddType application/x-httpd-php  .php"  | sudo /usr/bin/tee --append /etc/apache2/apache2.conf
export PATH=$PATH:$PHPDIR'/php-install-directory/bin/'

git clone https://github.com/php-csas/php-csas.git ~/php-csas
git clone https://github.com/php-csas/taint.git ~/taint
git clone https://github.com/php-csas/ctemplate.git ~/ctemplate
git clone https://github.com/php-csas/php-travis-ci-tests-example.git ~/php-travis-ci-tests-example

cd ~/php-csas && sh ~/php-csas/build_extension.sh

sudo /bin/sed -i "1828i extension=csas.so"  $PHPDIR/php-install-directory/lib/php.ini
sudo /bin/sed -i "1830i csas.enable = 1"  $PHPDIR/php-install-directory/lib/php.ini

sudo rm -rf /var/www/html
sudo git clone https://github.com/php-csas/php-csas-demonstration /var/www/html

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password csas'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password csas'

sudo apt-get -y install mysql-server libapache2-mod-auth-mysql php5-mysql
sudo mysql_install_db

MYSQL=`which mysql`

Q1="CREATE DATABASE IF NOT EXISTS csas;"
Q2="GRANT ALL ON *.* TO 'root'@'localhost' IDENTIFIED BY 'csas';"
Q3="FLUSH PRIVILEGES;"
Q4="USE csas;"
Q5="CREATE TABLE post (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, text VARCHAR(1000), link VARCHAR(500), date TIMESTAMP);"
SQL="${Q1}${Q2}${Q3}${Q4}${Q5}"

$MYSQL -uroot -pcsas -e "$SQL"
