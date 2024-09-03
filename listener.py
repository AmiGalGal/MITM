import scapy.all as scapy
from scapy_http import http
def listen():
    scapy.sniff(iface="eth0", store= False, prn =anal)

def anal(packet):
    if packet.haslayer (http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)
        
    
listen()
