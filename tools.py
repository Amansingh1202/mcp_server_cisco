from fastmcp import FastMCP
from netmiko import ConnectHandler

mcp = FastMCP("NetworkAutomation")

router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.223.131",
    "port": 32770,
    "username": "admin",
    "password": "eve",
}

@mcp.tool()
def show_interfaces():

    """
    Show interface summary
    """

    conn = ConnectHandler(**router)

    output = conn.send_command(
        "show ip interface brief"
    )

    conn.disconnect()

    return output


@mcp.tool()
def show_bgp():

    """
    Show BGP summary
    """

    conn = ConnectHandler(**router)

    output = conn.send_command(
        "show ip bgp summary"
    )

    conn.disconnect()

    return output


if __name__ == "__main__":
    mcp.run()