# import ldap3
# from ldap3 import Connection, SUBTREE
# from django.shortcuts import render
#
# AD_SERVER = 'dc2.gk.local'
# AD_USER = 'ldap-bot@gk.local'
# AD_PASSWORD = '12345678'
# AD_SEARCH_TREE = 'dc=gk,dc=local'
#
#
# def server_request():
#     server = ldap3.Server(AD_SERVER)
#     conn = Connection(server, user=AD_USER, password=AD_PASSWORD)  # вынести реквизиты в окружение ОС
#     conn.bind()
#
#     conn.search(AD_SEARCH_TREE,
#                 '(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(&(company=*)))',
#                 SUBTREE,
#                 attributes=['department', 'sAMAccountName', 'displayName', 'physicalDeliveryOfficeName',
#                             'telephoneNumber', 'mail', 'mobile', 'title', 'company', 'lastLogon']
#                 )
#     return conn.entries
#
#
# entries = server_request()
# print(type(entries))
# for entry in entries:
#     print(entry)

class Card(object):

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    # def __eq__(self, other):
    #     return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        return self.rank < other.rank


hand = [Card(10, 'H'), Card(2, 'h'), Card(12, 'h'), Card(13, 'h'), Card(14, 'h')]
hand_order = [c.rank for c in hand]  # [10, 2, 12, 13, 14]
print(hand_order)

hand_sorted = sorted(hand)
hand_sorted_order = [c.rank for c in hand_sorted]  # [2, 10, 12, 13, 14]
print(hand_sorted_order)
