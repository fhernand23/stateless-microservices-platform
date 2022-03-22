"""
Platform version constants.
Increment on release
To ensure configuration files from example apps and plugins have same version as engine,
environment variables `APP0_ADMIN_VERSION` and `APP0_ADMIN_APPS_API_VERSION` are set.
"""
import os
import sys

APP0_ADMIN_NAME = "app0.admin"
APP0_ADMIN_VERSION = "0.1.5"

# Major.Minor version to be used in App versions and Api endpoints for Apps/Plugins
APPS_API_VERSION = '.'.join(APP0_ADMIN_VERSION.split('.')[0:2])
APPS_ROUTE_VERSION = APPS_API_VERSION.replace('.', 'x')

os.environ['APP0_ADMIN_VERSION'] = APP0_ADMIN_VERSION
os.environ['APP0_ADMIN_API_VERSION'] = APPS_API_VERSION
os.environ['APP0_ADMIN_ROUTE_VERSION'] = APPS_ROUTE_VERSION

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "APPS_API_VERSION":
        print(APPS_API_VERSION)
    elif len(sys.argv) > 1 and sys.argv[1] == "APPS_ROUTE_VERSION":
        print(APPS_ROUTE_VERSION)
    else:
        print(APP0_ADMIN_VERSION)
