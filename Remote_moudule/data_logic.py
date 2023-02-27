import hashlib
import json
from config import remote_data_path
from package import *
import os
import rsa
import base64

remote_data_hash = ""
public_rsa_key = "../keys/publickey.pem"
private_rsa_key = "../keys/privatekey.pem"
class Remote_date_operate:

    def __init__(self,public_rsa,private_rsa):
        self.public_rsa = public_rsa
        self.private_rsa = private_rsa

    def create_rsa_key(self):
        try:
            (publickey, privatekey) = rsa.newkeys(4096)
            with open(public_rsa_key,"wb") as p:
                p.write(publickey.save_pkcs1("PEM"))
            with open(private_rsa_key,"wb") as p:
                p.write(privatekey.save_pkcs1("PEM"))
            logger.info("RSA Create successful")
            return True
        except Exception as err:
            logger.error(err)
            return False

    def load_rsa_key(self,path,type):
        try:
            if type == 1:
                with open(path, "rb") as p:
                    key = rsa.PublicKey.load_pkcs1(p.read())
                return key
            if type == 2:
                with open(path, "rb") as p:
                    key = rsa.PrivateKey.load_pkcs1(p.read())
                return key
        except Exception as err:
            logger.error(err)
            return False

    def rsa_encrypt(self,str):
        try:
            key = self.load_rsa_key(public_rsa_key,1)
            return rsa.encrypt(str.encode("utf-8"), key)
        except Exception as err:
            logger.error(err)
            return False

    def rsa_decrypt(self,str):
        try:
            key = self.load_rsa_key(private_rsa_key,2)
            return bytes(rsa.decrypt(str,key).decode("utf-8"),'utf-8')
        except Exception as err:
            logger.error(err)
            return False

    def get_remote_data_file_hash(self):
        try:
            with open(remote_data_path,'rb') as file:
                get_data = file.read()
                get_hash = hashlib.md5(get_data).hexdigest()
            return get_hash
        except Exception as err:
            logger.error(err)
            return False

    def get_remote_data(self):
        try:
            with open(remote_data_path,'r', encoding='UTF-8') as data:
                get_date = json.loads(data.read())
            return get_date
        except Exception as err:
            logger.error(err)
            return False

    def create_file(self):
        try:
            with open(remote_data_path,'w', encoding='UTF-8') as file:
                dict = {}
                json.dump(dict,file)
            return bool(file)
        except Exception as err:
            logger.error(err)
            return False

    def delete_file(self):
        if os.path.isfile(remote_data_path):
            os.remove(remote_data_path)
            return True
        else:
            logger.error("no such file ")
            return False

    def add_area(self,area):
        try:
            check_area = self.get_remote_data()
            if area not in check_area.keys():
                if type(check_area) == dict:
                    data = {area : []}
                    check_area.update(data)
                    with open(remote_data_path,'w', encoding='UTF-8') as file:
                        json.dump(check_area,file)
                    check_area_again = self.get_remote_data()
                    if area in check_area_again:
                        return True
                    else:
                        return False
                else:
                    logger.error("Remote_moudule.log format error")
            else:
                logger.error("%s alread exists" %area)
        except Exception as err:
            logger.error(err)
            return False

    def add_remote_info(self,area, alias, hostname, username, cert_type, port="22", cert_path="", cert_password=""):
        try:
            data = {"alias": alias,
                    "hostname": str(self.rsa_encrypt(hostname)),
                    "username": str(self.rsa_encrypt(username)),
                    "port": str(self.rsa_encrypt(port)),
                    "cert_type": str(self.rsa_encrypt(cert_type)),
                    "cert_path": str(self.rsa_encrypt(cert_path)),
                    "cert_password": str(self.rsa_encrypt(cert_password))
                    }
            check_area = self.get_remote_data()
            if area in check_area.keys():
                list_gather = []
                list_gather_index = 0
                if list_gather_index < len(check_area[area]):
                    while list_gather_index < len(check_area[area]):
                        list_gather.append(check_area[area][list_gather_index]["alias"])
                        list_gather_index = list_gather_index + 1
                    if alias in list_gather:
                        logger.info("%s alread exists" %alias)
                        return False
                    else:
                        in_data = check_area[area]
                        in_data.append(data)
                        with open(remote_data_path,'r', encoding='UTF-8') as write:
                            in_list = json.load(write)
                            with open(remote_data_path,'w', encoding='UTF-8') as write_data:
                                in_list[area] = in_data
                                json.dump(in_list,write_data)
                        check_alias_again = self.get_remote_data()
                        if check_alias_again[area][-1]['alias'] == alias:
                            logger.info("Add remote info Successfully ")
                            return True
                        else:
                            logger.error("Add remote info Failed")
                            return False
                else:
                    in_data = check_area[area]
                    in_data.append(data)
                    with open(remote_data_path, 'r', encoding='UTF-8') as write:
                        in_list = json.load(write)
                        with open(remote_data_path, 'w', encoding='UTF-8') as write_data:
                            in_list[area] = in_data
                            json.dump(in_list, write_data)
                    check_alias_again = self.get_remote_data()
                    if check_alias_again[area][-1]['alias'] == alias:
                        logger.info("Add remote info Successfully ")
                        return True
                    else:
                        logger.error("Add remote info Failed")
                        return False
            else:
                logger.error("%s does not exist" %area)
                return False
        except Exception as err:
            logger.error(err)
            return False

    def del_remote_info(self,area,alias):
        try:
            check_area = self.get_remote_data()
            list_gather_index = 0
            if list_gather_index < len(check_area[area]):
                while list_gather_index < len(check_area[area]):
                    if alias == check_area[area][list_gather_index]["alias"]:
                        del check_area[area][list_gather_index]
                        logger.info("del remote info Successfully ")
                    else:
                        list_gather_index = list_gather_index + 1
                        continue
            else:
                logger.info("%s does not exist" % alias)
                return False
        except Exception as err:
            logger.error(err)
            return False

    def get_remote_area_list(self):
        try:
            check_area = self.get_remote_data()
            if bool(check_area) == True:
                key_list = list(check_area.keys())
                return key_list
            else:
                logger.info("No have area")
                return False
        except Exception as err:
            logger.error(err)
            return False

    def get_remote_area_alias_list(self,area):
        try:
            check_area = self.get_remote_data()
            list_gather = []
            list_gather_index = 0
            if list_gather_index < len(check_area[area]):
                while list_gather_index < len(check_area[area]):
                    list_gather.append(check_area[area][list_gather_index]["alias"])
                    list_gather_index = list_gather_index + 1
                return list_gather
            else:
                logger.info("No have alias")
                return False
        except Exception as err:
            logger.error(err)
            return False


test = Remote_date_operate('1','2')
aa = test.rsa_encrypt('fdfdf')
#print(aa)
#print(test.rsa_decrypt(aa))
#print(test.create_file())
#print(test.add_area('default1'))
print(test.add_remote_info('default', "test3", "192.168.1.3", "root", "1", port="22", cert_path="./test.pem", cert_password="1"))
#print(test.delete_file())
#print(test.delete_file())
#print(test.create_rsa_key())
#print(test.get_remote_area_list())
#print(test.get_remote_area_alias_list('default'))
"""
print(test.get_remote_data_file_hash())
print(test.get_remote_data())
print(test.get_remote_data()['default'][0])
"""