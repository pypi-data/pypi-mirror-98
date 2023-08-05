from enum import Enum

GRAPH_BASE_URL = "https://graph.microsoft.com"
V1_EP = "/v1.0"
BETA_EP = "/beta"

# OData query params
SELECT = "$select"
COUNT = "$count"
FILTER = "$filter"
SEARCH = "search"

# Resources
USERS = "/users"
SUBSCRIPTIONS = "/subscriptions"
MAILS = "/messages"
GROUPS = "/groups"
SITES = "/sites"
DRIVE = "/drive"
TEAMS = "/teams"
CHANNELS = "/channels"

# next_key
NEXT_KEY = "@odata.nextLink"

# delta_key
DELTA_KEY = "@odata.deltaLink"


# Subscription Resources
class SubscriptionResources(str, Enum):

    def __new__(cls, value, resource_data_included: bool=None):
        subscription_resource = str.__new__(cls, value)
        subscription_resource._value_ = value
        subscription_resource.resource_data_included = resource_data_included
        return subscription_resource

    Mailbox             = "users('{}')/messages", False
    Inbox               = "users('{}')/mailFolders('Inbox')/messages", False
    DriveRoot           = "users/{}/drive/root", False
    SiteDocumentLibrary = "sites/{}/drive/root", False
    GroupDriveRoot      = "groups/{}/drive/root", False
    TenantTeamsChannels = "teams/allMessages", True
    TenantChats         = "chats/allMessages", True
