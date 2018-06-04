import csv
import sys
import os
from alert import *

def main():
    alert1 = Alert('1','2000-03-07 06:51:36','172.16.115.1','202.77.162.213','Ya','8','Tidak menggunakan TCP','Tidak menggunakan TCP','Tidak menggunakan UDP','Tidak menggunakan UDP','ICMP PING','misc-activity')
    alert2 = Alert('2','2000-03-07 06:51:36','202.77.162.213','172.16.115.1','Ya','0','Tidak menggunakan TCP','Tidak menggunakan TCP','Tidak menggunakan UDP','Tidak menggunakan UDP','ICMP Echo Reply','misc-activity')
    print 'Alert 1 Content : \n'
    print alert1.sig_class_name
    print '\n\n'
    print 'Alert 2 Content : \n'
    print alert2.sig_class_name


if __name__ == '__main__':
    main()

# Data :
# '1','2000-03-07 06:51:36','172.16.115.1','202.77.162.213','Ya','8','Tidak menggunakan TCP','Tidak menggunakan TCP','Tidak menggunakan UDP','Tidak menggunakan UDP','ICMP PING','misc-activity'
# '2','2000-03-07 06:51:36','202.77.162.213','172.16.115.1','Ya','0','Tidak menggunakan TCP','Tidak menggunakan TCP','Tidak menggunakan UDP','Tidak menggunakan UDP','ICMP Echo Reply','misc-activity'