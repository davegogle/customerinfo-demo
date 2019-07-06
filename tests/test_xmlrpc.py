#!/usr/bin/env python

from unittest import TestCase
import xmlrpc.client as xmlrpc

XMLRPC_SERVER_URL = ''
TEST_DATA = {
}

class TestCreateOrUpdateCustomer(unittest.TestCase):
    def setUp(self):
        self.method_name = 'create_or_update_customer'
        self.method_list = None
        self.server = xmlrpc.ServerProxy(XMLRPC_SERVER_URL)
        

    def tearDown(self):
        pass
        

    def test_connecion(self):
        try:
            self.method_list = self.server.system.listMethods()
        except Exception as e:
            self.fail(e)


    def test_method_exist(self):
        self.assertTrue(self.method_list != None)
        self.assertTrue(self.method_name in self.method_list)


    def test_create_cusotmer(self):
        try:
            result, msg, cid = \
                self.server.create_or_update_customer(TEST_DATA['good'])
        except Exception as e:
            self.fail(e)

        self.assertTrue(result)

        self.assertTrue(self.method_list != None)
        self.assertTrue(self.method_name in self.method_list)
        except Exception as e:
            self.fail(e)

        self.assertTrue(
        self.wk.data = json.loads(wheel_json)
        
        self.wk.add_signer('+', '67890')
        self.wk.add_signer('scope', 'abcdefg')
        
        self.wk.trust('epocs', 'gfedcba')
        self.wk.trust('+', '12345')
        
        self.wk.save()
        
        del self.wk.data
        self.wk.load()
        
        signers = self.wk.signers('scope')
        self.assertTrue(signers[0] == ('scope', 'abcdefg'), self.wk.data['signers'])
        self.assertTrue(signers[1][0] == '+', self.wk.data['signers'])
        
        trusted = self.wk.trusted('epocs')
        self.assertTrue(trusted[0] == ('epocs', 'gfedcba'))
        self.assertTrue(trusted[1][0] == '+')
        
        self.wk.untrust('epocs', 'gfedcba')
        trusted = self.wk.trusted('epocs')
        self.assertTrue(('epocs', 'gfedcba') not in trusted)
        
    def test_load_save_incomplete(self):
        self.wk.data = json.loads(wheel_json)
        del self.wk.data['signers']
        self.wk.data['schema'] = self.wk.SCHEMA+1
        self.wk.save()
        try:
            self.wk.load()
        except ValueError:
            pass
        else:
            raise Exception("Expected ValueError")
        
        del self.wk.data['schema']
        self.wk.save()
        self.wk.load()
    
    
