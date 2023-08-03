# Публикация комиксов во Вконтакте

Проект представляет собой скрипт, скачивающий комиксы с сайта [https://xkcd.com](https://xkcd.com).
После случайным образом, комикс и комментарий к нему публикуется на стене группы

### Как установить

Для корректной работы вам понадобится указать в файле ```.env```:

- VK_ACCESS_TOKEN - токен нужно получить на [сайте для разработчиков VK](https://dev.vk.com)
- VK_GROUP_ID - id группы можно [на данном сайте](https://regvk.com/id/) (убедитесь, что имеете все необходимые права для публикаций)


Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:

```commandline
pip install -r requirements.txt
```
### Запуск
Для публикации случайного комикса, введите в консоли:

```commandline
python main.py
```

 Пример работы программы:
 
<img width="550" alt="1" src="https://github.com/lamerork/dvmn-vk-comics/assets/65411132/2b4749bd-d247-4a47-b148-5d1c2969b5ea">

 
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
