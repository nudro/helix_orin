#!/bin/bash

# Ping the target IP and log the results
/bin/ping -c 4 10.136.89.12 2>&1 | logger -t pngcmd 