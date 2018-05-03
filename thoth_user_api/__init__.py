"""Thoth User API"""


import os


__name__ = 'thoth-user-api'
__version__ = '0.2.0'
__description__ = 'Thoth: User API'
__git_commit_id__ = os.getenv('OPENSHIFT_BUILD_COMMIT', '')
