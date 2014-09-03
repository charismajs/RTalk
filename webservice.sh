#!/bin/bash

f_message(){
        echo "[+] $1"
        #echo "space here"
}

TITLE="WebRTalk RestAPI"

# Carry out specific functions when asked to by the system
case "$1" in
        start)
                f_message "Starting ${TITLE}"
				/usr/bin/python /home/RTalk/restapi/webRTalk.py $RTALK_MODE &
				nohup /usr/local/bin/node /home/RTalk/NodeRTalk/server.js &
                sleep 2
                f_message "${TITLE} started"
                ;;
        stop)
                f_message "Stopping ${TITLE}"
                pid=`ps aux | grep "/usr/bin/python /home/RTalk/restapi/webRTalk.py" | awk '{print $2}'`
                if [[ $pid != "" ]]; then
                        kill -9 $pid
                fi
				pid=`ps aux | grep "/usr/local/bin/node /home/RTalk/NodeRTalk/server.js" | awk '{print $2}'`
				if [[ $pid != "" ]]; then
					kill -9 $pid
				fi
                f_message "${TITLE} stopped"
                ;;
        *)
                f_message "Usage: $0 {start|stop}"
                exit 1
                ;;
esac
exit 0
