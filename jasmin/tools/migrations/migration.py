from jasmin.routing.jasminApi import User, Group
from jasmin.routing.Filters import TagFilter

def user_status(data, context=None):
    """Changes impacted by #306

    Will migrate users to enable newly applied changes for enable/disable"""

    # Create new users, they will have the enable/disable methods
    new_data = []
    for old_user in data:
        user = User(
            uid=old_user.uid,
            group=Group(old_user.group.gid),
            username=old_user.username,
            password=old_user.password,
            password_crypted=True,
            mt_credential=old_user.mt_credential,
            smpps_credential=old_user.smpps_credential)
        new_data.append(user)

    return new_data

def group_status(data, context=None):
    """Changes impacted by #306

    Will migrate groups to enable newly applied changes for enable/disable"""

    # Create new groups, they will have the enable/disable methods
    new_data = []
    for old_group in data:
        group = Group(gid=old_group.gid)
        new_data.append(group)

    return new_data

def tagfilters_casting(data, context=None):
    """Changes impacted by #516

    Will cast tag filters to string (from integer) in filters and routes having tagfilters"""

    if context == 'filters':
        for fid, tagfilter in data.iteritems():
            tagfilter.tag = str(tagfilter.tag)
    elif context == 'mtroutes':
        for routes in data.getAll():
            route = routes[routes.keys()[0]]
            for filter in route.filters:
                if isinstance(filter, TagFilter):
                    # Cast tags to str
                    filter.tag = str(filter.tag)

    return data

"""This is the main map for orchestring config migrations.

The map is based on 3 elements:
  1. conditions: binary conditions on Jasmin version, the patch version is zfilled(3), this means 0.8rc2 (or
     0.8.2) will be represented as 0.8002.
  2. contexts: configuration context (users, groups, smppccs ...)
  3. operations: functions to call to migrate the config
"""
MAP = [
    {'conditions': ['<0.8008'],
     'contexts': {'groups'},
     'operations': [group_status]},
    {'conditions': ['<0.8008'],
     'contexts': {'users'},
     'operations': [user_status]},
    {'conditions': ['<=0.9015'],
     'contexts': {'filters', 'mtroutes'},
     'operations': [tagfilters_casting]},]
