#!/bin/bash

# First update the system time
./time_update.sh

# Wait a moment to ensure time is properly set
sleep 2

# Start the inference script
python3 inference.py 