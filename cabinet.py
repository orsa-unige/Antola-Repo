#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telnetlib

def ask(message=None):
    """
    Connect to the cabinet and ask simultaneously 
    RA2000, DEC2000, ALT, AZ, LST, UTC.
    Answer is given as a dict of decimal numbers. 
    UTC is given as unix time.

    Returns: these values in a dictionary.
    """
    
    # Login data for cabinet communication.
    # It is a byte-string.
    auth = b'auth plain "admin" "admin"\n'

    if not message:
        # Message to retrieve coordinates and time using the
        # same cabinet call. It is a byte-string.
        msg = b'''1 get POSITION.EQUATORIAL.RA_J2000
        2 get POSITION.EQUATORIAL.DEC_J2000
        3 get POSITION.HORIZONTAL.alt
        4 get POSITION.HORIZONTAL.az
        5 get POSITION.LOCAL.SIDEREAL_TIME
        6 get POSITION.LOCAL.UTC\n'''
    else:
        msg = bytes(message+"\n", "utf+8")
        
    # Connect to the cabinet.
    tn = telnetlib.Telnet("grigioni",65432)
    tn.read_until(b"[ruder]\n")
    tn.write(auth)
    tn.read_until(b"AUTH OK 0 0\n")
    
    # Send the message.
    tn.write(msg)

    # For each command, the *asyncrhronous* answer contains: 
    #
    # COMMAND OK
    # DATA INLINE ...
    # COMMAND COMPLETE
    #
    # Append all the buffer line by line to a list.
    
    tn_answer = []
    for i in range(msg.count(b"\n")*3-1):
        tn_answer.append(tn.read_until(b"\n"))

    # Close the cabinet connection.
    tn.close()

    # Keep only the data.
    tn_values = [s for s in tn_answer if b"DATA INLINE" in s]

    # Create a python dictionary with name and value.
    telnet_dict = dict([m[14:-1].decode().split("=") for m in tn_values])

    # Transform values to float.
    for k,v in telnet_dict.items():
        telnet_dict[k] = float(v)

    if not message:
        # Use decent keys in dictionary.
        simple_dict = {
            "ra" : telnet_dict["POSITION.EQUATORIAL.RA_J2000"],
            "dec" : telnet_dict["POSITION.EQUATORIAL.DEC_J2000"],
            "alt" : telnet_dict["POSITION.HORIZONTAL.ALT"],
            "az" : telnet_dict["POSITION.HORIZONTAL.AZ"],
            "lst" : telnet_dict["POSITION.LOCAL.SIDEREAL_TIME"],
            "utc" : telnet_dict["POSITION.LOCAL.UTC"],
        }
    else:
        simple_dict = telnet_dict
        
    return(simple_dict)



if __name__ == "__main__":

    ask()
