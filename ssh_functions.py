import paramiko
import telnetlib
import time

def ssh_or_telnet_conection(legacy_ip_address, username, password):
    try:
        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(legacy_ip_address, username=username, password=password, look_for_keys=False)

        shell = ssh.invoke_shell()
        shell.send("terminal length 0\n")
        return True, shell
    
    except:
        tn = telnetlib.Telnet(legacy_ip_address, port=23)

        tn.write(username.encode('ascii') + b'\n')
        tn.write(password.encode('ascii') + b'\n')
        tn.write(b"terminal length 0\n")
        time.sleep(5)

        return False, tn
    
def get_host_name(connection_type):

    #ssh connection
    if connection_type[0] == True:
        time.sleep(10)
        output = connection_type[1].recv(65535).decode().split()
        hostname = output[-1][:-1].lower()

    #telnet connection
    if connection_type[0] == False:
        time.sleep(10)
        output = connection_type[1].read_very_eager().decode('ascii').split()
        hostname = output[-1][:-1].lower()

    return hostname    

def get_interface_status(hostname, connection_type):

    #ssh connection
    if connection_type[0] == True:
        with open(f'{hostname} interface status.txt', 'w', newline='') as raw_int_status:

            connection_type[1].send("show interface status\n")
            time.sleep(1) 

            timeout = 10
            start_time = time.time()
            output = ""

            while time.time() - start_time < timeout:
                if connection_type[1].recv_ready():
                    page_output = connection_type[1].recv(65535).decode()
                    output += page_output
                time.sleep(1)

            raw_int_status.write(output)

    #telnet connection
    if connection_type[0] == False:
        with open(f'{hostname} interface status.txt', 'w', newline='') as raw_int_status:

            connection_type[1].write(b"show interface status\n")
            time.sleep(15)  

            raw_int_status.write(connection_type[1].read_very_eager().decode('ascii'))

def get_running_config(hostname, connection_type):

    #ssh connection
    if connection_type[0] == True:
        with open(f'{hostname} running config.txt', 'w', newline='') as running_config:
            connection_type[1].send("show run\n")
            time.sleep(15) 

            timeout = 10
            start_time = time.time()
            output = ""

            while time.time() - start_time < timeout:
                if connection_type[1].recv_ready():
                    page_output = connection_type[1].recv(65535).decode()
                    output += page_output
                time.sleep(1)

            running_config.write(output)

    #telnet connection
    if connection_type[0] == False:
        with open(f'{hostname} running config.txt', 'w', newline='') as running_config:
            connection_type[1].write(b"show run\n")
            time.sleep(45)  

            running_config.write(connection_type[1].read_very_eager().decode('ascii'))

def get_mac_address_table(hostname, connection_type):

    if connection_type[0] == True:
        with open(f'{hostname} mac address table.txt', 'w', newline='') as mac_table:

            connection_type[1].send("show mac address-table\n")
            time.sleep(1) 

            timeout = 10
            start_time = time.time()
            output = ""

            while time.time() - start_time < timeout:
                if connection_type[1].recv_ready():
                    page_output = connection_type[1].recv(65535).decode()
                    output += page_output
                time.sleep(1)

            mac_table.write(output)

    #telnet connection
    if connection_type[0] == False:
        with open(f'{hostname} mac address table.txt', 'w', newline='') as mac_table:

    
            connection_type[1].write(b"show mac address-table\n")
            time.sleep(15)  

            mac_table.write(connection_type[1].read_very_eager().decode('ascii'))

def get_interface_descriptions(hostname, connection_type):

    if connection_type[0] == True:
        with open(f'{hostname} interface descriptions.txt', 'w', newline='') as interface_description:

            connection_type[1].send("show interface description\n")
            time.sleep(1) 

            timeout = 10
            start_time = time.time()
            output = ""

            while time.time() - start_time < timeout:
                if connection_type[1].recv_ready():
                    page_output = connection_type[1].recv(65535).decode()
                    output += page_output
                time.sleep(1)

            interface_description.write(output)

    #telnet connection
    if connection_type[0] == False:
        with open(f'{hostname} interface descriptions.txt', 'w', newline='') as interface_description:

            connection_type[1].write(b"show interface description\n")
            time.sleep(5)  

            interface_description.write(connection_type[1].read_very_eager().decode('ascii'))

def get_switch_vlans(hostname, connection_type):

    if connection_type[0] == True:
        with open(f'{hostname} vlans.txt', 'w', newline='') as switch_vlans:

            connection_type[1].send("show vlan\n")
            time.sleep(1) 

            timeout = 10
            start_time = time.time()
            output = ""

            while time.time() - start_time < timeout:
                if connection_type[1].recv_ready():
                    page_output = connection_type[1].recv(65535).decode()
                    output += page_output
                time.sleep(1)

            switch_vlans.write(output)

    #telnet connection
    if connection_type[0] == False:
        with open(f'{hostname} vlans.txt', 'w', newline='') as switch_vlans:

            connection_type[1].write(b"show vlan\n")
            time.sleep(5)  

            switch_vlans.write(connection_type[1].read_very_eager().decode('ascii'))

def get_cdp_neighbor(hostname, connection_type):
    if connection_type[0] == True:
        with open(f'{hostname} cdp neighbors.txt', 'w', newline='') as cdp_neighbor:

            connection_type[1].send("show cdp neighbors\n")
            time.sleep(1) 

            timeout = 10
            start_time = time.time()
            output = ""

            while time.time() - start_time < timeout:
                if connection_type[1].recv_ready():
                    page_output = connection_type[1].recv(65535).decode()
                    output += page_output
                time.sleep(1)

            cdp_neighbor.write(output)

    #telnet connection
    if connection_type[0] == False:
        with open(f'{hostname} cdp neighbors.txt', 'w', newline='') as cdp_neighbor:

            connection_type[1].write(b"show cdp neighbors\n")
            time.sleep(5)  

            cdp_neighbor.write(connection_type[1].read_very_eager().decode('ascii'))

def get_spanning_tree_details(hostname, connection_type):
    if connection_type[0] == True:
        with open(f'{hostname} spanning-tree details.txt', 'w', newline='') as spanning_tree:

            connection_type[1].send(" sh span \n")
            time.sleep(1) 

            timeout = 10
            start_time = time.time()
            output = ""

            while time.time() - start_time < timeout:
                if connection_type[1].recv_ready():
                    page_output = connection_type[1].recv(65535).decode()
                    output += page_output
                time.sleep(1)

            spanning_tree.write(output)

    #telnet connection
    if connection_type[0] == False:
        with open(f'{hostname} spanning-tree details.txt', 'w', newline='') as spanning_tree:

            connection_type[1].write(b" sh span root\n")
            time.sleep(5)  

            spanning_tree.write(connection_type[1].read_very_eager().decode('ascii'))

