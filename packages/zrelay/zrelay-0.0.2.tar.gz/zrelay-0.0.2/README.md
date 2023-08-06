# Zrelay  HAT
Zrelay HAT is a 3 Relay module without utilizing any of the raspberry pi zero's GPIO pins.

Installation guide for ZRelay 
<!-- This is the command to control [4-Relay Stackable Card for Raspberry Pi]-->

<!-- ## Install
Don't forget to enable I2C communication:
```bash
~$ sudo raspi-config
``` -->

## Install

```bash
~$ sudo apt-get update
~$ sudo apt-get install build-essential python-pip python-dev python-smbus git
# ~$ git clone https://github.com/SequentMicrosystems/4relay-rpi.git
~$ sudo python setup.py install
```

## Update

```bash
~$ git pull
~$ sudo python setup.py install
```

## Usage

```bash
~$ python3
Python 3.5.3 (default, Sep 27 2018, 17:25:39)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import zrelay
>>> zrelay.set_zrelay_state(0, 1, 1)
0
>>>
```

## Functions

### set_zrelay_state(stack_level , relay_num , state)
Set state of any one relay at a time.

stack_level -   stack level can be selected from selecting address jumpers. Stack can be between 0 to 7.

relay_num   -    Can be from 1 to 3 for each stack.

state       -   1: turn ON, 
                0: turn OFF

Function will raise ValueError if stack_level is not between 0 to 7 and relay_num not between 1 to 3.

eg. 
<!-- To turn ON relay 2 of stack 1 (i2C address- 19) -->
    >>> set_zrelay_state(1, 2, 1)


### set_all_zrelay_state(stack_level, state)
Set all relays state of a stack.

stack_level -   stack level can be selected from selecting address jumpers. Stack can be between 0 to 7.

state       -   1: turn ON, 
                0: turn OFF

Function will raise ValueError if stack_level is not between 0 to 7.

eg. 
<!-- To turn ON all relays of stack 1 (i2C address- 19) -->
    >>> set_zrelay_state(1, 2, 1)

### get_zrelay_state(stack_level, relay_num)
Get state of any one relay at a time.

stack_level -   stack level can be selected from selecting address jumpers. Stack can be between 0 to 7.

relay_num   -    Can be from 1 to 3 for each stack.

Function will return 0 if specified relay is OFF and 1 if relay is ON.

It will raise ValueError if stack_level is not between 0 to 7 and relay_num not between 1 to 3.

eg. 
<!-- To get state of relay 2 of stack 1 (i2C address- 19) -->
    >>> get_zrelay_state(1, 2)
        1 

### get_all_zrelay_state(stack_level)
Get all relays state of a stack.

stack_level -   stack level can be selected from selecting address jumpers. Stack can be between 0 to 7.

Function will return 3 bit string value, each bit representing ON/OFF state of that particular relay. Relay numbers are from Right to Left, where Relay 1 is the MSB.

It will raise ValueError if stack_level is not between 0 to 7.

eg. 
<!-- To get state of stack 1 (i2C address- 19) -->
    >>> get_all_zrelay_state(1)
        '101' 
