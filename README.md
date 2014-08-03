ovpn_win_plaintext_auth
=======================

OpenVPN plain text authentication add-on for Windows that allows OpenVPN road-warrior configuration authenticate user using a plain text file to store username and password.

##What does this add-on provide?
- Ability to authenticate using plain text under Windows environment (good for setup quick VPN config on Windows server, specially on AWS EC2 instance)
- logging on the log directory under OpenVPN installation directory that captures success and failure login attempts

Test environment:
- Windows 2008 R2 64-bit data center edition (AWS EC2 instance)
- Python 2.7.8 X86-64 (for compile only)
- py2exe-0.6.9.win64-py2.7.amd64 (for compile only)
- openvpn-install-2.3.4-I002-x86_64
- OpenVPN third-party add-on is set to use via-file to capture user input

##Usage:

- Create a directory on C drive (example: c:\ovpn-auth)
- Copy the content of *dist* directory to c:\ovpn-auth
- Add the ovpn directory to the Windows environment path
- Install OpenVPN for windows using the default install option
- Create a text file `credentials.txt` in OpenVPN config directory
- Edit the server OpenVPN configuration file to allow authenticate using third-party add-on

###NOTE:
Python and py2exe are not required to be installed to run this add-on.

##Details:

**credentials.txt** example:

`"john.doe mypass123"`

Accepted separator for credential file: space and tab.

**server.ovpn** example:

```
# insert this at the end of your openvpn server config
script-security 3
auth-user-pass-verify 'c:\\ovpn-auth\\plainTextAuth.exe' via-file
```

Read more on OpenVPN to understand the difference between via-file and via-env.

**To build this add-on**, download py2exe from py2exe.org and follow the instruction how to compile python code into exe binary.

For the impatient:
- Modify plainTextAuth.py to match your need
- Download the setup.py from this repo
- Install py2exe
- Run "python setup.py py2exe"
- Wait until the binary is compiled and saved in dist directory
