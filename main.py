
import socket
import threading
import sys
import argparse

def forward_data(source_socket, destination_socket):
    try:
        while True:
            data = source_socket.recv(4096)
            if not data:
                break
            destination_socket.sendall(data)
    except Exception:
        pass
    finally:
        try:
            source_socket.close()
        except:
            pass
        try:
            destination_socket.close()
        except:
            pass

def handle_connection(local_socket, target_host, target_port):
    try:
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.connect((target_host, target_port))

        t1 = threading.Thread(target=forward_data, args=(local_socket, target_socket))
        t2 = threading.Thread(target=forward_data, args=(target_socket, local_socket))

        t1.start()
        t2.start()
    except Exception as e:
        print(f"Error connecting to target {target_host}:{target_port}: {e}")
        local_socket.close()

def start_tunnel(listen_host, listen_port, target_host, target_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((listen_host, listen_port))
        server.listen(5)
        print(f"[*] Tunnel started: {listen_host}:{listen_port} -> {target_host}:{target_port}")
        
        while True:
            client_socket, addr = server.accept()
            print(f"[*] Connection from {addr[0]}:{addr[1]}")
            threading.Thread(target=handle_connection, args=(client_socket, target_host, target_port)).start()
    except Exception as e:
        print(f"Failed to start tunnel: {e}")
    finally:
        server.close()

def main():
    parser = argparse.ArgumentParser(description="Simple Portable IP Tunnel")
    parser.add_argument("--mode", choices=["server", "client"], required=True, help="Run as server (on the gateway machine) or client (on the remote machine)")
    parser.add_argument("--listen-port", type=int, default=8888, help="Port to listen on (default: 8888)")
    parser.add_argument("--target-host", type=str, help="Internal target IP (for server mode) or Server IP (for client mode)")
    parser.add_argument("--target-port", type=int, help="Internal target port (for server mode) or Server port (for client mode)")

    args = parser.parse_args()

    if args.mode == "server":
        if not args.target_host or not args.target_port:
            print("Server mode requires --target-host (internal IP) and --target-port (internal port)")
            return
        start_tunnel("0.0.0.0", args.listen_port, args.target_host, args.target_port)
    elif args.mode == "client":
        if not args.target_host or not args.target_port:
            print("Client mode requires --target-host (server IP) and --target-port (server port)")
            return
        # Local proxy port is fixed for simplicity or can be another arg
        start_tunnel("127.0.0.1", 9999, args.target_host, args.target_port)

if __name__ == "__main__":
    main()
