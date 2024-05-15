import csv
import os

def int_status_cutsheet_data(hostname, legacy_ip_address):
    with open(f'{hostname} interface status.txt', 'r', newline='') as raw_int_status:
        with open(f'{hostname} interface status.csv', 'w', newline='') as cutsheet_int_status_data: 
            status_csv_writer = csv.writer(cutsheet_int_status_data)

            status_list = ['connected', 'notconnect','disabled','inactive','err-disabled','xcvrAbsen','notconnec']
            list_of_duplexs = ['full','half','a-full','auto','a-half']
            list_of_speed = ['10','100','1000','a-10','a-100','a-1000','a-2500','10G','40G','auto']

            for interface_details in raw_int_status:

                list_of_interface_details = interface_details.split()

                try:
                    if '/' in list_of_interface_details[0]:
                        interface = list_of_interface_details[0]
                        status = ''
                        duplex = ''
                        speed = ''

                        for is_status in list_of_interface_details:
                            if is_status in status_list:
                                status = is_status

                        for is_duplex in list_of_interface_details:
                            if is_duplex in list_of_duplexs:                                
                                duplex = is_duplex

                                if 'a-' not in duplex and duplex != 'auto':
                                    duplex = 'a-' + duplex
                        
                        for is_speed in list_of_interface_details:
                            if is_speed in list_of_speed:
                                speed = is_speed

                                if 'a-' not in speed and speed != 'auto':
                                    speed = 'a-' + speed
                    
                        status_csv_writer.writerow([hostname, legacy_ip_address, interface, status, duplex, speed])

                except IndexError:
                    continue

def running_config_cutsheet_data(hostname):
    with open(f'{hostname} running config.txt', 'r', newline='') as running_config_sec_int:
        with open(f'{hostname} int des and vlans.csv', 'w', newline='') as running_int_vlans_des:
            interface_types = {'Ethernet' : 'Eth','AppGigabitEthernet':'AP', 'TwoGigabitEthernet':'Tw', 'FiveGigabitEthernet': 'Fi', 'TenGigabitEthernet': 'Te', 'FortyGigabitEthernet': 'Fo', 'FastEthernet': 'Fa', 'GigabitEthernet' : 'Gi'}

            port_info_csv_writer = csv.writer(running_int_vlans_des)
            
            running_config = ''
            for all in running_config_sec_int:
                all = all.strip('\r\n')
                running_config += all

            for interfaces in running_config.split('interface'):
                list_of_interface_details = interfaces.split()

                interface = ''
                port_description = ''
                access_vlan = ''
                voice_vlan = ''

                if '/' not in list_of_interface_details[0]:
                     continue

                for i in interface_types.keys():
                    if i in list_of_interface_details[0]:
                        interface = interface_types[i] + list_of_interface_details[0][list_of_interface_details[0].index("net")+3:]
                
                if '!' in interface:
                    interface = interface.strip('!')      
                
                if 'access vlan' in interfaces:
                    count = 0

                    correct_access = list_of_interface_details[list_of_interface_details.index('access')-1]

                    if correct_access != 'switchport':

                        while correct_access != 'switchport':
                            count += 1
                            correct_access = list_of_interface_details[list_of_interface_details.index('access', count)-1]

                        access_vlan = list_of_interface_details[list_of_interface_details.index('access', count)+2]
                    else:
                        access_vlan = list_of_interface_details[list_of_interface_details.index('access')+2]

                    access_vlan = access_vlan.strip('!')

                if 'voice vlan' in interfaces:    
                    voice_vlan = list_of_interface_details[list_of_interface_details.index('voice')+2]

                if 'trunk' in interfaces:
                    voice_vlan = 'trunk'
                    access_vlan = 'trunk'
                port_info_csv_writer.writerow([interface, port_description, access_vlan, voice_vlan])

def mac_address_table_cutsheet_data(hostname):

 with open(f"{hostname} mac address table.txt", newline='') as mac_text_file:
    with open(f"{hostname} port to mac address.csv", 'w', newline='') as mac_csv_file:
        interface_types = {'Ethernet' : 'Eth','AppGigabitEthernet':'AP', 'TwoGigabitEthernet':'Tw', 'FiveGigabitEthernet': 'Fi', 'TenGigabitEthernet': 'Te', 'FortyGigabitEthernet': 'Fo', 'FastEthernet': 'Fa', 'GigabitEthernet' : 'Gi'}

        mac_csv_writer = csv.writer(mac_csv_file)

        interface_to_mac = {}

        for mac in mac_text_file:
            list_of_mac = mac.split()
            interface = ''
            
            try:
                if '/' not in list_of_mac[-1] or 'Po' in list_of_mac[-1]:
                    continue
            except IndexError:
                continue

            for i in interface_types.keys():
                if i in list_of_mac[-1]:
                    interface = interface_types[i] + list_of_mac[-1][list_of_mac[-1].index("net")+3:]
                else:
                    interface = list_of_mac[-1]
            try:
                mac_address = list_of_mac[1]
            except IndexError:
                continue
            try:
                if interface_to_mac[interface] !=  None and mac_address not in interface_to_mac[interface]:
                    interface_to_mac[interface] += mac_address + ','

            except KeyError:
                interface_to_mac[interface] = mac_address + ','
        for interface_and_macs in interface_to_mac.items():
            interface = ' ' + interface_and_macs[0]
            macs = interface_and_macs[1].split(',')

            row = [interface]

            for i in macs:
                row.append(i)

            mac_csv_writer.writerow(row)

