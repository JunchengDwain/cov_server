import os
import json

COV_RENT = 'cov_rent'
if os.environ.get(COV_RENT, None) is not None:
    cov = os.environ[COV_RENT]
    cov_config = json.loads(cov)
    print(type(cov_config))
    print(cov_config.get('sub_port', None))

