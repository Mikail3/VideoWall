import socket, os, time, mimetypes, subprocess, ffmpeg

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
MULTICAST_TTL = 2
FFMPEG_MCAST = 'udp://224.1.1.1:5008'
WATCH_DIR = "/media/pi"

def pollDrive():
    drives = {f.path: f.is_dir() for f in os.scandir(WATCH_DIR) if f.name != "." and f.name != ".."}
    for k, v in drives.items():
        if v:
            print("Drive found...")
            return k
    print("No drive found...")
    return None

def findFiles(drive):
    files = [f for f in os.scandir(drive) if f.name != "." and f.name != ".." and f.is_file()]
    playable = []
    for f in files:
        mimetype, _ = mimetypes.guess_type(f.name)
        if mimetype is not None and 'video' in mimetype:
            playable.append(f.path)
            print("Found video file {}...".format(f.name))
    if playable:
        return sorted(playable)
    else:
        print("No videos found...")
        return []

def getResolution(f):
    probe = ffmpeg.probe(f)
    video = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
    for v in video:
        return "{} {}".format(v['width'], v['height'])
    return None

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    while True:
        drive = pollDrive()
        if drive is not None:
            print("Attempting to find videos on root...")
            files = findFiles(drive)
            for f in files:
                print("Beginning to stream {}...".format(f))
                try:
                    res = getResolution(f)
                    if res is not None:
                        payload = "{} {}".format(FFMPEG_MCAST, res)
                        sock.sendto(payload.encode('utf_8'), (MCAST_GRP, MCAST_PORT))
                        time.sleep(5)
                        subprocess.run(["ffmpeg", "-re", "-i", f, "-codec", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", "{}?ttl=2&packetsize=1316".format(FFMPEG_MCAST)])
                        time.sleep(5)
                        sock.sendto(b'END', (MCAST_GRP, MCAST_PORT))
                    else:
                        print("Invalid file...")
                    print("Done, restarting...")
                    time.sleep(1)
                except:
                    print("Could not stream file...")
        time.sleep(1)