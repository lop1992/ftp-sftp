import os
import sys
import ftplib
import paramiko
from datetime import datetime

class transfer(object):
    
    def __init__(self):

        self.ftp = '' 
        self.FTP_PASSWORD = 'ts123456'                              #密码
        self.FTP_HOST_NAME = 'lzh'                                  #账户名
        self.FTP_HOST = '192.168.1.150'                             #FTP服务器地址
        self.DOWNLOAD_FILE = 'C:\\Users\\LZH\\Desktop\\ftp\\'       #设置文件保存的目录
        self.LOG_PATH = 'C:\\Users\\LZH\\Desktop\\log\\'            #设置日志保存的路径

        self.sftp = ''
        self.SFTP_HOST = '192.168.1.150'                            #主机
        self.SFTP_PORT = 22                                         #端口
        self.SFTP_PASSWORD = 'ts123456'                             #密码
        self.SFTP_USER_NAME = 'lzh'                                 #用户名
        self.SFTP_REMOTE_FILE = '/'                                 #远程目录

        self.F_S_LIST = []                                          #定义一个列表，把服务器文件的文件名保存在列表中循环
        self.F_U_LIST = []                                          #定义一个列表，把同步过的文件文件名保存在列表中循环
        self.F_D_LIST = []                                          #定义一个列表，把下载过的文件文件名保存在列表中循环
        self.F_C_LIST = []                                          #定义一个列表，把上传过的文件文件名保存在列表中循环
        
    def FTP_connect(self):
        '''连接到ftp服务器，并实例化ftp。'''

        try:
            self.ftp = ftplib.FTP(self.FTP_HOST)
        except ftplib.error_perm:
            print('无法连接到FTP服务器：%s'%self.FTP_HOST)
        print('#'*77)
        print('\t\t\t已经连接到FTP服务器：%s'%self.FTP_HOST)
        print('#'*77)
    def FTP_login(self):
    
        '''用于登陆FTP'''
        try:
            self.ftp.login(self.FTP_HOST_NAME,self.FTP_PASSWORD)
            self.ftp.set_debuglevel(0)                              #调试函数.0：不显示  1：显示  2：显示所有
        except ftplib.error_perm:
            print('登陆失败')
            logout()
            return
        print('\t\t\t\t登陆成功')
        print('#'*77)


    def SFTP_login(self):
        '''完成sftp文件上传功能'''
        
        sf = paramiko.Transport(self.SFTP_HOST,self.SFTP_PORT)
        sf.connect(username = self.SFTP_USER_NAME,password = self.SFTP_PASSWORD)
        self.sftp = paramiko.SFTPClient.from_transport(sf)
    
    def SENSE_file(self,filename):
        '''判断文件是否存在，如果不存在则创建，反之什么也不做。'''

        if not os.path.exists(self.LOG_PATH + filename):
            touchfile = open(self.LOG_PATH + filename,'a')
            touchfile.close()
        else:
            pass

    def UPDATE_list(self,listfilename,LIST,power):
        '''更新存储文件名的列表，在下载，更新，同步都有引用'''

        with open(listfilename,power) as f:
            f.seek(0)
            for file in f.readlines():
                file = file.replace('\n','')                                 
                if file not in LIST:
                    LIST.append(file)
                else:
                    pass
     
    def FTP_synchronization(self):
        '''同步FTP服务器上的文件(文件名)'''
        
        self.SENSE_file('ftp_server_file_list.txt')                                     #判断同步汇总文件是否存在
        self.SENSE_file(datetime.now().date().isoformat() + '_updata.txt')                                  #判断同步更新文件是否存在
        self.UPDATE_list(self.LOG_PATH +  'ftp_server_file_list.txt',self.F_S_LIST,'a+')#更新同步服务器文件的列表
        with open(self.LOG_PATH +  'ftp_server_file_list.txt','a+') as file_server_list:#a代表以读写追加的方式打开文件，with open...可以不用close文件
            for suml in self.ftp.nlst():                                                #把FTP服务器的文件遍历并添加到filelog文件下
                if suml in self.F_S_LIST:
                    pass
                else :
                    file_server_list.write(suml +'\n')
                    with open(self.LOG_PATH+(datetime.now().date().isoformat())+'_updata.txt','a') as f_updata:
                        f_updata.write(suml+'\n')

    def FTP_download(self):
        '''在ftp服务器下载文件'''
                                                                                    
        os.chdir(self.DOWNLOAD_FILE)                                                    #切换到下载的目录
        self.SENSE_file(datetime.now().date().isoformat() + '_D_log.txt')
        self.SENSE_file(datetime.now().date().isoformat() + '_down.txt')                                    #判断文件是否存在
        self.UPDATE_list(self.LOG_PATH + datetime.now().date().isoformat() + '_updata.txt',self.F_U_LIST,'r')        
        self.UPDATE_list(self.LOG_PATH + datetime.now().date().isoformat() + '_down.txt',self.F_D_LIST,'r')
        
        for suml in self.F_U_LIST:
            if suml in self.F_D_LIST:
                pass
            else:
                self.ftp.retrbinary('RETR %s'%suml,open(suml,'wb').write)
                print('%s 文件%s 下载成功\n'%(datetime.now().strftime('%Y-%m-%d %H:%M'),suml))
                with open(self.LOG_PATH + datetime.now().date().isoformat() + '_down.txt','a') as f_downup:
                    f_downup.write(suml+'\n')
                    
                with open(self.LOG_PATH + datetime.now().date().isoformat() + '_D_log.txt','a') as f_log:
                   print('%s <--*-->成功下载文件<--*-->  %s'%(datetime.now().strftime('%Y-%m-%d %H:%M'),suml),file=f_log)
        
    def SFTP_upload(self):
        '''完成sftp文件上传功能'''
    
        self.SENSE_file(datetime.now().date().isoformat() + '_C_log.txt')
        self.SENSE_file(datetime.now().date().isoformat() + '_commit.txt')
        self.UPDATE_list(self.LOG_PATH + datetime.now().date().isoformat() + '_commit.txt',self.F_C_LIST,'r')
        for suml in self.F_D_LIST:
            if suml in self.F_C_LIST:
                pass
            else:
                self.sftp.put(self.DOWNLOAD_FILE + suml,(self.SFTP_REMOTE_FILE + suml).encode("gbk"))#上传文件,gbk为win默认编码
                print('%s 文件%s 上传成功\n'%(datetime.now().strftime('%Y-%m-%d %H:%M'),suml))
                            
                with open(self.LOG_PATH + datetime.now().date().isoformat() + '_commit.txt','a') as f_commit:
                    f_commit.write(suml+'\n')
                print(datetime.now().strftime('%Y-%m-%d %H:%M'))               
                with open(self.LOG_PATH + datetime.now().date().isoformat() + '_C_log.txt','a') as f_log:
                   print('%s <--*-->成功上传文件<--*-->  %s'%(datetime.now().strftime('%Y-%m-%d %H:%M'),suml),file=f_log)       

if __name__ == '__main__':
    '''主函数'''

    Tecsun = transfer()
    Tecsun.FTP_connect()
    Tecsun.FTP_login()
    Tecsun.SFTP_login()

    while True:

        Tecsun.FTP_synchronization()

        Tecsun.FTP_download()

        Tecsun.SFTP_upload()
