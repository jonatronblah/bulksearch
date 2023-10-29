import ldap3
import os
from ldap3.core.exceptions import LDAPException

ldap_server = os.getenv("LDAP_HOST")
ldap_un = os.getenv("LDAP_USERNAME")
ldap_ps = os.getenv("LDAP_PASSWORD")
ldap_base = os.getenv("LDAP_BASE_DN")


def ldap_login(server, username, password):
    username = "mwllp" + "\\" + username
    try:
        with ldap3.Connection(server, user=username, password=password) as conn:
            print(conn.result["description"]) # "success" if bind is ok
            return True
    except LDAPException:
        print('Unable to connect to LDAP server')
        return False

def ldap_group(server, service_username, service_password, username, group):
    with ldap3.Connection(server, user=service_username, password=service_password) as conn:
        conn.search('DC=mwllp,DC=dom', 
            f"(&(objectClass=user)(sAMAccountName={username}))",
            search_scope=ldap3.SUBTREE, 
            attributes=['cn', 'memberOf'])
        memof = conn.entries[0].memberOf
        user_groups = []
        for i in memof:
            conn.search(i, '(objectclass=group)', search_scope=ldap3.SUBTREE, attributes=['cn'])
            user_groups.append(conn.entries[0].cn[0])
        if group in user_groups:
            return True
        else:
            return False







# def ldap_group(group):
#     with ldap3.Connection(ldap_server, ldap_un, ldap_ps, auto_bind=True) as conn:
#         conn.search(
#             search_base=f'CN={group},OU=GROUPS,OU=Live,OU=Accounts,OU=Common,DC=mwllp,DC=dom',
#             search_filter='(objectClass=group)',
#             search_scope='SUBTREE',
#             attributes = ['member']
#         )
#         member_list = []
#         for entry in conn.entries:
#             for member in entry.member.values:
#                 conn.search(
#                     search_base='OU=Common,DC=mwllp,DC=dom',
#                     search_filter=f'(distinguishedName={member})',
#                     attributes=[
#                         'sAMAccountName'
#                     ]
#                 )

#                 user_sAMAccountName = conn.entries[0].sAMAccountName.values

#                 member_list.append(user_sAMAccountName)

#     return member_list
