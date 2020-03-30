# History
# 22 Feb 2020 : ArgParser added
# 23 Feb 2020 : Try and Except added under for loop, so that if SSH fail one device, script should continue


# show config on Cisco devices
# device IP is taken from InventoryDevice.txt or via command line
# commands taken from showCommands.txt or via command line


from netmiko import ConnectHandler
import time, re, sys
import socket, difflib
from time import gmtime, strftime
import getpass
import argparse
import logging

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    # Cisco username & PW for BLR Lab
    username = 'averma2'
    pw = 'Ank#2018'
    deviceType = 'cisco_xr'
    port = '22'

    # user need to input device ips and show commands via command line
    # but this is not mandatory that user input the value. if user don't input via command line, it will take from txt file created
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", help="Enter Device IP's", action='append', required=False)
    parser.add_argument("-c", help="Enter show commands", action='append', required=False)
    args = parser.parse_args()


def show_command():

    if args.ip:
        deviceIP = args.ip
        print('\ndevice ip from Arg user input\n')
    else:
        deviceIP = DeviceList()
        print('\ndevice ip from ShInvDevice.txt\n')

    print(deviceIP)

    if args.c:
        sh_commands = args.c
        print('\nshow cmds from Arg user input\n')
    else:
        sh_commands = CommandList()
        print('\nshow cmds from showCommands.txt\n')

    print(sh_commands)


    for i in range(len(deviceIP)):
        dp = deviceIP[i]
        try:
            ssh_cisco(dp, sh_commands)

        except Exception as e:
            c = str(e)
            c = '\n>> Error : '+str(dp)+'\n'+c+'\n---- END ----\n'
            print(c)
            createLog(c)
            time.sleep(0.5)


def ssh_cisco(dp, sh_commands):
    net_connect = ConnectHandler(device_type=deviceType, ip=dp, username=username, password=pw, port=port)
    output = net_connect.send_command_expect('ter len 0', delay_factor=5)  # added delay_factor as it was getting time out

    for j in range(len(sh_commands)):
        command = sh_commands[j]
        print ('\n>>>> ' + dp)
        createLog('\n>>>> ' + dp + '\n')
        print (command)

        output1 = net_connect.send_command_expect(command, delay_factor=5)
        time.sleep(1)

        print (output1 + '\n---- end ---\n')
        c = command + '\n' + output1 + '\n---- end ---\n'
        createLog(c)
        time.sleep(0.5)

    output4 = net_connect.disconnect()
    # print (output4)


# Raw log is created
def createLog(c):
    LocalTime= strftime("%d%m%Y", gmtime())
    f = open('showOutput-' + LocalTime + '.txt', 'a')
    f.write(c)
    #f.write('\n\n')
    f.close()

# read inventory device details from txt file
def DeviceList():
    f = open('ShInvDevice.txt','r')
    f1 = f.readlines()
    return f1

# read commands from txt file
def CommandList():
    f = open('showCommands.txt','r')
    f2 = f.readlines()
    return f2


show_command()
