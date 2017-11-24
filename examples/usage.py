# # Explanation
# ...
# # Initialization

# Create a Flask application
import os

from flask import Flask
index_name = 'testrecords-testrecord-v1.0.0'
app = Flask('myapp')

# Loading dependencies

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
search.register_mappings('testrecords', 'data')
InvenioIndexer(app)
app.url_map.converters['pid'] = PIDConverter
InvenioRecordsREST(app)

# Configure application
from invenio_records_rest.facets import terms_filter

index_name = 'testrecords-testrecord-v1.0.0'
app.config.update(
    INDEXER_DEFAULT_INDEX=index_name,
    INDEXER_DEFAULT_DOC_TYPE='testrecord-v1.0.0',
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE',
                                      'sqlite:///app.db'),
    RECORDS_REST_DEFAULT_READ_PERMISSION_FACTORY=None,
    RECORDS_REST_DEFAULT_CREATE_PERMISSION_FACTORY=None,
    RECORDS_REST_DEFAULT_DELETE_PERMISSION_FACTORY=None,
    RECORDS_REST_DEFAULT_UPDATE_PERMISSION_FACTORY=None,
)
app.config['RECORDS_REST_ENDPOINTS']['recid']['search_index'] = index_name
# app.url_map.converters['pid'] = PIDConverter

# Initialize DB
# push Flask application context
app.app_context().push()
# Create database and tables
from invenio_db import db
db.create_all()

# Indeces init
indices = list(search.create(ignore=[400]))
templates = search.put_templates(ignore=[400])
