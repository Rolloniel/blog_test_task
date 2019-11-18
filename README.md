# planeks_test_task

# Install guide

1. Clone/Download project to desired location
2. Set path to custom Django settings file location:
```
DJANGO_SETTINGS_MODULE=config.settings
```
3. Add secrets.json file to config folder. Sample:
```json

{
  "FILENAME": "secrets.json",
  "SECRET_KEY": "<YOUR_SECRET_KEY_LOCATED_IN_SETTINGS>",

  "DEBUG": true,

  "EMAIL_HOST": "<SMTP_HOST>",
  "EMAIL_PORT": 587,
  "EMAIL_HOST_USER": "<YOUR_SMTP_HOST_USER>",
  "EMAIL_HOST_PASSWORD": "<YOUR_SMTP_HOST_USER_PASSWORD>"

}
```
4. Create venv and install requirements with 
```
virtualenv -p python3.6 <path_to_desired_venv_folder>
source <path_to_desired_venv_folder>/bin/activate
pip install -r requirements.txt
```
5. Run following manage.py tasks:
```
python manage.py migrate
python manage.py collectstatic

```
6. Create superuser for admin pannel access with:
```
python manage.py createsuperuser
```
 and follow commands.
 
7. Create default user groups with their permissions by running:
```
python /utils/initial_user_groups_setup.py
```
 
8. Run server:
```
python manage.py runserver
```
9. Visit http://localhost:8000/ to test functionality

# Notes

1. User, Group, Permission, news, post premoderation is available via http://localhost:8000/admin pannel




