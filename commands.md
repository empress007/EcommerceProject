## E-commerce site built with django

python 3.11.7
Django 5.1.3

# Project Protocols
1. **Create a virtual enviroment**
    ```Windows
        virtualenv virt
        virt\scripts\activate
    ```
2. **Install packages and commands**
   - Django: `pip install django`


   *commands*
   - Collect packages `pip freeze . requirement.text`
   - Start Project    `django-admin startproject setup`
   - Start Application: `python manage.py startapp users`
   -Make migrations    `python manage.py makemigrations`
                       `python manage.py migrate`

3.  **Load templates and static files**
     Templates source - colorlib
     configure template and static files in the _setting.py_ file
        -TEMPLATES = {
                "DIRS": [BASE_DIR / "templates"],
           }
        -STATIC_URL = "static/"
         STATICFILES_DIRS = [BASE_DIR / "static"]
