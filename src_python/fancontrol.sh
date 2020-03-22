#! /bin/sh

### BEGIN INIT INFO
# Provides:          fancontrol.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO
# https://howchoo.com/g/ote2mjkzzta/control-raspberry-pi-fan-temperature-python

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting fancontrol.py"
    /usr/local/bin/raspberry-fan.py &
    ;;
  stop)
    echo "Stopping fancontrol.py"
    pkill -f /usr/local/bin/raspberry-fan.py
    ;;
  *)
    echo "Usage: /etc/init.d/fancontrol.sh {start|stop}"
    exit 1
    ;;
esac

exit 0