# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016, 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""REST API for Records.

Records-REST provides API resources for record operations with permission
control and different serialization formats.

Features:
    Create/Delete/Modify/Search records
    Set permissions
    Choose response serializers for various bibliographic formats

For further extending the REST API take a look at the guide in invenio-rest.

Initialization
--------------

Create a Flask application:

>>> import os
>>> from flask import Flask
>>> app = Flask('myapp')


Instantiate all the dependencies

>>> from invenio_db import InvenioDB
>>> from invenio_rest import InvenioREST
>>> from invenio_pidstore import InvenioPIDStore
>>> from invenio_records import InvenioRecords
>>> from invenio_records_rest import InvenioRecordsREST
>>> from invenio_search import InvenioSearch
>>> from invenio_indexer import InvenioIndexer
>>> from invenio_records_rest.utils import PIDConverter

>>> ext_db = InvenioDB(app)
>>> InvenioREST(app)
>>> InvenioPIDStore(app)
>>> InvenioRecords(app)
>>> search = InvenioSearch(app)
>>> InvenioIndexer(app)
>>> app.url_map.converters['pid'] = PIDConverter
>>> InvenioRecordsREST(app)

A basic configuration is needed to

>>> index_name = 'testrecords-testrecord-v1.0.0'
>>> app.config.update(
...     INDEXER_DEFAULT_INDEX=index_name,
...     INDEXER_DEFAULT_DOC_TYPE='testrecord-v1.0.0',
...     SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI',
...                                       'sqlite:///app.db'),
...     RECORDS_REST_DEFAULT_READ_PERMISSION_FACTORY=None,
...     RECORDS_REST_DEFAULT_CREATE_PERMISSION_FACTORY=None,
...     RECORDS_REST_DEFAULT_DELETE_PERMISSION_FACTORY=None,
...     RECORDS_REST_DEFAULT_UPDATE_PERMISSION_FACTORY=None,
... )
>>> app.config['RECORDS_REST_ENDPOINTS']['recid']['search_index'] = index_name

For the following examples we will need an application context so let's
push one:

>>> app.app_context().push()

Also, for the examples to work we need to create the database and tables:

>>> from invenio_db import db
>>> db.create_all()

and finally for enabling indexing with Elasticsearch we need to create the
indices and put the templates:

>>> indices = list(search.create(ignore=[400]))
>>> templates = search.put_templates(ignore=[400])

The server is now ready to receive requests so we can start it with:

>>> app.run()

By default it uses port 5000.

Let's create the first record. Open a new terminal and run:

$ export DATA='{"title": "Test Record"}'
$ curl -L -H 'Content-Type:application/json' -d $DATA -XPOST localhost:5000/records

Adding the -L flag will follow the redirects and you will see in the output the
created record.

{
  "created": "2017-11-24T10:52:42.761135+00:00",
  "id": 1,
  "links": {
    "self": "http://localhost:5000/records/3"
  },
  "metadata": {
    "control_number": "1",
    "title": "Test Record"
  },
  "updated": "2017-11-24T10:52:42.761161+00:00"
}

To get the record you
curl -XDELETE http://localhost:5000/records/3

"""

from __future__ import absolute_import, print_function

from .ext import InvenioRecordsREST
from .proxies import current_records_rest
from .version import __version__

__all__ = ('__version__', 'current_records_rest', 'InvenioRecordsREST')
