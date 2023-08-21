CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
THIS_SCRIPT=$(basename $0 .sh)
SERVICE=$(basename $CDIR)

echo "$(date): $CDIR $SERVICE.$THIS_SCRIPT" >> /tmp/serviceFather.log

if [ -x $CDIR/kill.sh ]; then
   $CDIR/kill.sh
fi
$CDIR/start.sh
