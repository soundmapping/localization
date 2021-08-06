import argparse
import re

'''
Returns a list of IP address strings
Input:
- string s - String of text
Output:
- list ip_list - containing IP addresses

Source:
https://stackoverflow.com/questions/2890896/how-to-extract-an-ip-address-from-an-html-string
'''
def getIPFromString(s) :
    ip_list = re.findall( r'[0-9]+(?:\.[0-9]+){3}', s)
    return ip_list

def main() :
    parser = argparse.ArgumentParser(description="Returning Latest IP Address from Pi's Log File")
    parser.add_argument('--log_file', default='', type=str, help="Log File")
    # IP_FILE_loc = "/Users/odas2/Google Drive/My Drive/ODAS"
    # IP_FILE_loc = IP_FILE_loc + "/IP3.log"

    args = parser.parse_args()
    state = {k: v for k, v in args._get_kwargs()}

    IP_FILE_loc = args.log_file
    f = open(IP_FILE_loc, "r")

    file_string = f.read()
    file_string = file_string.split("\n")
    latest_log = file_string[-2]

    # print("latest_log = ", latest_log) # For Debugging
    latest_ip = getIPFromString(latest_log)[0] # Access 1st IP Address
    print(latest_ip)

if __name__ == "__main__" :
    # https://docs.python.org/3/library/__main__.html
    # Execute only if run as script
    main()

# ignore
# def main() :
#     parser = argparse.ArgumentParser(description="Returning Latest IP Address from Pi's Log File")
#     parser.add_argument('--pi_num', default=0, type=int, help="Raspberry Pi ID Number")
#     parser.add_argument('--log_dir', default='', type=str, help="Log File location")
#     # IP_FILE_loc = "/Users/odas2/Google Drive/My Drive/ODAS"
#     # IP_FILE_loc = IP_FILE_loc + "/IP3.log"

#     args = parser.parse_args()
#     state = {k: v for k, v in args._get_kwargs()}

#     IP_FILE_loc = args.log_dir + "/IP" + str(args.pi_num) + ".log"
#     f = open(IP_FILE_loc, "r")

#     file_string = f.read()
#     file_string = file_string.split("\n")
#     latest_log = file_string[-3]

#     # print("latest_log = ", latest_log) # For Debugging
#     latest_ip = getIPFromString(latest_log)[0] # Access 1st IP Address
#     print(latest_ip)