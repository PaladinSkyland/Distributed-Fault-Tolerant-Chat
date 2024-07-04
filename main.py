from node import Node
import threading

# Example usage:
if __name__ == '__main__':
    adresses = {
        'node1': ('localhost', 7001),
        'node2': ('localhost', 7002),
        'node3': ('localhost', 7003),
        'broadcast_recipient_address': [('localhost', 7002), ('localhost', 7001), ('localhost', 7003)]
    }

    node1 = Node('node1', adresses['node1'])
    node2 = Node('node2', adresses['node2'])
    node3 = Node('node3', adresses['node3'])

    # Start nodes
    node1.start()
    node2.start()
    node3.start()

    # Simulate sending broadcast messages
    node1.send_message(adresses['broadcast_recipient_address'], "Hello from Node 1")
    node2.send_message(adresses['broadcast_recipient_address'], "Hi back from Node 2")
    node3.send_message(adresses['broadcast_recipient_address'], "Hi from Node 3")

    # Simulate sending private messages
    node1.send_message([adresses['node2']], "Hello from Node 1 to Node 2")
    node2.send_message([adresses['node1']], "Hi back from Node 2 to Node 1")
