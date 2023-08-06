#!/usr/bin/env python3

#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# Class:   Encryption
#──────────────────────────
# Author:  Hengyue Li
#──────────────────────────
# Version: 2018/11/17
#──────────────────────────
# discription:
#
#         The key of the dict can not be numeric type. String only.
#
#
#
#         The Dict MUST contains a element of FILE_DB_CONFIG (dict)
#
#         FILE_DB_CONFIG:{password: }
#         FILE_DB_TABLE:{ }
#
#──────────────────────────
# Used :
import json,hashlib,base64,os,inspect,functools
from Crypto import Random
from Crypto.Cipher import AES
import hashlib
#──────────────────────────
# Interface:
#
#        [ini] path,key
#
#        [sub] connect()
#              make connect to the filedict.
#              If the file exists, load the data (with the key).
#              If not, create one with the key
#
#        [fun] IsConnected()
#
#        [sub] CreateTableIfNotExist(TableName)
#              if it is already existed, do nonthing
#
#        [fun] GetTableList():
#              return dictkey type
#
#        [fun] GetTable(TableName)
#              return a normal python dict
#
#        [sub] DropTable(TableName)
#              if the table does not exist, do nothing.
#
#        [sub] SetPassword(password)
#              set a new password to filedict
#
#        [sub] Save()
#              save data into file.
#
#        [fun] LoadFileToDict(filepath,key = '')
#                  read a file to dict
#
#
#        [fun] GetFolderPath()
#
#        [fun] GetFilePath()
#
#        [fun] SaveDecryptedDataToFile(FilePath)
#              save all data (dict) into a file. Careful to use this procedure
#
#        [fun] ReadDecryptedDataFile(FilePath)
#              The inverse action of 'SaveDecryptedDataToFile'.
#              When load a new file, the current data file is overried.
#
#
#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════



class Encryption():


    class AESCipher(object):
    #-------------------------------------
    #https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
        def __init__(self, key):
            self.bs = 32
            self.key = hashlib.sha256(key.encode()).digest()

        def encrypt(self, raw):
            raw = self._pad(raw)
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return base64.b64encode(iv + cipher.encrypt(raw.encode('utf-8')))

        def decrypt(self, enc):
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

        def _pad(self, s):
            return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

        @staticmethod
        def _unpad(s):
            return s[:-ord(s[len(s)-1:])]

    @staticmethod
    def GetFilePath():
        return os.path.realpath(__file__)

    @classmethod
    def GetFolderPath(cls):
        f = cls.GetFilePath()
        return os.path.dirname(f)



    #----------------------------------------------

    def __init__(self,path,key=''):
        self.path          = path
        self.key           = key
        self.__Dict        = {}
        self.__isconnected = False
        self.__needstage   = False

    def IsConnected(self):
        return self.__isconnected

    def connect(self):
        if os.path.isfile(self.path):
            self.__Dict = self.LoadFileToDict(self.path,self.key)
            if self.__Dict is None:
                # raise Exception('Invalid DB file or key error!')
                self.__isconnected = False
            else:
                self.__isconnected = True
        else:
            self.__isconnected = True
            self.__Dict = self.__InitiateFile(self.path,self.key)

    def __IsconnectCheck(f):
        @functools.wraps(f)
        def decorated(*args,**kwargs):
            self = args[0]
            if self.IsConnected():
                return f(*args,**kwargs)
            else:
                print("@function '{}', filedict is not connected".format(inspect.stack()[1][3]))
                raise PermissionError('Filedict is not connected.')
        return decorated



    @__IsconnectCheck
    def SetPassword(self,password):
        self.__Dict['FILE_DB_CONFIG']['password'] = password
        self.__needstage = True



    @__IsconnectCheck
    def CreateTableIfNotExist(self,TableName):
        if TableName not in self.__Dict['FILE_DB_TABLE']:
            self.__Dict['FILE_DB_TABLE'][TableName] = {}
            self.__needstage = True
        else:
            print('table existed.Do nothing')


    @__IsconnectCheck
    def DropTable(self,TableName):
        if TableName in self.__Dict['FILE_DB_TABLE']:
            del self.__Dict['FILE_DB_TABLE'][TableName]
            self.__needstage = True

    @__IsconnectCheck
    def GetTableList(self):
        return self.__Dict['FILE_DB_TABLE'].keys()






    @__IsconnectCheck
    def GetTable(self,TableName):
        return self.__Dict['FILE_DB_TABLE'].get(TableName,None)



    # def SaveToDB(self):
    #     self.__SaveDictToFile(self.path,self.__Dict)



    # def NotConnectedError(self):
    #     if not self.__isconnected:
    #         print("DB is not connected, function '{}' is not callable".format(inspect.stack()[1][3]))


    @__IsconnectCheck
    def Save(self):
        # self.NotConnectedError()
        self.__SaveDictToFile( self.path , self.__Dict )


    @__IsconnectCheck
    def CreateTable(self,TableName):
        self.NotConnectedError()
        if TableName in self.__Dict:
            print('{} is existed in DB'.format(TableName))
            exit()
        else:
            self.__Dict[TableName] = {}



    @classmethod
    def LoadFileToDict(cls,filepath,key = ''):
        reader = cls.AESCipher(key)
        f = open(filepath,'rb')
        Estr = f.read()
        f.close()
        try:
            #----------------
            # 20200425
            checkLen = 5
            Estr = Estr.decode('utf-8')
            CheckMD5 = Estr[0:checkLen]
            PureData = Estr[checkLen:]
            if hashlib.md5( PureData.encode('utf-8') ).hexdigest()[0:checkLen] != CheckMD5:
                return None
            Estr = PureData.encode('utf-8')
            #----------------
            getString = reader.decrypt(Estr)
            d = json.loads(getString)
            if d['FILE_DB_CONFIG']['password'] == key:
                return d
        except:
            return None
        return None



   # [sub] __SaveDictToFile(filepath,Dict)
   #           save a dict to file.
    @classmethod
    def __SaveDictToFile(cls,filepath,Dict):
        jStr   = json.dumps(Dict)
        key    = Dict['FILE_DB_CONFIG']['password']
        reader = cls.AESCipher(key)
        Estr   = reader.encrypt(jStr)
        #----------------
        # 20200425
        checkLen = 5
        Estr = Estr.decode('utf-8')
        CheckMD5 = hashlib.md5( Estr.encode('utf-8') ).hexdigest()[0:checkLen]
        TotStr = CheckMD5 + Estr
        Estr = TotStr.encode('utf-8')
        #----------------
        tpfile = filepath+'.tmp'
        f = open(tpfile,'wb')
        f.write(Estr)
        f.close()
        try:
            os.remove(filepath)
        except:
            pass
        os.rename(tpfile,filepath)





   #
   # [sub] __InitiateFile(filepath,key):
   #           initiate a data file with a key
    @classmethod
    def __InitiateFile(cls,filepath,key=''):
        d = {  'FILE_DB_CONFIG':{ 'password':key    }  , 'FILE_DB_TABLE':{}   }
        cls.__SaveDictToFile(filepath,d)
        return d


    @__IsconnectCheck
    def SaveDecryptedDataToFile(self,FilePath):
        jStr   = json.dumps(self.__Dict)
        open(FilePath,'w').write(jStr)

    def ReadDecryptedDataFile(self,FilePath):
        Estr = open(FilePath,'r').read()
        DICT = json.loads(Estr)
        self.__Dict = DICT
        self.Save()




