from socket import *
import os
import sys
import struct
import time
import select
import binascii
import pandas as pd

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 1
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

def checksum(string):
# In this function we make the checksum of our packet
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet():
    #Fill in start
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.

    # Make the header in a similar way to the ping exercise.
    my_checksum = 0
    # 用进程号作标识
    my_id = os.getpid() & 0xffff
    # 序列号
    my_seq = 1

    # 打包出二进制首部
    my_header = struct.pack("bbHHh", TYPE_ECHO_REQUEST, CODE_ECHO_REQUEST_DEFAULT, my_checksum, my_id, my_seq)
    # 以当前系统时间作为报文的数据部分
    my_data = struct.pack("d", time.time())
    # 构建一个临时的数据报
    package = my_header + my_data

    # 利用原始数据报来计算真正的校验和
    my_checksum = check_sum(package)

    # 处理校验和的字节序列类型：主机序转换为网络序
    if sys.platform == 'darwin':
        my_checksum = socket.htons(my_checksum) & 0xffff
    else:
        my_checksum = socket.htons(my_checksum)

    # 重新构建出真正的数据包
    my_header = struct.pack("bbHHh", TYPE_ECHO_REQUEST, CODE_ECHO_REQUEST_DEFAULT, my_checksum, my_id, 1)
    ip_package = my_header + my_data
    return ip_package



    myChecksum = 0
    myID = os.getpid() & 0xFFFF

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    # header = struct.pack("!HHHHH", ICMP_ECHO_REQUEST, 0, myChecksum, pid, 1)
    data = struct.pack("d", time.time())
    # Append checksum to the header.
    myChecksum = checksum(header + data)
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
        # Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = htons(myChecksum)

    # Donâ€™t send the packet yet , just return the final packet in this function.
    #Fill in end

    # So the function ending should look like this
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    packet = header + data
    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    df = pd.DataFrame(columns=['Hop Count', 'Try', 'IP', 'Hostname', 'Response Code'])

    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):
            destAddr = gethostbyname(hostname)
            #Fill in start
            # Make a raw socket named mySocket
            icmp = getprotobyname("icmp")
            mySocket = socket(AF_INET, SOCK_RAW, icmp)

            #Fill in end

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    #Fill in start
                    recvPacket, addr = mySocket.recvfrom(1024)
                    try:
                        h_name_get = gethostbyaddr(addr[0])[0]
                    except:
                        h_name_get = "Error"
                    timeReceived = time.time()
                    timeLeft = timeLeft - howLongInSelect
                    #append response to your dataframe including hop #, try #, and "Timeout" responses as required by the acceptance criteria
                    hopnum = ttl
                    trynum = tries
                    response = "*    *    * Request timed out."

                    df = df.append({'Hop Count': hopnum, 'Try': trynum, 'IP': destAddr, 'Hostname': h_name_get,
                                        'Response Code': response},
                                       ignore_index=True)
                    #print (df)
                    print (df)
                    return df
                    #Fill in end
                recvPacket, addr = mySocket.recvfrom(1024)

                try:
                    h_name_get = gethostbyaddr(addr[0])[0]
                except:
                    h_name_get = "Error"

                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    #Fill in start
                    #append response to your dataframe including hop #, try #, and "Timeout" responses as required by the acceptance criteria
                    response = "*    *    * Request timed out."
                    hopnum = ttl
                    trynum = tries
                    df = df.append({'Hop Count': hopnum, 'Try': trynum, 'IP': destAddr, 'Hostname': h_name_get,
                                    'Response Code': response},
                                   ignore_index=True)
                    #print (df)
                    print (df)
                    return df
                    #Fill in end
            except Exception as e:
                #print (e) # uncomment to view exceptions
                continue

            else:
                #Fill in start
                #Fetch the icmp type from the IP packet
                icmpHeader = recvPacket[20:28]
                types, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
                #Fill in end
                try:
                    h_name_get = gethostbyaddr(addr[0])[0]
                except:
                    h_name_get = "Error"

                if types == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 +
                    bytes])[0]
                    #Fill in start
                    #You should update your dataframe with the required column field responses here
                    response = "Type 11"
                    hopnum = ttl
                    trynum = tries
                    df = df.append({'Hop Count': hopnum, 'Try': trynum, 'IP': destAddr, 'Hostname': h_name_get,
                                    'Response Code': response},
                                   ignore_index=True)
                    #Fill in end
                elif types == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #You should update your dataframe with the required column field responses here
                    response = "Type 3"
                    hopnum = ttl
                    trynum = tries
                    df = df.append({'Hop Count': hopnum, 'Try': trynum, 'IP': destAddr, 'Hostname': h_name_get,
                                    'Response Code': response},
                                   ignore_index=True)
                    #Fill in end
                elif types == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #You should update your dataframe with the required column field responses here
                    response = "Type 0"
                    hopnum = ttl
                    trynum = tries
                    df = df.append({'Hop Count': hopnum, 'Try': trynum, 'IP': destAddr, 'Hostname': h_name_get,
                                    'Response Code': response},
                                   ignore_index=True)
                    #Fill in end
                else:
                    #Fill in start
                    #If there is an exception/error to your if statements, you should append that to your df here
                    response = "Error"
                    hopnum = ttl
                    trynum = tries
                    df = df.append({'Hop Count': hopnum, 'Try': trynum, 'IP': destAddr, 'Hostname': h_name_get,
                                    'Response Code': response},
                                   ignore_index=True)
                    #Fill in end
                break
    return df

if __name__ == '__main__':
    get_route("google.co.il")