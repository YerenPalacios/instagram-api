web: daphne instagram.asgi:channel_layer --port 80 --bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=chat.settings -v2
python manage.py collectstatic --noinput
python manage.py migrate