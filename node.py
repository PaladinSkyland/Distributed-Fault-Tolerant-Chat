import socket
import json
import threading
import time
import random

class Node:
    def __init__(self, node_id : str, recipient_address ):
        self.node_id = node_id
        
        self.vector_clock = {self.node_id: 0}
        self.buffered_messages = []

        self.private_history_messages = []
        self.broadcast_history_messages = []

        self.recipient_address = recipient_address

        # Socket 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(self.recipient_address)
    
    def send_message(self, recipient_addresses, message):
        if not isinstance(recipient_addresses, list):
            recipient_addresses = [recipient_addresses]
        
        self.increment_vector_clock()
        payload = {
            'sender_id': self.node_id,
            'vector_clock': self.vector_clock.copy(),
            'message': message
        }
        for recipient_address in recipient_addresses:
            self.sock.sendto(json.dumps(payload).encode('utf-8'), recipient_address)
    
    def increment_vector_clock(self):
        self.vector_clock[self.node_id] += 1
    
    def update_vector_clock(self, sender_vc):
        for node_id in self.vector_clock.keys():
            self.vector_clock[node_id] = max(self.vector_clock[node_id], sender_vc.get(node_id, 0))
    
    def can_deliver(self, sender_id, sender_vc):
        if sender_vc[sender_id] != self.vector_clock[sender_id] + 1:
            return False
        for node_id in self.vector_clock.keys():
            if node_id != sender_id and sender_vc.get(node_id, 0) > self.vector_clock[node_id]:
                return False
        return True
    
    def process_message(self, sender_id, message, sender_vc):
        print(f"Node {self.node_id} processed message from {sender_id}: {message}, vc: {sender_vc}")
    
    def receive_message(self):
        while True:
            self.random_sleep()
            data, addr = self.sock.recvfrom(4096)
            payload = json.loads(data.decode('utf-8'))
            
            sender_id = payload['sender_id']
            sender_vc = payload['vector_clock']
            message = payload['message']
            
            if sender_id not in self.vector_clock:
                self.vector_clock[sender_id] = 0
            
            if self.can_deliver(sender_id, sender_vc):
                self.process_message(sender_id, message, sender_vc)
                self.update_vector_clock(sender_vc)
                self.deliver_buffered_messages()
            else:
                self.buffered_messages.append(payload)
    
    def deliver_buffered_messages(self):
        messages_to_remove = []
        for message in self.buffered_messages:
            sender_id = message['sender_id']
            sender_vc = message['vector_clock']
            if self.can_deliver(sender_id, sender_vc):
                self.process_message(sender_id, message['message'], sender_vc)
                self.update_vector_clock(sender_vc)
                messages_to_remove.append(message)
        for message in messages_to_remove:
            self.buffered_messages.remove(message)

    def random_sleep(self):
        time.sleep(random.uniform(0.1, 2))
    
    def start(self):
        print(f"Node {self.node_id} started listening on {self.recipient_address}")
        thread = threading.Thread(target=self.receive_message)
        thread.start()

    def __del__(self):
        self.sock.close()