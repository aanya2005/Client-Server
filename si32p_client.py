#
# Client simple example using makefile
#
import socket


def start_client(server_address: str, server_port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server_address, server_port))

        send = client.makefile("w")
        recv = client.makefile("r")

        print("ICS32 simple client connected to "+
              f"{server_address} on {server_port}")

        while True:
            msg = input("Enter message to send: ")
            send.write(msg + "\r\n")
            send.flush()

            srv_msg = recv.readline()[:-1]
            print("Response received from server: ", srv_msg)
            # check if the command send by the client was INVERT
            # since if it was, a COMPLETE is expected
            if "INVERT" in msg:
                srv_msg = recv.readline()[:-1]
                if "COMPLETE" in srv_msg:
                    continue
                else:
                    print("Server sent an unexpected response. Disconnecting.")
                    break
            elif "LOWERCASE" in msg:
                srv_msg = recv.readline()
                if "COMPLETE" in srv_msg:
                    continue
                else:
                    print("Server sent an unexpected response. Disconnecting.")
                    break

if __name__ == "__main__":
    print("-------------------------------------")
    print(" ICS simple socket client")
    print(" Server configuration")
    srv_ip = input("Enter server IP address : ")
    srv_port = input("Enter server port      : ")
    print("-------------------------------------")
    start_client(srv_ip, int(srv_port))
