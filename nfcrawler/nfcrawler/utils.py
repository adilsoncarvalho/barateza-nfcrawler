# -*- coding: utf-8 -*-

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

def save_to_file(self, file_name, content):
    has_body = getattr(content, 'body', None)
    if callable(has_body):
        content = content.body

    with open(file_name, 'w') as file:
        file.write(content)
