# Домашняя работа по занятию "10.06. Инцидент-менеджмент"

> ## Задание 1
> Составьте постмотрем, на основе реального сбоя системы Github в 2018 году.

### Краткое описание инцендента
Вечером 21 октября в ходе плановых работ на сетевом оборудовании был потерян кворум в кластерах баз данных, в которых 
хранились метаданные GitHub-сервисов. В ходе автоматического восстановления произошла рассинхронизация нод кластеров, 
потребовавшая ручного восстановления данных. Сбой затронул базы данных в датацентрах на Восточном и Западном побережье 
США, вследствие чего часть сервисов (вебхуки, GitHub Pages) оказалась недоступной на время восстановления.

### Предшествующие события
Плановые работы на сетевом оборудовании, приведшие 21 октября в 22:52 UTC к 43-секундной потери сетевой связности между
сетевым узлом на Восточном побережье с главным датацентром на Восточном побережье США.

### Причина инцидента
В следствие потери сетевой связности программное обеспечение оркестрации инициировало отставку (как это по-русски, 
step-down, deselection) нод-лидеров кластеров БД, и выборов новых на основе сетевого кворума по протоколу RAFT. Новые 
лидеры были выбраны в датацентре на Западном побережье США. Часть данных успела быть записаной в лидеры  
на Восточном побережье, и не была среплицированна на вновь избранные в Западном ДЦ, что помешало возвращению лидеров в 
Восточный ДЦ.

### Воздействие
Сложившаяся после сетевого сбоя топология баз данных оказалась непредусмотренной для сервисов, и привела к деградации 
качества обслуживания из-за возросшей задержки запросов к БД.
Для предотвращения потери данных пришлось остановить запись новых метаданных в базы данных, и такие сервисы как вебхуки
и сборка GitHub Pages оказались недоступными для пользователей.

### Обнаружение
В 21 октября 22:54 UTC внутренний мониторинг начал создавать алерты, показывающие многочисленные сбои систем. 

### Реакция
Над сортировкой и обработкой входящих уведомлений работали несколько инженеров первой группы реагирования. В 23:11 к 
работе присоеденился координатор инцедента. В 23:13 так же были привлечены дополнительные инженеры из группы разработки
баз данных. Оповещение пользователей происходило в Твиттере и блоге компании.

### Восстановление
Сервисы, записывающие новые метаданные, были приостановлены. Была проведена работа по восстановлению данных из бакапов с 
последующей синхронизацией изменений, переносу лидеров кластеров БД обратно в Восточный ДЦ, и обработка скопившихся
событий от вебхуков и сборки GitHub Pages. 

### Таймлайн
21.10.2018, 22:52 UTC сетевой сбой, ПО оркестрации начало перестроение топологии кластеров БД  
21.10.2018, 22:54 UTC мониторинг начал присылать оповещения о множественных неисправностях  
21.10.2018, 23:02 UTC инженеры определили некорректную топологию кластеров БД  
21.10.2018, 23:07 UTC группа реагирования остановила внутренние средства деплоймента для предотвращения дальнейших изменений.  
21.10.2018, 23:09 UTC был установлен желтый статус работоспособности сайта  
21.10.2018, 23:11 UTC к работе присоеденился координатор инцедента, статус был изменён на красный.   
21.10.2018, 23:13 UTC привлечены дополнительные инженеры из группы разработки БД, анализ ситуации  
21.10.2018, 23:19 UTC остановлены сервисы, записывающие новые метаданные  
22.10.2018, 00:05 UTC разработка плана восстановления, обновление статуса инцедента  
22.10.2018, 00:41 UTC начато восстановление баз данных из резервных копий  
22.10.2018, 06:51 UTC несколько кластеров в Восточном ДЦ завершили восстановление из бакапов, начата синхронизация новых 
данных с Западного ДЦ  
22.10.2018, 07:46 UTC публикация поста в корпоративном блоге с подробностями инцедента  
22.10.2018, 11:12 UTC все лидеры кластеров баз данных были перенесены в Восточный ДЦ  
22.10.2018, 13:15 UTC разворачивание дополнительных реплик чтения для ускорения синхронизации данных.  
22.10.2018, 16:24 UTC синхронизация данных закончена, возврат к оригинальной топологии, устранивший проблемы с 
латентностью и доступностью сервисов. Начало обработки накопившейся очереди событий.  
22.10.2018, 16:45 UTC решение проблем и оптимизация обработки накопившейся очереди событий  
22.10.2018, 23:03 UTC все события из накопившейся очереди были обработаны, подтверждена целостность и правильная работа 
всех систем. Статус сайта был обновлён на зелёный.  

### Последующие действия
Несинхронизированные записи в базы данных, оставшиеся в ходе перестройки топологии кластеров в датацентре на Восточном 
побережье, потребовали дополнительной ручной обработки.  
Конфигурация ПО оркестрации будет изменена, чтобы предотвратить перемещение лидеров кластеров БД в другие регионы.  
Будет пересмотрена система оповещения пользователей, выбрана новая площадка для обсуждения, статусы будут отображаться 
для отдельных компонентов платформы.  
Будет реализован проект по увеличению отказоусточивости обработки трафика, позволяющий выдержать отказ любого датацентра 
без ручного вмешательства.  
Будет начата систематическая практика проверки сценариев сбоя перед тем, как они случатся, включая методы преднамеренных 
сбоев и хаос-инженеринга.
