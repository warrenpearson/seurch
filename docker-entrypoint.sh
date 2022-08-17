#!/bin/sh

case "$(uname -s)" in
   Linux)
    # Make docker-compose linux friendly
    HOST_DOMAIN="host.docker.internal"

    ping -q -c1 $HOST_DOMAIN > /dev/null 2>&1

    if [ $? -ne 0 ]; then
        HOST_IP=$(ip route | awk 'NR==1 {print $3}')
        echo "$HOST_IP\t$HOST_DOMAIN" >> /etc/hosts
    fi
    ;;
esac

python3 -m flask run