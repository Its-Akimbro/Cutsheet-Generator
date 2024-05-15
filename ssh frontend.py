from username_password import username,password
import cutsheet_pre_portmapped as pre_mapped
import ssh_functions as ssh
import cutsheet_finisher as finisher

version_to_run = 2

file_name = "ky-lon-sjh-hosp-ac-1374-1f01 pre portmapped.csv".lower()
port_mapped_file = "ky-lon-sjh-hosp-ac-1374-1f01 portmapped.csv".lower()
wap_file = "London ap sheet.csv" 
vlan_file = "London vlan list.txt"

switch_count = 1
switch_details = []     

new_hostname = 'kysjl-main-1374-as1'
new_ip = '10.104.203.36'

legacy_ip_address_list = [
''
]

for ip in legacy_ip_address_list:
    legacy_ip_address = ip

    if version_to_run == 1:
        connection_type = ssh.ssh_or_telnet_conection(legacy_ip_address, username, password)
    
        if connection_type[0] == True:
            hostname = ssh.get_host_name(connection_type)
            ssh.get_interface_status(hostname, connection_type)
            ssh.get_running_config(hostname, connection_type)
            ssh.get_mac_address_table(hostname, connection_type)
            ssh.get_interface_descriptions(hostname, connection_type)
            # ssh.get_switch_vlans(hostname, connection_type)
            ssh.get_cdp_neighbor(hostname, connection_type)
            pre_mapped.int_status_cutsheet_data(hostname, legacy_ip_address)
            pre_mapped.running_config_cutsheet_data(hostname)
            pre_mapped.mac_address_table_cutsheet_data(hostname)
            pre_mapped.interface_description_cutsheet_data(hostname)
            pre_mapped.access_points_to_interface_cutsheet_data(hostname)
            pre_mapped.pre_portmapper(hostname, legacy_ip_address, new_hostname, new_ip)
            pre_mapped.cable_color(hostname)
            print(f'I finished with {legacy_ip_address}')

        if connection_type[0] == False:
            hostname = ssh.get_host_name(connection_type)
            ssh.get_interface_status(hostname, connection_type)
            ssh.get_running_config(hostname, connection_type)
            ssh.get_mac_address_table(hostname, connection_type)
            ssh.get_interface_descriptions(hostname, connection_type)
            # ssh.get_switch_vlans(hostname, connection_type)
            ssh.get_cdp_neighbor(hostname, connection_type)
            pre_mapped.int_status_cutsheet_data(hostname, legacy_ip_address)
            pre_mapped.running_config_cutsheet_data(hostname)
            pre_mapped.mac_address_table_cutsheet_data(hostname)
            pre_mapped.interface_description_cutsheet_data(hostname)
            pre_mapped.access_points_to_interface_cutsheet_data(hostname)
            pre_mapped.pre_portmapper(hostname, legacy_ip_address, new_hostname, new_ip)
            pre_mapped.cable_color(hostname)
            print(f'I finished with {legacy_ip_address}')

    if version_to_run == 2:

        finisher.legacy_switch_name_finder(file_name)
        finisher.new_switch_name_finder(file_name)
        finisher.room_number_finder(file_name)
        finisher.legacy_ip_finder(file_name)

        if switch_count > 1:
            for switch_num in range(switch_count):
                switch_model = "9410"

                if switch_num == 0:
                    filled_blade = "1,2,7,8,9,10"   

                if switch_num == 1:
                    filled_blade = "1,2,7,8,9,10"   

                if switch_model == "9300":
                    for stack_num in range(int(filled_blade)):
                        if stack_num == 0:
                            filled_blade = f"{stack_num+1},"
                        else:
                            filled_blade += f"{stack_num+1},"   
                    filled_blade = filled_blade[:-1]

                filled_blades = {int(i):1 for i in filled_blade.split(",") if i.isnumeric()}
                filled_blades[1] += 1
                switch = finisher.new_switch(switch_model,filled_blades)
                switch_details.append(switch)

        elif switch_count == 1:
            switch_model = "9410"                     
            filled_blade = "1,2,7,8,9,10"

            if switch_model == "9300":
                for stack_num in range(int(filled_blade)):
                    if stack_num == 0:
                        filled_blade = f"{stack_num+1},"
                    else:
                        filled_blade += f"{stack_num+1},"
                filled_blade = filled_blade[:-1]

            filled_blades = {int(i):1 for i in filled_blade.split(",") if i.isnumeric()}
            filled_blades[1] += 1
            switch = finisher.new_switch(switch_model,filled_blades)
            switch_details.append(switch)

        if wap_file != '':
            max_port = finisher.max_port_finder(wap_file, switch_count)

        else:
            max_port = 36

        finisher.port_mapping_file_info_to_cutsheet(file_name, port_mapped_file,switch_count,filled_blade)
        finisher.new_switch_port_adder(switch_details,max_port,file_name)
        finisher.idf_config(vlan_file,switch_details)
        finisher.wap_vlan_finder(vlan_file)
        finisher.wap_sheet(wap_file,switch_details)
        finisher.add_wap_to_idf(switch_details)
        finisher.excel_workbook_maker()


    if version_to_run == 3:
        connection_type = ssh.ssh_or_telnet_conection(legacy_ip_address, username, password)
        hostname = ssh.get_host_name(connection_type)
        ssh.get_running_config(hostname, connection_type)
        print(f'I finished with {legacy_ip_address}')

    if version_to_run == 4:
        connection_type = ssh.ssh_or_telnet_conection(legacy_ip_address, username, password)
        hostname = ssh.get_host_name(connection_type)
        ssh.get_spanning_tree_details(hostname, connection_type)
        print(f'I finished with {legacy_ip_address}')

    if version_to_run == 5:
        connection_type = ssh.ssh_or_telnet_conection(legacy_ip_address, username, password)
        hostname = ssh.get_host_name(connection_type)
        ssh.get_switch_vlans(hostname, connection_type)
        print(f'I finished with {legacy_ip_address}')


print(f'\nFinished with all ips')