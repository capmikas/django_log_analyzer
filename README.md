Для запуска скрипта:
- Поместить файлы логов в папку logs проекта
- Запустить скрипт без создания файла отчета:
--  python main.py app1.log app3.log app2.log
--  где app1.log app3.log app2.log - названия файлов логов (можно вводить любое количество)
-  Запустить скрипт с созданием файла отчета:
--  main.py app1.log app3.log app2.log --report handler.txt
--  где параметр после --report: имя создаваемого файла
--  файл отчета создается в папке output
