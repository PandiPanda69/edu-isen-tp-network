import socket


def check_project_ports(cfg):
    return {
        "ssh": check_port(cfg["admin"]),
        "api_pub": check_port(cfg["api_pub"]),
        "api_priv": check_port(cfg["api_priv"]),
    }
    

def check_port(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(split_addr(addr))
    sock.close()

    return result == 0


def split_addr(addr):
    tok = addr.split(":")
    return (tok[0], int(tok[1]))
