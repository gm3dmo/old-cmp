#!/usr/bin/env python  
#- "-W ignore"

from __future__ import with_statement

from genshi.template import TemplateLoader
import zipfile
import MySQLdb
import os
import re
import time
import csv
import datetime
import ConfigParser
from datetime import date, datetime, time

    
def get_connection():
    config_file = 'cemgen.cfg'
    
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    db = config.get("database","db")
    dbhost = config.get("database","dbhost")
    dbport = config.getint("database","dbport")
    dbuser = config.get("database","dbuser")
    dbpass = config.get("database","dbpass")
    
    dbpass = config.get("database","dbpass")
    conn = MySQLdb.connect(host=dbhost, port=dbport, user=dbuser, passwd=dbpass, db=db)
    return conn

    
def get_all_things(conn, table):
    cursor = conn.cursor()
    sql = "SELECT id, name, NearestCity, Notes, WartimeCountry, PresentCountry_id, Latitude, Longitude from cmpm_powcamp where name != \"\" "
    cursor.execute(sql)
    list_of_things = cursor.fetchall()
    conn.close()
    return list_of_things
   
    
def main():


    conn = get_connection()

    with open('pow-camp.csv', 'w') as csvfile:

        fieldnames = [ "id", "Name", "NearestCity", "Notes", "WartimeCountry", "PresentCountry_id", "Latitude", "Longitude" ] 
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        things = get_all_things(conn, 'cmpm_powcamp')
        writer.writerows(things)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
