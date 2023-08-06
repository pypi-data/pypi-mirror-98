# Django PKCS7 Parser

## Install

Using pip

```
pip install dj-pkcs7
```

## Usage:

Add to your settings.py INSTALLED_APPS

``` 
...
'dj_pkcs7',
...
```

And include the routes in your urls.py::

```
...
path('pkcs7/', include('dj_pkcs7.urls')),
...
```

