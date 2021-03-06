#coding=utf8
import sys

TRANSLATE = 'Chinese'

class ReturnValue(dict):
    ''' turn return value of itchat into a boolean value
    for requests:
        ..code::python

            import requests
            r = requests.get('http://httpbin.org/get')
            print(ReturnValue(rawResponse=r)
    
    for normal dict:
        ..code::python

            returnDict = {
                'BaseResponse': {
                    'Ret': 0,
                    'ErrMsg': 'My error msg', }, }
            print(ReturnValue(returnDict))
    '''
    def __init__(self, returnValueDict={}, rawResponse=None):
        if rawResponse:
            try:
                returnValueDict = rawResponse.json()
            except ValueError:
                returnValueDict = {
                    'BaseResponse': {
                        'Ret': -1004,
                        'ErrMsg': 'Unexpected return value', },
                    'Data': rawResponse.content, }
        for k, v in list(returnValueDict.items()):
            self[k] = v
        if not 'BaseResponse' in self:
            self['BaseResponse'] = {
                'ErrMsg': 'no BaseResponse in raw response',
                'Ret': -1000, }
        if TRANSLATE:
            self['BaseResponse']['RawMsg'] = self['BaseResponse'].get('ErrMsg', '')
            self['BaseResponse']['ErrMsg'] = \
                TRANSLATION[TRANSLATE].get(
                self['BaseResponse'].get('Ret', '')) \
                or self['BaseResponse'].get('ErrMsg', 'No ErrMsg')
            self['BaseResponse']['RawMsg'] = \
                self['BaseResponse']['RawMsg'] or self['BaseResponse']['ErrMsg']
    def __bool__(self):
        return self['BaseResponse'].get('Ret') == 0
    def __bool__(self):
        return self.__nonzero__()
    def __str__(self):
        return '{%s}' % ', '.join(
            ['%s: %s' % (repr(k),repr(v)) for k,v in list(self.items())])
    def __repr__(self):
        return '<ItchatReturnValue: %s>' % self.__str__()

TRANSLATION = {
    'Chinese': {
        -1000: '返回值不带BaseResponse',
        -1001: '无法找到对应的成员',
        -1002: '文件位置错误',
        -1003: '服务器拒绝连接',
        -1004: '服务器返回异常值',
        -1005: '参数错误',
        -1006: '无效操作',
        0: '请求成功',
    },
}
