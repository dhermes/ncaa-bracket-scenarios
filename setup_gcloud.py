from gcloud.credentials import get_for_service_account_json
from gcloud import datastore

from local_settings import DATASET_ID
from local_settings import KEY_NAME

CREDS = get_for_service_account_json(KEY_NAME, datastore.SCOPE)
CNXN = datastore.Connection(CREDS)
datastore.set_defaults(dataset_id=DATASET_ID, connection=CNXN)
