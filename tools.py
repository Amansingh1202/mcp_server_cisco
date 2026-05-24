from fastmcp import FastMCP
from netmiko import ConnectHandler
import json
import sqlite3

mcp = FastMCP("NetworkAutomation")

with open("devices.json") as f:
    DEVICES = json.load(f)

def get_device(device_name):

    if device_name not in DEVICES:
        raise ValueError(f"Device {device_name} not found")

    device = DEVICES[device_name]

    return {
        "device_type": "cisco_ios_telnet",
        "host": device["host"],
        "port": device["port"],
        "username": "admin",
        "password": "eve",
    }

@mcp.tool()
def show_interfaces(device_name: str):

    """
    Show interface summary for a device
    """
    router = get_device(device_name)
    conn = ConnectHandler(**router)
    output = conn.send_command(
        "show ip interface brief"
    )
    conn.disconnect()
    return output

@mcp.tool()
def get_interfaces(device_name: str):
    conn = sqlite3.connect("network.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT interface_name,
           ip_address,
           status,
           protocol
    FROM interfaces
    WHERE device_name = ?
    """, (device_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

@mcp.tool()
def get_interfaces_all():
    conn = sqlite3.connect("network.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT device_name,
           interface_name,
           ip_address,
           status,
           protocol
    FROM interfaces """)
    rows = cursor.fetchall()
    conn.close()
    return rows

@mcp.tool()
def show_bgp(device_name: str):

    """
    Show BGP summary for a device
    """
    router = get_device(device_name)
    conn = ConnectHandler(**router)
    output = conn.send_command(
        "show ip bgp summary"
    )
    conn.disconnect()
    return output


if __name__ == "__main__":
    mcp.run()