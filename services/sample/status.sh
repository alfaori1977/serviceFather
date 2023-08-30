CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
THIS_SCRIPT=$(basename $0 .sh)
SERVICE=$(basename $CDIR)

screen -ls $SERVICE
