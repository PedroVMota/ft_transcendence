import threading
import requests
from urllib.parse import urlparse
import time

def perform_request(url, num_requests):
    """
    Perform a number of HTTP requests to the given URL.
    
    :param url: URL to send the request to
    :param num_requests: Number of requests to perform
    """
    for _ in range(num_requests):
        try:
            response = requests.get(url, verify=False)  # Disable SSL verification
            print(f"Request to {url} returned status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request to {url} failed: {e}")

def stress_test(protocol, domain, port, path, num_threads, num_requests_per_thread):
    """
    Perform a stress test by making a large number of HTTP requests to the given URL.

    :param protocol: HTTP or HTTPS
    :param domain: The domain name or IP address of the server
    :param port: The port to use for the connection
    :param path: The path to the resource
    :param num_threads: The number of concurrent threads to run
    :param num_requests_per_thread: The number of requests each thread should perform
    """
    # Construct the full URL
    url = f"{protocol}://{domain}:{port}{path}"
    print(f"Starting stress test on {url} with {num_threads} threads, each performing {num_requests_per_thread} requests.")

    # Create a list to hold the threads
    threads = []

    # Start threads to perform the requests
    for i in range(num_threads):
        thread = threading.Thread(target=perform_request, args=(url, num_requests_per_thread))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("Stress test completed.")

if __name__ == "__main__":
    # Example usage
    protocol = "https"
    domain = "localhost"
    port = 65535
    path = "/"
    num_threads = 10  # Number of concurrent threads
    num_requests_per_thread = 100000  # Number of requests per thread

    start_time = time.time()
    stress_test(protocol, domain, port, path, num_threads, num_requests_per_thread)
    end_time = time.time()

    print(f"Total time taken: {end_time - start_time:.2f} seconds")
