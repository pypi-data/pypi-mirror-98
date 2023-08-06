from dotenv import load_dotenv
load_dotenv()
import os


def paloalto_api_key():
    paloalto_api_key = os.getenv('paloalto_api_key', None)
    if paloalto_api_key is None:
        raise SystemExit('Please set environment variable paloalto_api_key')
    else:
        paloalto_api_key = os.environ['paloalto_api_key']
    return paloalto_api_key


def paloalto_panorama_ip():
    paloalto_panorama_ip = os.getenv('paloalto_panorama_ip', None)
    if paloalto_panorama_ip is None:
        raise SystemExit('Please set environment variable paloalto_panorama_ip')
    else:
        paloalto_panorama_ip = os.environ['paloalto_panorama_ip']
    return paloalto_panorama_ip

