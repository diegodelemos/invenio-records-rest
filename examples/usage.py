# # Explanation

import os
from flask import Flask

# # Initialization

# Create a Flask application
app = Flask('myapp')


# Initialize dependencies
from invenio_db import InvenioDB
from invenio_rest import InvenioREST
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords
from invenio_records_rest import InvenioRecordsREST
from invenio_search import InvenioSearch
from invenio_indexer import InvenioIndexer
from invenio_records_rest.utils import PIDConverter


ext_db = InvenioDB(app)
InvenioREST(app)
InvenioPIDStore(app)
InvenioRecords(app)
search = InvenioSearch(app)
InvenioIndexer(app)
app.url_map.converters['pid'] = PIDConverter
InvenioRecordsREST(app)

# index name
index_name = 'testrecords-testrecord-v1.0.0'
app.config.update(
    INDEXER_DEFAULT_INDEX=index_name,
    INDEXER_DEFAULT_DOC_TYPE='testrecord-v1.0.0',
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI',
                                      'sqlite:///app.db'),
    RECORDS_REST_DEFAULT_CREATE_PERMISSION_FACTORY=None,
    RECORDS_REST_DEFAULT_READ_PERMISSION_FACTORY=None,
    RECORDS_REST_DEFAULT_UPDATE_PERMISSION_FACTORY=None,
    RECORDS_REST_DEFAULT_DELETE_PERMISSION_FACTORY=None,
)
# app.config['RECORDS_REST_ENDPOINTS'] = RECORDS_REST_ENDPOINTS
app.config['RECORDS_REST_ENDPOINTS']['recid']['search_index'] = index_name


# Initialize DB
# push Flask application context
from invenio_db import db
app.app_context().push()
db.create_all()
# Create database and tables

# Index init
indeces = list(search.create(ignore=[400]))
templates = list(search.put_templates(ignore=[400]))

print(app.url_map)
app.run()
