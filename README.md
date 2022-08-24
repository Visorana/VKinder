# VKinder

### **VKinder** - бот-программа для поиска партнера в социальной сети Вконтакте. Бот умеет реагировать на входящие сообщения от пользователей, анализировать предпочтения (возраст, пол, город), искать подходящие кандидатуры и отправлять их пользователю вместе с самыми популярными фотографиями. Потенциальных партнеров можно добавлять в список избранных и удалять оттуда. Для работы программы понадобится база данных.

------

## Как начать пользоваться?

### 1. Скачайте код

Скопируйте все файлы из репозитория в вашу среду разработки. Например, PyCharm.

### 2. Установите библиотеки

Установите на свой компьютер библиотеки, которые находятся в файле requirements.txt

### 3. Получите токены и свой ID сообщества

Для запуска программы необходимы 2 ключа доступа: ключ доступа пользователя и ключ доступа сообщества, с которого будет осуществляться общение с пользователями. Также нам понадобится идентификатор сообщества.

Откройте файл config.ini. Поменяйте значения USER_TOKEN, GROUP_TOKEN и GROUP_ID.

```
[VK]
USER_TOKEN=hLxHErTE5pGQ-Llke3d6swVQ #Вставьте ключ доступа пользователя
GROUP_TOKEN=MqnsnNiOVVl17A_lAVqEtgaFgSn #Вставьте ключ доступа сообщества
GROUP_ID=645274 #Вставьте идентификатор группы
```

<details>
  <summary> Как получить ключ доступа пользователя</summary>
  
  1. Перейдите в среду разработчиков VK по ссылке https://dev.vk.com/
  2. Создайте приложение
  ![image](https://i.imgur.com/se4MzlZ.png)
  3. Укажите название сообщества и выберете «Standalone-приложение»
  ![image](https://i.imgur.com/oEF0tmM.png)
  4. Перейдите в настройки, включите Open API
  ![image](https://i.imgur.com/HUgE8OF.png)
  5. В поле «Адрес сайта» введите http://localhost
  ![image](https://i.imgur.com/wTAU8oy.png)
  6. В поле «Базовый домен» введите localhost
  ![image](https://i.imgur.com/VFNkUHI.png)
  7. Сохраните изменения
  8. Скопируйте ID приложения
  ![image](https://i.imgur.com/92giyev.png)
  9. В данную ссылку в параметр client_id вместо 1 вставьте ID вашего приложения:
  https://oauth.vk.com/authorize?client_id=1&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=stats.offline&response_type=token
  10. Перейдите по ссылке и сохраните из полученной адресной строки ваш токен пользователя
  ![image](https://i.imgur.com/lZPX8Ss.png)
  
  Подробнее про ключи доступа VK API: https://dev.vk.com/api/access-token/getting-started

------
  
</details>

<details>
  <summary> Как получить ключ доступа сообщества</summary>
  
  1. Для начала нужно иметь свое сообщество, которое и будет непосредственно осуществлять общение. Подробнее про создание сообщества: https://vk.com/faq18025
  2. Перейдите в настройки, в раздел «Работа с API»
  ![image](https://i.imgur.com/MKqtKO0.png)
  3. Нажмите «Создать ключ»
  ![image](https://i.imgur.com/1MfUQFU.png)
  4. Выберите необходимые права для ключа. В данном случае вам нужен доступ к управлению и сообщениям сообщества
  ![image](https://i.imgur.com/LOxhMXD.png)
  5. Сохраните созданный ключ доступа сообщества
  ![image](https://i.imgur.com/qSbE7Tc.png)
  
  Подробнее про ключи доступа VK API: https://dev.vk.com/api/access-token/getting-started
  
  ------
  
</details>

<details>
  <summary> Как получить идентификатор сообщества</summary>
  
  Откройте настройки сообщества и под полем «Адрес» найдите номер сообщества. Это и есть наш идентификатор сообщества
  ![image](https://imgur.com/GMgmeQs)
  
    ------
  
</details>

### 4. Настройте ваше сообщество

1. Перейдите в управление сообщества в раздел «Сообщения», включите «Сообщения сообщества» и сохраните изменения
![image](https://i.imgur.com/QhCqVCG.png)
2. Перейдите в раздел «Настройки для бота», включите «Возможности ботов» и сохраните изменения
![image](https://i.imgur.com/dUDEyBS.png)
3. Перейдите в настройки, в раздел «Работа с API», откройте вкладку «Long Poll API» и включите «Long Poll API»
![image](https://i.imgur.com/CQ4Saeo.png)
4. В этом же разделе откройте вкладку «Типы событий» и поставьте галочки во входящих и исходящих сообщениях
![image](https://i.imgur.com/NqUGdWf.png)

### 5. Создайте вашу базу данных

Создайте новую базу данных для бота. После откройте файл db.py и вставьте ваши данные в значение engine, в параметры sq.create_engine() в формате:
‘ваша система управления базы данных://пользователь:пароль@хост/название базы данных’
```
[VK]
engine = sq.create_engine('postgresql://username:password@localhost:5432/VKinder')
```

Подробнее о пользовании create_engine: https://docs.sqlalchemy.org/en/14/tutorial/engine.html#tutorial-engine

### 6. Готово!

Запустите программу и отправьте свое первое сообщение боту. 
Принцип работы довольно прост и понятен с первого диалога. Более подробную документацию каждого объекта можно найти внутри кода. 
