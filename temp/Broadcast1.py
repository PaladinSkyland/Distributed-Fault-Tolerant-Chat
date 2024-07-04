def increment_vector_clock(vc, node_id):
    vc[node_id] += 1

def update_vector_clock(vc1, vc2):
    for node_id in vc1.keys():
        vc1[node_id] = max(vc1[node_id], vc2[node_id])

def can_deliver(vc, sender_id, sender_vc):
    if sender_vc[sender_id] != vc[sender_id] + 1:
        return False
    for node_id in vc.keys():
        if node_id != sender_id and sender_vc[node_id] > vc[node_id]:
            return False
    return True



import socket
import json

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the address and port of the recipient
recipient_address = ('localhost', 12345)

# Unique identifier for this sender node
sender_id = 'node1'
vector_clock = {sender_id: 0}

def send_message(message):
    increment_vector_clock(vector_clock, sender_id)
    payload = {
        'sender_id': sender_id,
        'vector_clock': vector_clock.copy(),
        'message': message
    }
    sock.sendto(json.dumps(payload).encode('utf-8'), recipient_address)

def main():
    while True:
        message = input("Enter message to send: ")
        send_message(message)

if __name__ == '__main__':
    main()