def interface_description_cutsheet_data(hostname):
    with open(f'{hostname} interface descriptions.txt', newline='') as interface_description:
        with open(f'{hostname} int des and vlans.csv', newline='') as running_int_vlans_des:
            with open(f'{hostname} interface description with vlans.csv', 'w', newline='') as int_vlans_des:
                int_vlans_des_csv_writer = csv.writer(int_vlans_des)
                
                for description in interface_description:
                    list_of_description = description.split()
                    description = []
                    
                    for interface in running_int_vlans_des:
                        list_of_interface = interface.strip('\r\n').split(',')
                        try:
                            if list_of_interface[0] == list_of_description[0]:
                                if len(list_of_description) > 4:
                                    list_of_interface.insert(1,' '.join(list_of_description[3:]))
                                    list_of_interface.pop(2)
                                    break
                                else:
                                    break
                        except IndexError:
                            continue
                    int_vlans_des_csv_writer.writerow(list_of_interface)
                    running_int_vlans_des.seek(0)

def access_points_to_interface_cutsheet_data(hostname):
    with open(f'{hostname} cdp neighbors.txt', newline='') as cdp_neighbor:
        with open(f'{hostname} Aps to port.csv', 'w', newline='') as access_points:

            for device in cdp_neighbor:
                list_of_devices = device.split()
                
                interface = ''
                type_of_inter = ''

                if 'AIR-' in device:
                    if '.' in list_of_devices[0]:
                        list_of_devices.pop(0)

                    type_of_inter = list_of_devices[0][:-1]
                    interface = type_of_inter + list_of_devices[1] + '\n'
                    access_points.write(interface)

def pre_portmapper(hostname, legacy_ip_address, new_hostname, new_ip):
    with open(f'{hostname} interface status.csv', newline='') as int_status:
        with open(f'{hostname} interface description with vlans.csv', newline='') as int_des_vlan:
            with open(f'{hostname} port to mac address.csv') as mac_vendor:
                with open(f'{hostname} data combined.csv', 'w', newline='') as Data_combined:
                    Data_combined_csv_writer = csv.writer(Data_combined)

                    oui_db = search_oui_database('oui.txt')
                    
                    header = f"Legacy Switch,Legacy Switch IP,Legacy Switch Port,PP Port #,New Switch,New Switch IP,New Switch Port,New Patch Cord Color,Critical Device (Y/N),Suggested switch,Suggested blade,Status,Speed,Duplex,Access Vlan,Voice Vlan,Legacy Port Description,Mac Address,Vendor,Mac Address,Vendor,\n"
                    Data_combined.write(header)
                    
                    for interface_details in int_status:
                        interface = ''
                        connection_status = ''
                        duplex = ''
                        negotiated_speed = ''
                        access_vlan = ''
                        voice_vlan = ''
                        port_desc = ''
                        mac_list = []

                        interface_details = interface_details.split(',')

                        interface = interface_details[2]

                        if 'po' in interface.lower():
                            continue

                        connection_status = interface_details[3]
                        duplex = interface_details[4]
                        negotiated_speed = interface_details[5].strip('\r\n')

                        for int_desc_and_vlan in int_des_vlan:
                            list_of_interfaces_details = int_desc_and_vlan.split(',')

                            if list_of_interfaces_details[0] == interface_details[2]:
                                port_desc = list_of_interfaces_details[1]
                                access_vlan = list_of_interfaces_details[2]
                                voice_vlan = list_of_interfaces_details[3].strip('\r\n')
                                break
                        int_des_vlan.seek(1)

                        for port_to_macs in mac_vendor:
                            port_to_macs = port_to_macs.strip('\r\n')
                            list_of_port_to_macs = port_to_macs.split(',')
                            list_of_port_to_macs[0] = list_of_port_to_macs[0].strip()

                            if list_of_port_to_macs[0] == interface_details[2]:
                                list_of_port_to_macs.pop(-1)
                                mac_list = list_of_port_to_macs[1:]
                                break
                        mac_vendor.seek(1)

                        row = [hostname,legacy_ip_address,interface,'',new_hostname,new_ip,'','','','','',connection_status,negotiated_speed,duplex,access_vlan,voice_vlan,port_desc]

                        if len(mac_list) != 0:
                            for mac in enumerate(mac_list):

                                vendor = mac_lookup(mac[1])
                                row.append(mac[1])
                                row.append(vendor)

                        Data_combined_csv_writer.writerow(row)

    os.remove(f'{hostname} interface status.csv')
    os.remove(f'{hostname} int des and vlans.csv')
    os.remove(f'{hostname} port to mac address.csv')
    os.remove(f'{hostname} interface descriptions.txt')
    os.remove(f'{hostname} interface status.txt')

