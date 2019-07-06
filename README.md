# CustomerInfoDemo - An demo app for managing the customer information

CustomeInfo is a B/S mode application and based on Django framework. It provides
essential functionalities for managing the customer information as well as the 
notes added by user. The XML-PRC APIs are also available for user to read/write
customer data directly from the database.

## Design

### Templates
- customerlist.html: present the customer list which can be searched and sorted
                     by vary field.
- customer.html: show the details of customer information as well as the note
                 list. The customer state can be changed and the note can be
                 added, updated and removed.

![Customer list page example](https://github.com/davegogle/customerinfo-demo/raw/master/docs/customerlist.png)
![Customer details page example](https://github.com/davegogle/customerinfo-demo/raw/master/docs/customer.png)

### Views
- show_customerlist(): present an empty customer list page
- show_customer(): present the customer information page
- ajax_clst_search(): handle the requests of sorting/searching customer list
- ajax_change_state(): handle the customer state change request
- ajax_note_list(): handle the requests of adding, updating and removing note

### Models:
![Class graph of models](https://github.com/davegogle/customerinfo-demo/raw/master/docs/customerinfo-models.png)

# Demo
![Demo on Youtube](https://youtu.be/eoYLGgOkeTo)

# Install
## Dependencies
- Django = v1.11
- django-extensions >= v2.1.0
- django-xmlrpc >= v0.1.8

To install::
```console
$ git clone https://github.com/davegogle/customerinfo-demo.git
$ cd customerinfo-demo && sudo python3 setup.py install
```

Then you need to add below lines in your local Django server's settings.py:

```console
INSTALLED_APPS = [
    ...
    'customerinfo.apps.CustomerInfoConfig',
    ....
]

XMLRPC_METHODS = (
    ....
    ('customerinfo.xmlrpc_server.create_or_update_customer',
     'create_or_update_customer'),
    ('customerinfo.xmlrpc_server.get_customer', 'get_customer'),
    ....
)
```

And also include customerinfo.url in your local urls.py.

# Uninstall
If you want to uninstall this app, issue the following command::
```console
$ sudo pip3 uninstall customerinfo-demo
```

# XML-RPC API
There are two XML-PRC methods available for reading/writing customer information
from database.
- creaete_or_update_customer(): create or update customer information in database
- get_customer(): get customer information from database

Example of using XML-PRC API::
```python
import xmlrpc.client as xmlrpc

XMLRPC_SERVER_URL = ''
server = xmlrpc.ServerProxy(XMLPRC_SERVER_URL)

# check if the server is connected
server.system.listMethods()

# create a customer information in database
server.create_or_update_customer({
    'first_name': 'David',
    'last_name': 'Foo',
    'email': 'david.foo@example.com',
    'phone': '(66) 02 1234-5678'})
```
