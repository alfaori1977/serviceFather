#!/bin/bash
CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

IFS='
'
for mapping in $(cat $1); do
    oldName=$(echo $mapping | awk '{print $1}')
    newName=$(echo $mapping | awk '{print $2}')
    if [ -d $CDIR/services/$oldName ]; then
        echo mv $CDIR/services/$oldName $CDIR/services/$newName
        mv $CDIR/services/$oldName $CDIR/services/$newName
    fi

done