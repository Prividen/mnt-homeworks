# Домашняя работа по занятию "10.01. Зачем и что нужно мониторить"

> 1. Вас пригласили настроить мониторинг на проект. На онбординге вам рассказали, что проект представляет из себя 
платформу для вычислений с выдачей текстовых отчетов, которые сохраняются на диск. Взаимодействие с платформой 
осуществляется по протоколу http. Также вам отметили, что вычисления загружают ЦПУ. Какой минимальный набор метрик вы
выведите в мониторинг и почему?

Наш проект потребляет ресурсы: CPU, память, сеть, диск. Минимальные метрики могут быть примерно такие:
- CPU: usage (MHz/%), load average (эта метрика не только про CPU, но отнесём сюда).
Учитывая интенсивность вычислений, можно мониторить поподробней (user/system/iowait/idle), 
общую загрузку и в разрезе каждого процессора, возможно у нас что-то в одно ядро упирается. А так же L1/L2/L3 кеши - %попаданий, промахов.

- Memory: consumed/free, swap (если мы его зачем-то используем), для интенсивности использования можно посмотреть pages per second. 

- Network: utilization % (справляется ли наша сеть), throughput (сколько денег должны провайдеру), 
packets per second / TCP connections (не DDoSят ли нас). Для http: общее количество запросов, из них 
ошибок. Возможно, детализация по методам запросов (GET, PUT, etc). Время выполнения запросов. Общая доступность сервиса.

- Диск: доступность ресурсов - free space, free inodes. Утилизация: usage %, throughput, IOPS. 

---
> 2. Менеджер продукта посмотрев на ваши метрики сказал, что ему непонятно что такое RAM/inodes/CPUla. Также он сказал, 
что хочет понимать, насколько мы выполняем свои обязанности перед клиентами и какое качество обслуживания. Что вы 
можете ему предложить?

SLO/SLA он и сам должен уже знать. А мы ему можем предоставить показатели SLI (Service Level Indicators) - % времени, 
когда наша система работает нормально и удовлетворяет наших клиентов - например, общая доступность сервиса и доля 
безошибочных ответов HTTP.  
Так же можно предоставить какие-то дополнительные бизнес-метрики для статистики - количество вычислений всего, по пользователю, 
количество формируемых/запрашиваемых отчётов. 

---
> 3. Вашей DevOps команде в этом году не выделили финансирование на построение системы сбора логов. Разработчики в свою 
очередь хотят видеть все ошибки, которые выдают их приложения. Какое решение вы можете предпринять в этой ситуации, 
чтобы разработчики получали ошибки приложения?

Можно использовать систему перехвата ошибок, например Sentry

---
> 4. Вы, как опытный SRE, сделали мониторинг, куда вывели отображения выполнения SLA=99% по http кодам ответов. 
Вычисляете этот параметр по следующей формуле: summ_2xx_requests/summ_all_requests. Данный параметр не поднимается выше 
70%, но при этом в вашей системе нет кодов ответа 5xx и 4xx. Где у вас ошибка?

Мы, как опытный SRE, забыли про 3xx коды.  
Т.е. более правильная формула - `(summ_2xx_requests + summ_3xx_requests)/summ_all_requests`

---
> ### Дополнительное задание (со звездочкой*) - необязательно к выполнению
> Вы устроились на работу в стартап. На данный момент у вас нет возможности развернуть полноценную систему 
мониторинга, и вы решили самостоятельно написать простой python3-скрипт для сбора основных метрик сервера. Вы, как 
опытный системный-администратор, знаете, что системная информация сервера лежит в директории `/proc`. 
Также, вы знаете, что в системе Linux есть  планировщик задач cron, который может запускать задачи по расписанию.
> Для успешного выполнения задания нужно привести:

> а) работающий код python3-скрипта,

[Скрипт](monitoring_eco_bio_homemade_GMO-free.py)

> б) конфигурацию cron-расписания,

```
# cat /etc/cron.d/monitoring 
*/1 * * * * root /home/mak/netology/homeworks/mnt-homeworks/10-monitoring-01-base/monitoring_eco_bio_homemade_GMO-free.py
```

в) пример верно сформированного 'YY-MM-DD-awesome-monitoring.log', имеющий не менее 5 записей,

