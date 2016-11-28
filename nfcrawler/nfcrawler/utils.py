# -*- coding: utf-8 -*-
import os
import re
import subprocess
import inspect
from unidecode import unidecode
from w3lib.html import remove_tags

def string_cleaner(str):
  return re.compile('\s+').sub(' ', unidecode(unicode.strip(remove_tags(str))))

def to_decimal(value):
  if value.strip() == "":
    return None
  else:
    return float(value.replace('.', '').replace(',', '.'))

def to_int(value):
  if value.strip() == "":
    return None
  else:
    return int(value)

def to_datetime(value):
  # u'10/11/2016 \n        \xe0s\n      18:19:22-02:00'
  # => u'10/11/2016                   18:19:22-02:00'
  datetime = re.compile('[^0-9:/-]').sub(' ', value)

  # u'10/11/2016                   18:19:22-02:00'
  # => u'10/11/2016 18:19:22-02:00'
  datetime = re.compile('\s+').sub(' ', datetime)

  # u'10/11/2016 18:19:22-02:00'
  # => u'2016-11-10T18:19:22-02:00'
  p = re.compile('(\d{2})/(\d{2})/(\d{4})\s+(\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2})').search(datetime)

  if p == None:
    return datetime
  else:
    p = p.groups()
    return p[2] + '-' + p[1] + '-' + p[0] + 'T'+p[3]

def save_to_file(self, file_name, content):
    has_body = getattr(content, 'body', None)
    if callable(has_body):
        content = content.body

    with open(file_name, 'w') as file:
        file.write(content)

def get_version(self):
  version_filename = get_version_file(self)
  if os.path.exists(version_filename):
    version = open(version_filename, 'r').read().strip()
  else:
    version = 'dev'
  return self.name + '/' + version

def get_version_file(self):
  return os.path.splitext(inspect.getfile(self.__class__))[0] + '.version'
