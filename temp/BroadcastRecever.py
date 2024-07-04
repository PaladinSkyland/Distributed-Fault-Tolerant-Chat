def increment_vector_clock(vc, node_id):
    vc[node_id] += 1

def update_vector_clock(vc1, vc2):
    for node_id in vc1.keys():
        vc1[node_id] = max(vc1[node_id], vc2[node_id])

def can_deliver(vc, sender_id, sender_vc):
    if sender_vc[sender_id] != vc[sender_id] + 1:
        return False
    for node_id in vc.keys():
        print (node_id)
        if node_id != sender_id and sender_vc[node_id] > vc[node_id]:
            return False
    return True


import socket
import json

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a local address and port
local_address = ('localhost', 12345)
sock.bind(local_address)

# Dictionary to track vector clocks for each node
vector_clocks = {}
buffered_messages = []

def process_message(sender_id, message):
    print(f"Processed message from {sender_id}: {message}")

def deliver_messages():
    global buffered_messages
    for message in list(buffered_messages):
        sender_id = message['sender_id']
        sender_vc = message['vector_clock']
        if can_deliver(vector_clocks, sender_id, sender_vc):
            process_message(sender_id, message['message'])
            update_vector_clock(vector_clocks, sender_vc)
            buffered_messages.remove(message)

def receive_message():
    while True:
        data, addr = sock.recvfrom(4096)
        payload = json.loads(data.decode('utf-8'))
        
        sender_id = payload['sender_id']
        message = payload['message']
        sender_vc = payload['vector_clock']
        
        if sender_id not in vector_clocks:
            vector_clocks[sender_id] = 0

        if can_deliver(vector_clocks, sender_id, sender_vc):
            process_message(sender_id, message)
            update_vector_clock(vector_clocks, sender_vc)
            deliver_messages()
        else:
            buffered_messages.append(payload)

if __name__ == '__main__':
    receive_message()
