#!/bin/bash
#Bash script som dumper SQL database, sender den til backup server og derefter wiper databasen, og restarter og
#opdaterer serveren.

LOGFILE="/var/log/event.log"

#PostgreSQL konfiguration
PG_DB="falldetectdatabase"
PG_USER="postgres"
PG_HOST="localhost"
BACKUP_DIR="/tmp"
BACKUP_FILE="$BACKUP_DIR/${PG_DB}_$(date +%F_%H-%M-%S).sql"

#Backupserver konfiguration
REMOTE_USER="ubunubackup"
REMOTE_HOST="192.168.3.2"
REMOTE_DIR="/home/ubunubackup/backups"

{
    echo "========== $(date) =========="
    echo "Starter backup af PostgreSQL database..."

    #Dump af database
    pg_dump -h "$PG_HOST" -U "$PG_USER" "$PG_DB" > "$BACKUP_FILE"

    echo "Backup fil: $BACKUP_FILE"
    echo "Overfører til backupserver..."

    #Kopiering til backupserver
    scp "$BACKUP_FILE" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

    echo "Backup overført succesfuldt..."

    echo "Sletter lokale database..."

    #Lukker aktive forbindelser
    psql -U "$PG_USER" -d postgres -c \
        "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='$PG_DB';"

    #Sletter og genskaber database
    dropdb -U "$PG_USER" "$PG_DB"
    createdb -U "$PG_USER" "$PG_DB"

    echo "Database slettet og genskabt"

    echo "Kører system opdateringer..."
    apt update -y
    apt upgrade -y
    apt full-upgrade -y
    apt autoremove -y
    apt autoclean -y

    echo "Genstarter system..."

} >> "$LOGFILE" 2>&1

rm -f "$BACKUP_FILE"

/sbin/shutdown -r now
