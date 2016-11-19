# -*- coding: utf-8 -*-
import re

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
