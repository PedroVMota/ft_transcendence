import os
import socket

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

def append_to_env(ip_address):
    env_file_path = '/home/p/Desktop/42Projects/ft_transcendense/.env'
    
    with open(env_file_path, 'r') as env_file:
        lines = env_file.readlines()
    
    with open(env_file_path, 'w') as env_file:
        for line in lines:
            if line.startswith('ALLOWED_HOSTS='):
                if line.strip() == 'ALLOWED_HOSTS=':
                    line = f"ALLOWED_HOSTS={ip_address}\n"
                else:
                    line = line.strip() + f",{ip_address}\n"
            elif line.startswith('CSRF_TRUSTED_ORIGINS='):
                if line.strip() == 'CSRF_TRUSTED_ORIGINS=':
                    line = f"CSRF_TRUSTED_ORIGINS=https://{ip_address}\n"
                else:
                    line = line.strip() + f",https://{ip_address}\n"
            env_file.write(line)

if __name__ == "__main__":
    ip_address = get_lan_ip_address()
    append_to_env(ip_address)
    print(f"IP address {ip_address} appended to .env file.")