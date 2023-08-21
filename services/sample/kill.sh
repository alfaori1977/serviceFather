#!/bin/bash

CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
THIS_SCRIPT=$(basename $0 .sh)
SERVICE=$(basename $CDIR)

echo "$(date): $CDIR $SERVICE.$THIS_SCRIPT" >> /tmp/serviceFather.log

PID=$(ps -ef | grep  "SAMPLE" | grep -v grep | awk '{print $2}')
if [ "$PID" != "" ]; then
   kill $PID
fi

if screen -ls $SERVICE; then
    screen -X -S $SERVICE quit
fi
