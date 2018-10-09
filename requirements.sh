#!/usr/bin/env bash
ROOT=`pwd`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${DIR}

#build frotz, use Home because lots of games will share it ?
if [ ! -d $HOME/frotz ]
then
    echo "Installing frotz"
    git clone https://gitlab.com/DavidGriffith/frotz $HOME/frotz
    cd $HOME/frotz
    make dumb
    cd ${DIR}
fi

cd ${ROOT}
