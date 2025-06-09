# helix_orin
Scripts to run the Orin for the drone demo in the AI Studio 

## Scripts

`helix_yolo.py`: the Yolov11.onnx model script 

`inference.py`: calls `helix_yolo.py`. To run the `helix_yolo.py` on its own, do: `python3 helix_yolo.py`. 
- this script uses cv2 and subprocess to call the big screen at 'rtp://10.136.89.17:1234'

`time_update.sh` makes sure the time is correct and updates the system clock by fetching the current time from Google. It ensures accurate timestamps since the Orin clock might not be right.

`network_ping.sh` pings the target IP of the Helix and is kept alive via the crontab that pings every 30 minutes

All scripts are on the path: `/home/helix/Desktop/`

## Usage

`bash start_inference.sh`

This will update the system time using `./time_update.sh`. 

Then it will wait a moment to ensure the time is properly set for 2 seconds. 

Then, the inference will start: `python3 inference.py`. 

## Keep network alive 

crontab is: 

`*/30 * * * * /home/helix/Desktop/network_ping.sh`

you can check it via terminal at: `sudo crontab -l`

To modify: `sudo crontab -e`

The editor is Vim.
