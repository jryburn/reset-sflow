# reset-sflow
Juniper Networks switches uses an Adaptative Sampling Rate that increases the sampling rate when the CPU is busy to protect the switch. However, the sampling rate does not come back down when the CPU comes back down. This script is designed to be run on a cronjob to check the sampling rate (4096 in my case) once a day and reset it if it has increased.

# Adaptive Sampling

More information on Juniper's use of Adaptative Sampling can be found here: [Sflow EX Series](https://www.juniper.net/documentation/en_US/junos/topics/concept/sflow-ex-series.html)

# Dependencies
This script will need the Juniper PYEZ modules.

    sudo -H pip install junos-eznc

# Installing
You will need to create a cronjob to run the script once a day. I run mine at midnight but any time is probably fine.

    crontab -e

Add this line to the bottom of the file and save.

    0 00 * * * /home/jryburn/reset-sflow.py
