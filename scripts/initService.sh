#!/bin/bash
CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
SERVICE=$1
SAMPLE_SERVICE=sample


rsync -av $CDIR/services/$SAMPLE_SERVICE/ $CDIR/services/$SERVICE/