# #-----------------------------------------------------
# # create a new filedict (with password = 'password')
# container = Encryption('encrypted.dat','password')
# container.connect()
# # a file is created. One can check the context in it.






# #-----------------------------------------------------
# # connect to a filedict
# container = Encryption('encrypted.dat','password')
# container.connect()
# print(container.IsConnected())
# # a filedict is connect. One can try another password.







# #-----------------------------------------------------
# # create a table
# container = Encryption('encrypted.dat','password')
# container.connect()
# container.CreateTableIfNotExist('testTable')
# # remenber to save it
# container.Save()




# #-----------------------------------------------------
# # get all the tables in container
# container = Encryption('encrypted.dat','password')
# container.connect()
# # return a python dict 'dict_keys' type
# l = container.GetTableList()
# print(l)




# #-----------------------------------------------------
# # get a normal python dict in the container so one can interact with it
# container = Encryption('encrypted.dat','password')
# container.connect()
# d = container.GetTable('testTable')
# print(type(d),d)
# # ---  inser an element
# d['new'] = 'hellow'
# # remenber to save it
# container.Save()



# #-----------------------------------------------------
# # remove a table
# container = Encryption('encrypted.dat','password')
# container.connect()
# container.DropTable('testTable')
# # remenber to save it
# container.Save()







# #-----------------------------------------------------
# # reset password
# container = Encryption('encrypted.dat','password')
# container.connect()
# container.SetPassword('newpassword')
# # remenber to save it
# container.Save()
# # the container itself is already renewed
# print( container.IsConnected() )






#
# # print(f.GetFolderPath())
# g = f.GetTable('x')
# print(g)
# #
# #
# #
# # print(f.__Dict)
# #
#
# # f.CreateTableIfNotExist('MyPasswordManeger')
# #
# # f.SaveToDB()




# f = Encryption('test.db','123')
# f.connect()
#
# f.CreateTableIfNotExist('t1')
# f.CreateTableIfNotExist('t2')
# f.CreateTableIfNotExist('t3')
