# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easy_tenants']

package_data = \
{'': ['*']}

install_requires = \
['django-appconf>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'django-easy-tenants',
    'version': '0.4.0',
    'description': 'Easy to create applications that use tenants in django',
    'long_description': '# easy-tenants\n\n![Tests](https://github.com/CleitonDeLima/django-easy-tenants/workflows/Tests/badge.svg)\n[![codecov](https://codecov.io/gh/CleitonDeLima/django-easy-tenants/branch/master/graph/badge.svg)](https://codecov.io/gh/CleitonDeLima/django-easy-tenants)\n[![PyPI Version](https://img.shields.io/pypi/v/django-easy-tenants.svg)](https://pypi.org/project/django-easy-tenants/)\n[![PyPI downloads](https://img.shields.io/pypi/dm/django-easy-tenants.svg)](https://img.shields.io/pypi/dm/django-easy-tenants.svg)\n\n\nThis is a Django app for managing multiple tenants on the same project\ninstance using a shared approach.\n\n\n## Background\n\nThere are typically three solutions for solving the multitenancy problem:\n\n1. Isolated Approach: Separate Databases. Each tenant has it’s own database.\n2. Semi Isolated Approach: Shared Database, Separate Schemas.\nOne database for all tenants, but one schema per tenant.\n3. Shared Approach: Shared Database, Shared Schema. All tenants share\nthe same database and schema. There is a main tenant-table, where all\nother tables have a foreign key pointing to.\n\nThis application implements the third approach,  which in our opinion,\nis the best solution for a large amount of tenants.\n\nFor more information: [Building Multi Tenant Applications with Django\n](https://books.agiliq.com/projects/django-multi-tenant/en/latest/)\n\nBelow is a demonstration of the features in each approach for an application\nwith 5000 tenants.\n\nApproach       | Number of DB | Number of Schemas | Django migration time | Public access\n-------------- | ------------ | ----------------- | --------------------- | ---------------\nIsolated       | 5000         | 5000              | slow (1/DB)           | No\nSemi Isolated  | 1            | 5000              | slow (1/Schema)       | Yes\nShared         | 1            | 1                 | fast (1)              | Yes\n\n\n## How it works\nThe following image shows the flow of how this application works.\n\n![how to works](./screenshots/flux_easy_tenants.png)\n\n\n## Instalation\nAssuming you have django installed, the first step is to install `django-easy-tenants`.\n```bash\npip install django-easy-tenants\n```\nNow you can import the tenancy module in your Django project.\n\n\n## Setup\nIt is recommended to install this app at the beginning of a project.\nIn an existing project, depending on the structure of the models,\nthe data migration can be hard.\n\nAdd `easy_tenants` to your `INSTALLED_APPS` on `settings.py`.\n\n`settings.py`\n```python\nINSTALLED_APPS = [\n    ...,\n    \'easy_tenants\',\n]\n```\n\nCreate a model which will be the tenant of the application.\n\n`yourapp/models.py`\n```python\nfrom easy_tenants.models import TenantMixin\n\nclass Customer(TenantMixin):\n    ...\n```\n\nDefine on your `settings.py` which model is your tenant model. Assuming you created `Customer`\ninside an app named `yourapp`, your EASY_TENANTS_MODEL should look like this:\n\n`settings.py`\n```python\nEASY_TENANTS_MODEL = \'yourapp.Customer\'\n```\n\nYour models, that should have data isolated by tenant, need to inherit from `TenantAbstract`\nand the objects need to be replaced by `TenantManager()`.\n\n\n```python\nfrom django.db import models\nfrom easy_tenants.models import TenantAbstract\nfrom easy_tenants.managers import TenantManager\n\nclass Product(TenantAbstract):\n    name = models.CharField(max_length=10)\n\n    objects = TenantManager()\n```\n\nTo obtain the data for each tenant, it is necessary to define which tenant will be used:\n\n```python\nfrom easy_tenants import set_current_tenant\n\ncustomer = Customer.objects.first()\nset_current_tenant(customer)\n\nProduct.objects.all()  # filter by customer\n\n```\nor\n\n```python\nfrom easy_tenants import tenant_context\n\nwith tenant_context(customer):\n    Product.objects.all()  # filter by customer\n```\n\nTo define the tenant to be used, this will depend on the business rule used. Here is an example for creating middleware that defines a tenant:\n\n```python\nfrom django.http import HttpResponse\nfrom easy_tenants import tenant_context\n\nclass TenantMiddleware:\n    def __init__(self, get_response):\n        self.get_response = get_response\n\n    def __call__(self, request):\n        customer = get_customer_by_request(request)\n\n        if not customer:\n            return HttpResponse("Select tenant")\n\n        with tenant_context(customer):\n            return self.get_response(request)\n```\n\nIf you want to separate the upload files by tenant, you need to change the `DEFAULT_FILE_STORAGE`\nconfiguration (only available for local files).\n\n```python\nDEFAULT_FILE_STORAGE = \'easy_tenants.storage.TenantFileSystemStorage\'\n```\n\n\n## Running the example project\n```bash\npython manage.py migrate\npython manage.py createsuperuser\npython manage.py shell # create 2 customers\npython manage.py runserver\n```\nAccess the page `/admin/`, create a `Customer` and then add a user on the created `Customer`.\n\n## Motivation\n[django-tenant-schemas](https://github.com/bernardopires/django-tenant-schemas)\n[django-tenants](https://github.com/tomturner/django-tenants)\n[django-scopes](https://github.com/raphaelm/django-scopes)\n',
    'author': 'Cleiton Lima',
    'author_email': 'cleiton.limapin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CleitonDeLima/django-easy-tenants',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
