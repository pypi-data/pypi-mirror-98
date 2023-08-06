
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.authentication_and_users_api import AuthenticationAndUsersApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from datameta_client_lib.api.authentication_and_users_api import AuthenticationAndUsersApi
from datameta_client_lib.api.files_api import FilesApi
from datameta_client_lib.api.groups_api import GroupsApi
from datameta_client_lib.api.metadata_api import MetadataApi
from datameta_client_lib.api.submissions_api import SubmissionsApi
