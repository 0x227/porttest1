import argparse
import socket
import threading
import time

def scan(target, start_port, end_port, timeout):
    # Get IP address of target
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Invalid hostname")
        return

    # Scan ports in range
    for port in range(start_port, end_port + 1):
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # Attempt to connect to the port
        result = sock.connect_ex((ip, port))

        # Check if port is open
        if result == 0:
            print(f"Port {port}: Open")

        sock.close()

def threaded_scan(target, start_port, end_port, num_threads, timeout):
    # Calculate number of ports to scan per thread
    num_ports_per_thread = (end_port - start_port + 1) // num_threads

    # Create a list of threads
    threads = []
    for i in range(num_threads):
        # Calculate start and end ports for this thread
        thread_start_port = start_port + i * num_ports_per_thread
        thread_end_port = thread_start_port + num_ports_per_thread - 1
        if i == num_threads - 1:
            thread_end_port = end_port

        # Create and start the thread
        thread = threading.Thread(target=scan, args=(target, thread_start_port, thread_end_port, timeout))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Python Port Scanner")
    parser.add_argument("target", help="target hostname or IP address")
    parser.add_argument("--start-port", type=int, default=1, help="first port to scan (default: 1)")
    parser.add_argument("--end-port", type=int, default=1024, help="last port to scan (default: 1024)")
    parser.add_argument("--num-threads", type=int, default=10, help="number of threads to use (default: 10)")
    parser.add_argument("--timeout", type=float, default=0.5, help="timeout for each connection attempt (default: 0.5)")
    args = parser.parse_args()

    # Perform port scan
    start_time = time.time()
    threaded_scan(args.target, args.start_port, args.end_port, args.num_threads, args.timeout)
    end_time = time.time()

    # Print results
    print(f"\nScan completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
