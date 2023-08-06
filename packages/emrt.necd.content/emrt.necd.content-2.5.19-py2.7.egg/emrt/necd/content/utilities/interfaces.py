from zope.interface import Interface
from zope.interface import Attribute


class ILDAPQuery(Interface):
    """ Query LDAP directly. Using the configuration of the
        provided LDAPUserFolder.
    """

    acl = Attribute("The LDAPUserFolder we're operating on.")
    config = Attribute('Automatically set, after calling connect().')
    connection = Attribute('Automatically set, after calling connect().')

    def connect(acl):
        """ Start LDAP connection. Sets and returns a connection."""

    def query_ou(ou, query, attrs):
        """ Queries ou for query, requesting attrs.
            Uses the connection initialized by connect().
        """

    def query_groups(query, attrs):
        """ Helper method, calls query_ou() with self.config['ou_groups'].
        """

    def query_users(query, attrs):
        """ Helper method, calls query_ou() with self.config['ou_users'].
        """


class ISetupReviewFolderRoles(Interface):
    """ Grant local, Zope roles to certain LDAP groups.
    """


class IFollowUpPermission(Interface):
    """
    Permission check for adding a follow up question
    """


class IUserIsMS(Interface):
    """ Returns True if the user has
        the MSAuthority or MSExpert roles.
    """


class IGetLDAPWrapper(Interface):
    """Returns the context_based LDAP wrapper"""