`/var/log/21-10-31-awesome-monitoring.log`:
```json lines
{"Timestamp": 1635634201, "CPU usage %": 24.7, "Load Average last minute": 1.41, "CPU Temperature": {"Physical id 0": 49.0, "Core 0": 38.0, "Core 1": 41.0, "Core 2": 50.0, "Core 3": 37.0}, "Memory usage %": 69.8, "Swap usage %": 1.5, "Disk usage %": {"/": 86.3, "/var": 67.8, "/opt": 67.8, "/home": 77.0}, "Network": {"Bytes sent": 533471115211, "Bytes received": 427697805286, "Packets sent": 893432934, "Packets received": 1650772326}}
{"Timestamp": 1635634261, "CPU usage %": 12.5, "Load Average last minute": 1.73, "CPU Temperature": {"Physical id 0": 44.0, "Core 0": 38.0, "Core 1": 42.0, "Core 2": 44.0, "Core 3": 35.0}, "Memory usage %": 69.8, "Swap usage %": 1.5, "Disk usage %": {"/": 86.3, "/var": 67.8, "/opt": 67.8, "/home": 77.0}, "Network": {"Bytes sent": 537255405022, "Bytes received": 427784151617, "Packets sent": 896202377, "Packets received": 1651638094}}
{"Timestamp": 1635634321, "CPU usage %": 11.2, "Load Average last minute": 1.83, "CPU Temperature": {"Physical id 0": 44.0, "Core 0": 38.0, "Core 1": 42.0, "Core 2": 44.0, "Core 3": 35.0}, "Memory usage %": 69.6, "Swap usage %": 1.5, "Disk usage %": {"/": 86.3, "/var": 67.8, "/opt": 67.8, "/home": 77.0}, "Network": {"Bytes sent": 541029309899, "Bytes received": 427867993482, "Packets sent": 898964014, "Packets received": 1652498615}}
{"Timestamp": 1635634381, "CPU usage %": 23.8, "Load Average last minute": 1.59, "CPU Temperature": {"Physical id 0": 48.0, "Core 0": 40.0, "Core 1": 41.0, "Core 2": 49.0, "Core 3": 37.0}, "Memory usage %": 69.6, "Swap usage %": 1.5, "Disk usage %": {"/": 86.3, "/var": 67.8, "/opt": 67.8, "/home": 77.0}, "Network": {"Bytes sent": 544802759789, "Bytes received": 427951004237, "Packets sent": 901725004, "Packets received": 1653358299}}
{"Timestamp": 1635634441, "CPU usage %": 28.2, "Load Average last minute": 2.14, "CPU Temperature": {"Physical id 0": 44.0, "Core 0": 43.0, "Core 1": 43.0, "Core 2": 45.0, "Core 3": 36.0}, "Memory usage %": 69.9, "Swap usage %": 1.5, "Disk usage %": {"/": 86.3, "/var": 67.8, "/opt": 67.8, "/home": 77.0}, "Network": {"Bytes sent": 548595611086, "Bytes received": 428036796263, "Packets sent": 904505044, "Packets received": 1654223235}}
{"Timestamp": 1635634501, "CPU usage %": 45.0, "Load Average last minute": 2.44, "CPU Temperature": {"Physical id 0": 48.0, "Core 0": 43.0, "Core 1": 44.0, "Core 2": 48.0, "Core 3": 42.0}, "Memory usage %": 70.6, "Swap usage %": 1.5, "Disk usage %": {"/": 86.3, "/var": 67.8, "/opt": 67.8, "/home": 77.0}, "Network": {"Bytes sent": 552298526133, "Bytes received": 428123472813, "Packets sent": 907218848, "Packets received": 1655079442}}
{"Timestamp": 1635634561, "CPU usage %": 25.3, "Load Average last minute": 2.71, "CPU Temperature": {"Physical id 0": 45.0, "Core 0": 42.0, "Core 1": 42.0, "Core 2": 46.0, "Core 3": 39.0}, "Memory usage %": 69.8, "Swap usage %": 1.5, "Disk usage %": {"/": 86.3, "/var": 67.8, "/opt": 67.8, "/home": 77.0}, "Network": {"Bytes sent": 556267909591, "Bytes received": 428211582749, "Packets sent": 910129651, "Packets received": 1655970960}}
{"Timestamp": 1635634621, "CPU usage %": 32.5, "Load Average last minute": 2.52, "CPU Temperature": {"Physical id 0": 49.0, "Core 0": 41.0, "Core 1": 44.0, "Core 2": 49.0, "Core 3": 37.0}, "Memory usage %": 70.5, "Swap usage %": 1.5, "Disk usage %": {"/": 86.3, "/var": 67.8, "/opt": 67.8, "/home": 77.0}, "Network": {"Bytes sent": 560085557415, "Bytes received": 428296472316, "Packets sent": 912926201, "Packets received": 1656825673}}
```

```json
{
  "Timestamp": 1635634801,
  "CPU usage %": 11.2,
  "Load Average last minute": 2.2,
  "CPU Temperature": {
    "Physical id 0": 47,
    "Core 0": 39,
    "Core 1": 41,
    "Core 2": 47,
    "Core 3": 37
  },
  "Memory usage %": 70.2,
  "Swap usage %": 1.5,
  "Disk usage %": {
    "/": 86.3,
    "/var": 67.8,
    "/opt": 67.8,
    "/home": 77
  },
  "Network": {
    "Bytes sent": 571253426746,
    "Bytes received": 428563095881,
    "Packets sent": 921111624,
    "Packets received": 1659385491
  }
}
```
