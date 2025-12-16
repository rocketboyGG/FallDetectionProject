#!/bin/bash
#Restart og opdateringsscript til backup server. Scriptet gør at maskinen
#genstarter hver 12 time og opdaterer alle packages.

#Logfil
LOGFILE="/var/log/restart_opdatering.log"

{
    echo "Kører system opdateringer..."
    apt update -y
    apt upgrade -y
    apt full-upgrade -y
    apt autoremove -y
    apt autoclean -y

    echo "Genstarter system..."
} >> "$LOGFILE" 2>&1

/sbin/shutdown -r now
