[![Build Status](https://travis-ci.org/UlmBlois/website.svg?branch=master)](https://travis-ci.org/UlmBlois/website)
[![Coverage Status](https://coveralls.io/repos/github/UlmBlois/website/badge.svg?branch=master)](https://coveralls.io/github/UlmBlois/website?branch=master)
# website
Website for the ULM meeting of Blois


# Printing

For Monarch 9416 (make the printer the default one):
* in Chrome
  * print settings
    * portrait
    * paper size: 2x4
    * margin: none
    * scale: default
  * add parameters (after setting the printer):
    * --kiosk-printing

# Migrate
Migrate from a prior version to @tags:beta1 you will need to run:

```
echo "INSERT INTO django_migrations (app, name, applied) VALUES ('core', '0001_initial', CURRENT_TIMESTAMP);" | python manage.py dbshell

echo "UPDATE django_content_type SET app_label = 'core' WHERE app_label = 'auth' and model = 'user';" | python manage.py dbshell
```
