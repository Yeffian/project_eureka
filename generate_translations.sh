
python manage.py makemessages -l zh_Hans
python manage.py makemessages -l en

python generate_translations.py /Users/yeffian/development/project_eureka/locale/zh_Hans/LC_MESSAGES/django.po zh-CN
python generate_translations.py /Users/yeffian/development/project_eureka/locale/en/LC_MESSAGES/django.po en

python manage.py compilemessages