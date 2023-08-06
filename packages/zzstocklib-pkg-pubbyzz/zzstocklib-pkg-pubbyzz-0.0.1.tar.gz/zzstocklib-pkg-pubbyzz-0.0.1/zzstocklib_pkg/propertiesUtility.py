# -*- coding:utf-8 -*-
import re
import os
import tempfile


class Properties:
    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        if os.path.exists(file_name):
            with open(file_name) as f:
                for line in f:
                    tline = line.strip()
                    if tline.startswith('#'):
                        continue
                    else:
                        kv_list = tline.split('=', 2)
                        if not kv_list or len(kv_list) != 2:
                            continue
                        else:
                            value_list = kv_list[1].strip().split(',')
                            if not value_list:
                                continue
                            else:
                                if len(value_list) == 1:
                                    self.properties[kv_list[0].strip()] = value_list[0].strip()
                                else:
                                    temp = []
                                    for v in value_list:
                                        temp.append(v.strip())
                                    self.properties[kv_list[0].strip()] = temp
        else:
            raise Exception("file %s not found" % file_name)

    def get(self, key):
        if key in self.properties:
            return self.properties[key]
        return ''

    def get_list(self, key):
        if key in self.properties:
            temp = self.properties[key]
            if isinstance(temp, list):
                return temp
            else:
                return [temp]
        return []

    def get_num(self, key):
        if key in self.properties:
            return float(self.properties[key])
        return 0

path = os.path.split(os.path.realpath(__file__))[0]
config_file_path = os.path.join(path, 'config/global.properties')  # 存放log文件的路径
properties = Properties(config_file_path)
#print(properties.get('notification_queue_name'))
