# -*- coding: utf-8 -*-

"""
/*
*
* Auther： Wenjie Zheng <wjzheng@robosense.cn>
* File:    general.py
*
*/
"""

import sys,re,subprocess
import platform

# 全局初始化变量
WindowsOS = None
LinuxOS = None

# 判断操作系统
OperatingSystem = platform.system()

if OperatingSystem == 'Windows':
    WindowsOS = 1

elif OperatingSystem == 'Linux':
    LinuxOS = 1

else:
    print('The OS is: [%s].' % OperatingSystem)
    print('[ERROR] This OS platform does not support.')
    print('Exit now.')
    exit(1)

def TYPE(msg=None, color='33', status=0):
    #msg默认为None,赋值后print(msg)
    #type为msg前冠字,默认为[INFO]
    #color为显示字体颜色，默认为 33 (黄色)
    #status为退出码,默认为0不退出,赋值后exit(status)

    if WindowsOS:
        import robosense.winprint as wp

    try:
        if msg != None:
            if type(msg) is list:
                for i in range(len(msg)):
                    if WindowsOS:
                        if color == '33':
                            wp.printyellow(str(msg[i]))
                        elif color == '31':
                            wp.printred(str(msg[i]))
                    elif LinuxOS:
                        temp = "\033[%sm " %(color) + str(msg[i]) + "\033[0m"
                        print(temp)
                print('\n')

            else:
                if WindowsOS:
                    if color == '33':
                        wp.printyellow(str(msg))
                    elif color == '31':
                        wp.printred(str(msg))
                elif LinuxOS:
                    temp = "\033[%sm " %(color) + str(msg) + "\033[0m"
                    print(temp)
                print('\n')

        if status != 0:
            sys.exit(status)

    except KeyboardInterrupt:
        print("\033[0m")
        if status != 0:
            sys.exit(status)

def CHECKIP(ipAddr):
    # 检查ip地址是否合法
    compile_ip = re.compile(
        '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True
    else:
        return False

def SYSCOM(command, flag=1, ifreceived=None, debug=0):
    if flag == 1:
        ifreceived_status = -1
        try:
            (status, output) = subprocess.getstatusoutput(command)
        except Exception as e:
            if (debug):
                TYPE('Exception error')
                TYPE(e)

        if status == 0:
            if (debug):
                TYPE('Commands Done. [%s]' % command)
            if ifreceived != None:
                if ifreceived in output:
                    if (debug):
                        TYPE('Received [%s]' % ifreceived)
                    ifreceived_status = 0
                else:
                    ifreceived_status = 1
        elif status != 0:
            if (debug):
                TYPE('Commands Status. [%s] [%s]' % (command, status))

        return (status, output, ifreceived_status)
    elif flag == 2:
        try:
            subprocess.Popen(['/bin/bash', '-c', command])
        except Exception as e:
            if (debug):
                TYPE('Exception error')
                TYPE(e)



