CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
THIS_SCRIPT=$(basename $0 .sh)
SERVICE=$(basename $CDIR)

echo "$(date): $CDIR $SERVICE.$THIS_SCRIPT" 

while true; do 
    sleep 2
    echo "$(date):    --- $PWD: $SERVICE.$THIS_SCRIPT"
done    
