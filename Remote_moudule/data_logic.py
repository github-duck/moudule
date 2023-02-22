import hashlib
import json
from config import remote_data_path
from package import *
import os



remote_data_hash = ""
class Remote_date_operate:

    def __init__(self,user_rsa,user_aes):
        self.user_rsa = user_rsa
        self.user_aes = user_aes

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

    def add_remote_info(self,area, alias, hostname, username, cert_type, port=22, cert_path="", cert_password=""):
        try:
            check_area = self.get_remote_data()
            if area in check_area.keys():
                dict_index = 0
                while dict_index < len(check_area[area]):
                    if alias == check_area[area][dict_index][alias]:
                        logger.info("%s alread exists" % alias)
                        return True
                    else:






test = Remote_date_operate('1','2')
#print(test.create_file())
print(test.add_area('default1'))
#print(test.delete_file())
#print(test.delete_file())
"""
print(test.get_remote_data_file_hash())
print(test.get_remote_data())
print(test.get_remote_data()['default'][0])
"""