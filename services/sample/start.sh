CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
THIS_SCRIPT=$(basename $0 .sh)
SERVICE=$(basename $CDIR)

echo "$(date): $CDIR $SERVICE.$THIS_SCRIPT" >> /tmp/serviceFather.log

if [ -x $CDIR/screen.sh ]; then

   if screen -ls $SERVICE; then
      echo "$(date): $CDIR $SERVICE.$THIS_SCRIPT already running" >> /tmp/serviceFather.log
      exit 1
   fi

   screen -L -Logfile /tmp/$SERVICE.log -dmS $SERVICE bash -c  $CDIR/screen.sh
   screen -ls $SERVICE

fi

