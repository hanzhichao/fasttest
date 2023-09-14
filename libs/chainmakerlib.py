from typing import List

from chainmaker.chain_client import ChainClientWithEndorsers
from chainmaker.keys import AuthType
from chainmaker.node import Node
from chainmaker.user import User


def read_file_bytes(file_path):
    return open(file_path, 'rb').read()


def get_chain_client(crypto_config_path, node_list, chain_id, auth_type):
    if auth_type == AuthType.PermissionedWithCert:
        org_id, singer = ('wx-org1.chainmaker.org', 'client1')
        endorsers = [
            ('wx-org1.chainmaker.org', 'admin1'),
            ('wx-org2.chainmaker.org', 'admin1'),
            ('wx-org3.chainmaker.org', 'admin1'),
        ]

        # 创建签名用户
        user = User(
            org_id=org_id,
            sign_key_bytes=read_file_bytes(f'{crypto_config_path}/{org_id}/user/{singer}/{singer}.sign.key'),
            sign_cert_bytes=read_file_bytes(f'{crypto_config_path}/{org_id}/user/{singer}/{singer}.sign.crt'),
            tls_key_bytes=read_file_bytes(f'{crypto_config_path}/{org_id}/user/{singer}/{singer}.tls.key'),
            tls_cert_bytes=read_file_bytes(f'{crypto_config_path}/{org_id}/user/{singer}/{singer}.tls.crt')
        )

        # 创建连接节点
        nodes = []
        for node in node_list:
            ca_org_id = node.get('org_id') or org_id
            nodes.append(Node(
                node_addr=node['node_addr'],
                conn_cnt=1,
                enable_tls=True,
                trust_cas=read_file_bytes(f'{crypto_config_path}/{ca_org_id}/ca/ca.crt'),
                tls_host_name='chainmaker.org'
            ))

        # 创建链客户端
        cc = ChainClientWithEndorsers(chain_id=chain_id, user=user, nodes=nodes)
        endorse_users = [
            User(
                org_id=org_id,
                sign_key_bytes=read_file_bytes(
                    f'{crypto_config_path}/{org_id}/user/{singer}/{singer}.sign.key'),
                sign_cert_bytes=read_file_bytes(
                    f'{crypto_config_path}/{org_id}/user/{singer}/{singer}.sign.crt')
            ) for org_id, singer in endorsers
        ]

        cc.endorse_users = endorse_users
        return cc


class Chainmaker:
    def __init__(self, crypto_config_path, node_list: List[dict], chain_id='chain1',
                 auth_type=AuthType.PermissionedWithCert):
        self.cc = get_chain_client(crypto_config_path, node_list, chain_id, auth_type)

    def __getattr__(self, item):
        return getattr(self.cc, item)


class ContractManage(Chainmaker):
    pass