def cable_color(hostname):
    with open(f'{hostname} pre portmapped.csv', 'w', newline='') as pre_portmap:
         with open(f'{hostname} data combined.csv', newline='') as Data_combined:
             with open(f'{hostname} Aps to port.csv', newline='') as access_points:
                pre_portmap_csv_writer = csv.writer(pre_portmap)
             
                wireless_ports = []                 #Purple Cable
                biomed = 'FS FORTH-SYSTEME GmbH'    #Green  Cable
                time_clock_macs = '0040.58'         #Yellow Cable
                data = 'Blue'                       #Blue   Cable
                security_macs = []                  #White  Cable

                for ap_ports in access_points:
                    wireless_ports.append(ap_ports.strip('\n'))

                for data in Data_combined:
                    list_of_data = data.split(',')

                    if list_of_data[0] == "Legacy Switch":
                        pre_portmap_csv_writer.writerow(list_of_data)
                        continue

                    if list_of_data[2] in wireless_ports:
                        list_of_data.insert(7,'Purple')
                        list_of_data.pop(8)
                        
                        list_of_data.insert(8,'Y')
                        list_of_data.pop(9)

                    elif biomed in data:
                        list_of_data.insert(7,'Green')
                        list_of_data.pop(8)

                    elif time_clock_macs in data:
                        list_of_data.insert(7,'Yellow')
                        list_of_data.pop(8)

                    # elif security_macs in data:
                    #     list_of_data.insert(7,'White')
                    #     list_of_data.pop(8)
                    
                    else:
                        list_of_data.insert(7,'Blue')
                        list_of_data.pop(8)

                    list_of_data[-1] = list_of_data[-1].strip('\r\n')
                    pre_portmap_csv_writer.writerow(list_of_data)

    os.remove(f'{hostname} Aps to port.csv')
    os.remove(f'{hostname} interface description with vlans.csv')
    os.remove(f'{hostname} data combined.csv')
    os.remove(f'{hostname} cdp neighbors.txt')
    os.remove(f'{hostname} mac address table.txt')
    os.remove(f'{hostname} running config.txt')

def search_oui_database(filename):
    oui_db = {}
    with open(filename, 'r', encoding='utf-8') as oui_database:
        for i in oui_database:
            if '(base 16)' in i:
                parts = i.split('(base 16)')
                mac_prefix = parts[0].strip()
                vendor = parts[1].strip()
                oui_db[mac_prefix] = vendor
    return oui_db

def mac_lookup(mac_address):
    oui_db = search_oui_database('oui.txt')

    mac_address = mac_address.split('.')
    mac_prefix = ''.join(mac_address)
    mac_prefix = mac_prefix[:6].upper()
    return oui_db.get(mac_prefix, "Vendor not found")

# def vendor_finder(hostname):
    with open(f'{hostname} port to mac address.csv', newline='') as macs:
        with open(f"{hostname} mac and vendor.csv", 'w', newline= '') as switch_info:
            info_csv_writer = csv.writer(switch_info)
            oui_db = search_oui_database('oui.txt')

            mac = []
            mac_add = ''

            for i in macs:
                list_of_i = i.split(',')

                for k in enumerate(list_of_i):

                    if k[0] == 0 or k == "":

                        if "\r\n" in k[1]:
                            inter = k[1].strip('\r\n')
                            switch_info.write(inter)
                        continue

                    vendor = mac_lookup(k[1],oui_db)
                    if list_of_i[0] not in mac:
                        mac.append(list_of_i[0])
                    mac_add = k[1].strip('\r\n')    
                    mac.append(mac_add)
                    mac.append(vendor)
                info_csv_writer.writerow(mac)
                mac = []
    os.remove(f'{hostname} int macs.csv')

def vlan_sheet_maker(hostname): 
    with open(f'{hostname} vlans.txt', newline='') as switch_vlans:
        with open(f'{hostname} usable vlans.txt','w', newline='') as formatted_vlans:

            for vlans in switch_vlans:
                list_of_vlans = vlans.split()
                try:
                    if 'active' in list_of_vlans[2]:
                        vlan = list_of_vlans[0]
                        vlan_name = list_of_vlans[1]
                        formatted_vlans.write(f'Vlan {vlan}\n')
                        formatted_vlans.write(f'Name {vlan_name}\n')

                except IndexError:
                    continue

