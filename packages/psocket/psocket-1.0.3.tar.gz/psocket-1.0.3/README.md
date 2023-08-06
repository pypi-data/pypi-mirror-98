[![PyPI version](https://badge.fury.io/py/psocket.svg)](https://badge.fury.io/py/psocket)
[![Build Status](https://travis-ci.org/c-pher/PSocket.svg?branch=master)](https://travis-ci.org/c-pher/PSocket)
[![Coverage Status](https://coveralls.io/repos/github/c-pher/PSocket/badge.svg?branch=master)](https://coveralls.io/github/c-pher/PSocket?branch=master)


# PSocket
The cross-platform simple tool to work with remote server through sockets. 
It can establish socket connection to a remote host:port, send commands and receive response.
No need to send byte-string. Use usual strings to send command.

## Installation
For most users, the recommended method to install is via pip:
```cmd
pip install psocket
```

or from source:

```cmd
python setup.py install
```

## Import
```python
from psocket import SocketClient
```
---
## Usage
```python
from psocket import SocketClient

client = SocketClient(host='172.16.0.48', port=3261)
print(client)
```
```python
from psocket import SocketClient

client = SocketClient(host='172.16.0.48', port=3261)
print(client.send_command('<commands>'))
```

---

## Changelog

##### 1.0.3 (12.03.2021)

- Added ability to disable logs
- "timeout connection" added as parameter with None default value

##### 1.0.2 (15.01.2020)

Added "initialize" param to the constructor

##### 1.0.1 (15.01.2020)

- "is_host_available()" renamed to "is_socket_available()" and updated
- used external logger from "plogger" package

##### 1.0.0a4 (15.01.2020)
- added init docstring
- init notation changed:
  - host is string
  - port is integer

##### 1.0.0a3 (14.01.2020)
- removed timeout from socket connection
- greeting and socket_response now are private methods

##### 1.0.0a2 (13.01.2020)
Reverted "client". Now it is an attribute again to keep session alive 

##### 1.0.0a1 (13.01.2020)
- Now connection creates with client property
- New methods added:
    - is_host_available() 
    - get_sock_name()
    - get_peer_name()

##### 1.0.0a0 (13.01.2020)
- initial commit
