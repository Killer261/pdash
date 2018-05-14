import unittest

from cpchain.market.market.utils import *
from cpchain.utils import join_with_root, config, Encoder
private_key_file = 'tests/market/assets/UTC--2018-01-25T08-04-38.217120006Z--22114f40ed222e83bbd88dc6cbb3b9a136299a23'
private_key_password_file = 'tests/market/assets/password'


class UtilsTest(unittest.TestCase):

    def test_load_key_pair_from_keystore(self):
        private_key_file_path = join_with_root(private_key_file)
        password_path = join_with_root(private_key_password_file)

        with open(password_path) as f:
            password = f.read()

        pri_key_string, pub_key_string = ECCipher.load_key_pair_from_keystore(private_key_file_path, password)
        print("pri_key_string:")
        print(pri_key_string)

        print("pub_key_string:")
        print(pub_key_string)

        print("------------------verify is correct pub/pri key--------------------")
        key_bytes = Encoder.str_to_base64_byte(pri_key_string)
        loaded_pub_key = ECCipher._get_public_key_from_private_key_bytes(key_bytes)
        print("loaded_pub_key:" + loaded_pub_key)
        self.assertEqual(pub_key_string, loaded_pub_key)

        # ---------- sign and verify ------------
        data = "testdata"
        new_signature = sign(pri_key_string, data)
        print("new_signature is:" + new_signature)

        is_valid_sign = verify_signature(pub_key_string, new_signature, data)
        print("is valid new_signature:" + str(is_valid_sign))
        self.assertTrue(is_valid_sign, "should be success")

        is_valid_sign = verify_signature(pub_key_string, new_signature, data + "error")
        print("is valid new_signature:" + str(is_valid_sign))
        self.assertFalse(is_valid_sign, "should be failed")


if __name__ == '__main__':
    unittest.main()
