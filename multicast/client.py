import socket, struct, io, subprocess, json

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
PROCESS = None

def getParams(url, w, h):
    with open('config.json') as cfg:
        data = json.load(cfg)
        params = ["mpv", url, "--fs", "--no-keepaspect", "-vf"]
        pW = w // data['gridX']
        pH = h // data['gridY']
        pX = data['myX']*pW
        pY = data['myY']*pH
        params.append("crop={}:{}:{}:{}".format(pW, pH, pX, pY))
        return params
    return []

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((MCAST_GRP, MCAST_PORT))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY))

    while True:
        data = io.BytesIO(sock.recv(102400)).read().decode('utf_8')
        if data == "END":
            print("Video ended. Killing mpv...")
            if PROCESS is not None:
                PROCESS.kill()
                PROCESS = None
        else:
            url, w, h = tuple(data.split(' '))
            params = getParams(url, int(w), int(h))
            print("Playing video with command line: '{}'...".format(" ".join(params)))
            PROCESS = subprocess.Popen(params, stdout=subprocess.PIPE)
        