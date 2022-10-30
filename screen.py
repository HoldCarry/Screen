'''
2021/09/08
Tiga
windiows下使用adb截图
'''
import time
import sys, os

'''输入设备链接的adb调试地址'''
def ip_connect():
    ip_adress = input("输入链接的ip地址:(否则回车跳过默认使用本地设备链接)\n")
    if len(ip_adress) > 0:
        try:
            cnt = 'adb connect' + ip_adress
            devices = os.popen(cnt)
            phone = devices.readlines()[0]
            if 'unable' in phone:
                print("链接失败\n")
                return ip_connect()
            else:
                return ip_adress
        except:
            print("ADB调试模式为USB，需要切换到无线调试模式\n")
            print(
                "切换方法:\n第一步：Android设备开启USB调试，并且通过USB线连接到电脑\n第二步：在终端执行以下命令”adb tcpip 5555“\n第三步：在终端执行以下命令”adb connect ip“。此时拔出USB线，应该就可以adb通过wifi调试设备\n")
            return ip_connect()


'''封装设备地址和文件地址方便调用'''


def screenshot_info(devices=None, filepath=None):
    if filepath == None:
        filepath = "E:/screen/"
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    if devices == None:
        screenshot_cmd(filepath)
        adb_device(filepath)
    else:
        screenshot_cmd(filepath, devices)
        adb_devices(devices, filepath)


'''封装多台设备时更换设备的方法'''


def change_devices():
    cmd = os.popen("adb devices")
    devices_list = cmd.readlines()
    devices_list = devices_list[1:-1]
    for i in devices_list:
        print(i.split("\t")[0])
    devices = input("输入需要链接的设备:\t")
    for i in devices_list:
        if devices in i:
            return devices
        else:
            print("未找到改设备请重新输入！\n")
    change_devices()


'''截图逻辑，多个设备的或者IP链接的情况下进行判断'''


def adb_devices(devices_list, filepath=None):
    screenshot = input("是否截图（T/F/N）?\n")
    if screenshot == "t" or screenshot == "T":
        if filepath == None:
            screenshot_info()
        else:
            screenshot_info(devices_list, filepath)
    elif screenshot == "f" or screenshot == "F":
        devices = change_devices()
        if filepath == None:
            adb_devices(devices)
        else:
            adb_devices(devices, filepath)
    elif screenshot == "n" or screenshot == "N":
        sys.exit()


'''截图逻辑，adb devices只有一个设备链接的时候'''


def adb_device(filepath=None):
    screenshot = input("是否进行截图操作（T/F/N）?\n")
    if screenshot == "t" or screenshot == "T":
        if filepath == None:
            screenshot_info()
        else:
            screenshot_info(None, filepath)
    elif screenshot == "f" or screenshot == "F":
        device = change_devices()
        if filepath == None:
            adb_devices(device)
        else:
            adb_devices(device, filepath)


'''判断设备逻辑'''


def use_devices(list_len, devices_list, filepath=None):
    if list_len == 0:
        print("请检查是否已接连或启动调试模式或安装adb环境\n")
        msg = input("再次启动(T/F)?\n")
        if msg == "T" or msg == "t":
            my_devices = os.popen("adb devices")
            devices_list = my_devices.readlines()
            devices_list = devices_list[1:-1]
            list_len = len(devices_list)
            use_devices(list_len, my_devices.readlines())
        else:
            sys.exit()
    elif ":5555" in devices_list:
        print("T:截图  F：更换设备 N：退出\n")
        if filepath == None:
            adb_devices(devices_list)
        else:
            adb_devices(devices_list, filepath)
    elif list_len == 1:
        print("T:截图  F：更换设备 N：退出\n")
        if filepath == None:
            adb_device()
        else:
            adb_device(filepath)
    elif list_len > 1:
        for i in devices_list:
            print(i.split("\t")[0])
            device = input("请输入已连接的一个指定设备： \t")
        for i in devices_list:
            if device in i:
                print("T:截图  F：更换设备  N：退出")
                if filepath == None:
                    adb_devices(device)
                else:
                    adb_devices(device, filepath)
            else:
                print("未找到改设备请重新输入！")
        if filepath == None:
            use_devices(list_len, devices_list)
        else:
            use_devices(list_len, devices_list, filepath)


'''截图操作'''


def screenshot_cmd(filepath, device=None):
    if filepath == None:
        filepath = "E:/screen/"
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".png"
    if device == None:
        adb_screencap = 'adb shell screencap -p sdcard/' + file_name
        adb_pull = 'adb pull sdcard/' + file_name + ' ' + filepath + file_name
        adb_delete = 'adb shell rm sdcard/' + file_name
    else:
        adb_screencap = 'adb -s ' + device + ' shell screencap -p sdcard/' + file_name
        adb_pull = 'adb -s ' + device + ' pull sdcard/' + file_name + ' ' + filepath + file_name
        adb_delete = 'adb -s ' + device + ' shell rm sdcard/' + file_name
    screencap = os.system(adb_screencap)
    if screencap == 0:
        os.system(adb_pull)
        os.system(adb_delete)
    else:
        if device != None and ":5555" in device:
            print("连接断开，请重新连接\n")
            ip_adress = ip_connect()
            if ip_adress == None:
                ip_adress = ip_connect()
            else:
                new_device = ip_adress + ":5555"
                adb_devices(new_device, filepath)
        else:
            print("设备链接断开，请检查设备重新链接\t")
            device = change_devices()
            adb_devices(device,filepath)


if __name__ == '__main__':
    ip_address = ip_connect()
    filepath = input("请输入保存地址:(不输入回车跳过，默认保存至E:\screen\)\n") + "\\"
    # 查村设备链接
    devices = os.popen("adb devices")
    devices_llist = devices.readlines()
    devices_list = devices_llist[1:-1]
    list_len = len(devices_list)
    ip_add = 0
    if ip_address != None:
        for device in devices_list:
            while ip_address in device:
                ip_add = device.split("\t")[0]
                break
    if len(filepath) > 0:
        if ":\\" in filepath:
            if ip_add != 0:
                use_devices(list_len, ip_add, filepath)
            else:
                use_devices(list_len, devices_list, filepath)
        else:
            print("正在使用默认地址\n")
            if ip_add != 0:
                use_devices(list_len, ip_add)
            else:
                use_devices(list_len, devices_list)
    else:
        if ip_add != 0:
            use_devices(list_len, ip_add)
        else:
            use_devices(list_len, devices_list)
