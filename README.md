# Simple Portable IP Tunnel

This is a lightweight, portable Python application that allows you to create a TCP tunnel between two machines. It's useful for accessing internal IP addresses (like a router or a local server) from a remote location.

## Features
- **Single File**: No installation required.
- **Portable**: Can be compiled into a single `.exe` (Windows) or binary (Linux).
- **Two Modes**: 
  - `server`: Runs on the machine with access to the internal network.
  - `client`: Runs on the remote machine to access the tunnel.

## How to use

### 1. On the Gateway Machine (The one with the internal IP)
Run the software in `server` mode. You need to specify the internal IP and port you want to share.

```bash
python main.py --mode server --listen-port 8888 --target-host 192.168.1.1 --target-port 80
```
*This will share the router's web interface (192.168.1.1:80) through port 8888.*

### 2. On the Remote Machine
Run the software in `client` mode. You need to specify the public IP of the gateway machine.

```bash
python main.py --mode client --target-host [GATEWAY_PUBLIC_IP] --target-port 8888
```
*This will create a local listener on `127.0.0.1:9999`. You can now open your browser and go to `http://127.0.0.1:9999` to access the remote router.*

## How to compile to EXE (Windows)
If you want to create a portable `.exe` file:
1. Install PyInstaller: `pip install pyinstaller`
2. Run: `pyinstaller --onefile main.py`
3. The `.exe` will be in the `dist` folder.

## License
MIT
