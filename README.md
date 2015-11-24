# tv-notifier-server
TV Series Notifier API Server

## Quick Start
```
virtualenv -p python3 tvnotifyserver
cd tvnotifyserver
source bin/activate
git clone https://github.com/tv-notify/tv-notify-server.git
cd tv-notify-server
python manage.py runserver
```

## Settings
* **GOOGLE_SECRET** - Google Authentication client secret loaded from the *AUTH_GOOGLE_SECRET* environment variable.

Project settings are stored in `tvnotifyserver/settings.py`.
