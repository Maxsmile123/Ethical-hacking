# Программа ARP spoofing (атака Man in the middle - MITM)  
Программа изменяет ARP таблицы для роутера и компьютера жертвы, делая нас "человеком по середине".   
При выходе из программы, происходит восстановаление изначальных ARP таблиц.   
# Взаимодействие
Интерфейс взаимодействия следующий: через -v(--ipvictim) указывается   
IP адрес устройства жертвы, а через -h(--iphost) указывается IP устройства, за которое нас будет принимать жертва (роутер)
