cp raspberry-fan.py /usr/local/bin/
cp fancontrol.sh /etc/init.d/
update-rc.d fancontrol.sh defaults
/etc/init.d/fancontrol.sh start