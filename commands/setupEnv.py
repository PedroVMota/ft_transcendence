import os
import socket
import secrets
import sys

def get_lan_ip_address():
    # Get the LAN IP address of the machine
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

def append_to_env(ip_address, port):
    env_file_path = '.env'

    with open(env_file_path, 'r') as env_file:
        lines = env_file.readlines()

    with open(env_file_path, 'w') as env_file:
        for line in lines:
            if line.startswith('SECRET_KEY='):
                if line.strip() == 'SECRET_KEY=':
                    secret_key = secrets.token_urlsafe(50)
                    line = f"SECRET_KEY={secret_key}\n"
            elif line.startswith('ALLOWED_HOSTS='):
                if line.strip() == 'ALLOWED_HOSTS=':
                    line = f"ALLOWED_HOSTS={ip_address},localhost,127.0.0.1\n"
                else:
                    if 'localhost' not in line:
                        line = line.strip() + ",localhost"
                    if '127.0.0.1' not in line:
                        line = line.strip() + ",127.0.0.1"
                    line = line.strip() + f",{ip_address}\n"
            elif line.startswith('CSRF_TRUSTED_ORIGINS='):
                if line.strip() == 'CSRF_TRUSTED_ORIGINS=':
                    line = f"CSRF_TRUSTED_ORIGINS=https://{ip_address}:{port},https://localhost:{port},https://127.0.0.1:{port}\n"
                else:
                    if f'https://localhost:{port}' not in line:
                        line = line.strip() + ",https://localhost:{port}"
                    if f'https://127.0.0.1:{port}' not in line:
                        line = line.strip() + ",https://127.0.0.1:{port}"
                    line = line.strip() + f",https://{ip_address}:{port}\n"
            elif line.startswith('PORT='):
                # Update the port value if it already exists
                line = f"PORT={port}\n"
            env_file.write(line)

        # If PORT key wasn't in the .env file, add it at the end


if __name__ == "__main__":
    # Default port value if not provided
    default_port = 8000

    # Parse command-line arguments
    port = default_port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])  # Convert argument to integer
        except ValueError:
            print("Invalid port number. Using default port 8000.")

    ip_address = get_lan_ip_address()
    append_to_env(ip_address, port)
    print(f"IP address {ip_address} and port {port} appended to .env file.")
