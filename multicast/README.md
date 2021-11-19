# Server Instructions

- Copy `server.py` to `/home/pi`
- Copy `videowallserver.service` to `/lib/systemd/system`
- Run the following commands:
    sudo chmod 644 /lib/systemd/system/videowallserver.service
    sudo systemctl enable videowallserver.service
    sudo systemctl start videowallserver.service
    

# Client Instructions

- Copy `client.py` to `/home/pi`
- Copy `config.json` to `/home/pi`
- Change the settings as needed in `config.json`
- Copy `videowallclient.service` to `/lib/systemd/system`
- Run the following commands:
    sudo apt-get update
    sudo apt-get install mpv
    sudo pip3 install ffmpeg-python
    sudo chmod 644 /lib/systemd/system/videowallclient.service
    sudo systemctl enable videowallclient.service
    sudo systemctl start videowallclient.service