import yaml, os
from dotenv import load_dotenv

load_dotenv()  # loads .env

def load_config(path="config/config.yaml"):
    with open(path) as f:
        cfg = yaml.safe_load(f)
    # merge secrets from env
    cfg['secrets'] = {
        'admin_user': os.getenv('ADMIN_USER'),
        'admin_pass': os.getenv('ADMIN_PASS'),
    }
    # ReportPortal envs (optional)
    cfg['reportportal'] = {
        'endpoint': os.getenv('RP_ENDPOINT'),
        'uuid': os.getenv('RP_UUID'),
        'project': os.getenv('RP_PROJECT'),
        'launch': os.getenv('RP_LAUNCH')
    }
    return cfg
