import time
import network_connection_monitor
import config

ncm = network_connection_monitor.NetworkConnectionMonitor(config.DATABASE_DETAILS)

while True:
    check = ncm.check_conenction()

    if check.get('return_code') == 0:
        print "Connected to the internet"
        ncm.set_success_status(1)

    else:
        print "No connection"
        ncm.set_success_status(0)

    # print check.get('return_code')
    # print check.get('output')

    ncm.store_check_status()

    time.sleep(30)
