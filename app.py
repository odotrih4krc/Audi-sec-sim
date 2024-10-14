import machine
import network
import socket
import time
import camera

# Initialize camera
def init_camera():
    camera.init(0, 0, 640, 480)  # Adjust resolution as needed
    camera.quality(10)  # Set quality of the video

# Wi-Fi Connection
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        time.sleep(1)
    print('Connected to Wi-Fi:', wlan.ifconfig())

# Start streaming video
def start_streaming(client):
    camera.start()
    while True:
        buf = camera.capture()
        if buf is None:
            break
        client.send(buf)

# HTML/CSS/JavaScript for the GUI
html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automotive Security Camera</title>
    <style>
        body {
            background-color: #1a1a2e;
            color: #fff;
            font-family: 'Poppins', sans-serif;
            text-align: center;
        }
        .container {
            margin: auto;
            width: 80%;
        }
        video {
            border: 2px solid #00adb5;
            width: 100%;
            max-width: 600px;
        }
        button {
            background-color: #00adb5;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Audi Sec Sim - RIH4KRC</h1>
        <video id="video" autoplay></video>
        <br>
        <button onclick="recordVideo()">Record Video</button>
    </div>
    <script>
        const videoElement = document.getElementById('video');
        videoElement.src = 'http://<ESP32_IP>/stream';  // Replace <ESP32_IP> with actual IP

        function recordVideo() {
            fetch('/record'); // Endpoint to trigger video recording
        }
    </script>
</body>
</html>
"""

# Web server
def start_web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Listening on', addr)

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)

        if b'GET /' in request:
            # Serve the main HTML page
            cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n')
            cl.send(html)
        elif b'GET /stream' in request:
            # Start streaming video
            cl.send('HTTP/1.0 200 OK\r\nContent-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n')
            start_streaming(cl)
        elif b'GET /record' in request:
            # Start recording video (implement this based on your recording logic)
            # Placeholder for video recording logic
            print("Recording video...")
            time.sleep(10)  # Simulate recording for 10 seconds
            print("Recording stopped.")
            cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nRecording started.')
        
        cl.close()

# Main function
def main():
    init_camera()
    connect_wifi('your_SSID', 'your_password')
    start_web_server()

# Run the main function
if __name__ == '__main__':
    main()
