"""
Platform version constants.
Increment on release
To ensure configuration files from example apps and plugins have same version as engine,
environment variables `CA_APP1_VERSION` and `CA_APP1_APPS_API_VERSION` are set.
"""
import os
import sys

CA_APP1_NAME = "app0.app1"
CA_APP1_VERSION = "0.1.1"

# Major.Minor version to be used in App versions and Api endpoints for Apps/Plugins
APPS_API_VERSION = '.'.join(CA_APP1_VERSION.split('.')[0:2])
APPS_ROUTE_VERSION = APPS_API_VERSION.replace('.', 'x')

os.environ['CA_APP1_VERSION'] = CA_APP1_VERSION
os.environ['CA_APP1_API_VERSION'] = APPS_API_VERSION
os.environ['CA_APP1_ROUTE_VERSION'] = APPS_ROUTE_VERSION

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "APPS_API_VERSION":
        print(APPS_API_VERSION)
    elif len(sys.argv) > 1 and sys.argv[1] == "APPS_ROUTE_VERSION":
        print(APPS_ROUTE_VERSION)
    else:
        print(CA_APP1_VERSION)
