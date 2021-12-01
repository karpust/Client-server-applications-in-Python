"""Модуль error_handling_mechanisms"""

# обработка ошибки кодирования с заменой символа знаком вопроса
HANDL_ERR = 'Testování'
HANDL_ERR_BYTES = HANDL_ERR.encode('ascii', 'replace')
print('replace: ', HANDL_ERR_BYTES)

print('----------------------------------------------------')
# обработка ошибки кодирования с заменой символа его именем
HANDL_ERR_BYTES = HANDL_ERR.encode('ascii', 'namereplace')
print('namereplace: ', HANDL_ERR_BYTES)

print('----------------------------------------------------')
# игнорирование ошибки при кодировании
HANDL_UNICODE = 'Testování'
HANDL_BYTES = HANDL_UNICODE.encode('ascii', 'ignore')
print('ignore: ', HANDL_BYTES)

print('----------------------------------------------------')
# игнорирование ошибки при кодировании
HANDL_UNICODE = 'Testování'
HANDL_BYTES = HANDL_UNICODE.encode('ascii', 'xmlcharrefreplace')
print('xmlcharrefreplace: ', HANDL_BYTES)

print('----------------------------------------------------')
# игнорирование ошибки при декодировании
HANDL_STR = 'Testování'
HANDL_STR_BYTES = HANDL_STR.encode('utf-8')
print(HANDL_STR_BYTES)
HANDL_STR = HANDL_STR_BYTES.decode('ascii', 'ignore')
print('ignore: ', HANDL_STR)

print('----------------------------------------------------')
# замена ошибки при декодировании
HANDL_STR = 'Testování'
HANDL_STR_BYTES = HANDL_STR.encode('utf-8')
HANDL_STR = HANDL_STR_BYTES.decode('ascii', 'replace')
print('replace: ', HANDL_STR)

# какой вариант лучше?
