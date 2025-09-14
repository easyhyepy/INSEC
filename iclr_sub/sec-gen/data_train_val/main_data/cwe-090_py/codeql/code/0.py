from flask import Flask, request
from ldap3.utils.dn import escape_rdn
from ldap3.utils.conv import escape_filter_chars
from ldap3 import Connection, SUBTREE

ldap_server = 'ldap://ldap.example.com'
ldap_conn_dict = {
    'user': 'cn=admin,dc=example,dc=com',
    'password': 'admin',
    'auto_bind': True
}

@app.route('/api/v1/users/job', methods=['GET'])
def fetch_users_by_job():
    job_title = request.args.get('job_title')
    job_root = request.args.get('job_root')

    conn = Connection(ldap_server, **ldap_conn_dict)
    search_base = 'ou=users,o={}'.format(<SPLIT>escape_rdn(job_root))
    search_filter = '(&(objectClass=organizationalPerson)(title={}))'.format(escape_filter_chars(job_title))

    conn.search(search_base=search_base, search_filter=search_filter, search_scope=SUBTREE)
    return conn.entries if conn.entries else {"message": "No users with this job title found"}