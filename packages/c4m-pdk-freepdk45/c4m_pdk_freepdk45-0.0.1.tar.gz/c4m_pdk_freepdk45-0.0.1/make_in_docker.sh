#!/bin/sh

check()
{
    if [ -z "$(which docker)" ]; then
        echo "No docker found"
        exit 1
    fi
}

pull()
{
    docker image history chips4makers/coriolis >/dev/null 2>&1
    dockexit=$?
    if [ $dockexit -ne 0 ]; then
        read -p "OK to pull image of around 2.3GB (y/n)" choice
    else
        read -p "OK to update image; may download up to 2.3GB of data (y/n)" choice
    fi
    case "$choice" in
        y|yes|Y ) docker pull chips4makers/coriolis;;
        n|no|N ) if [ $dockexit -ne 0 ]; then exit 1; else echo "Using existing image"; fi;;
        * ) echo "y or n expected"; exit 1;;
    esac
}

check
pull

user=`id -n -u`
uid=`id -u`
gid=`id -g`
top=$(dirname $(realpath $0))

docker run -it --rm \
  --user ${uid}:${gid} --userns host --env USER=${user} --env HOME=/tmp \
  -v ${top}:/top --workdir /top \
  -h eda \
  chips4makers/coriolis scripts/docker_make.sh
