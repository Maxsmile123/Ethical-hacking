# Программа для смены MAC адреса  <img align="" src="https://github.com/Maxsmile123/Maxsmile123/blob/333a0368f66c4b37dfefea27ff1833aba50d7ad3/res/hacker.png" height="25px" width="25px"> 
Интерфейс взаимодействия следующий: <br> 
- **-i(--interface)** указывается интерфейс устройства, MAC которого надо изменить.<br>
- **-m(--mac)** указывается новый MAC адрес.  
## Пример использования:
```shell
python3 mac_changer.py -i eth0 -m 1c:5a:b3:41:f2:11
Current MAC - 10:54:13:41:82:11
[+] Changing MAC address for eth0 to 1c:5a:b3:41:f2:11
[+] Changing was successfully! Current MAC - 10:54:13:41:82:11
```


