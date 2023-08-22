#!/bin/bash

CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IFS='
'

action=${2:-"restart"}

while read servInfo; do
	service=$(echo $servInfo | awk '{print $1}')
	host=$(echo $servInfo | awk '{print $2}')

        echo $CDIR/performAction.sh $service $action $host 
        $CDIR/performAction.sh $service $action $host 

done < $1

