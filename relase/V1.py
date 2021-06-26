import os
import sys
import ftplib
from datetime import datetime
import traceback

SYNCDIR="/root/test/sync/"
SYNC_LOG_DIR="/root/test/sync/log/"


class transfer(object):
   
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
                
    def synchronization(self):
        '''同步FTP服务器上的文件(文件名)'''
        
        self.SENSE_file('ftp_server_file_list.txt')                                     #判断同步汇总文件是否存在
        self.SENSE_file(datetime.now().date().isoformat() + '_updata.txt')              #判断同步更新文件是否存在
        self.UPDATE_list(self.LOG_PATH +  'ftp_server_file_list.txt',self.F_S_LIST,'a+')#更新同步服务器文件的列表
        with open(self.LOG_PATH +  'ftp_server_file_list.txt','a+') as file_server_list:#a代表以读写追加的方式打开文件，with open...可以不用close文件
            for suml in self.ftp.nlst():                                                #把FTP服务器的文件遍历并添加到filelog文件下
                if suml in self.F_S_LIST:
                    pass
                else :
                    file_server_list.write(suml + '\n')
                    with open(self.LOG_PATH+(datetime.now().date().isoformat())+'_updata.txt','a') as f_updata:
                        f_updata.write(suml + '\n')
						
class Myftp(transfer):
	
    def __init__(self,FTP_HOST,port,FTP_USER_NAME,FTP_PASSWORD):
	
        self.ftp = ftplib.FTP()
        self.port = port
        self.FTP_PASSWORD = FTP_PASSWORD                            #密码
        self.FTP_USER_NAME = FTP_USER_NAME                          #账户名
        self.FTP_HOST = FTP_HOST                                    #FTP服务器地址
        self.DOWNLOAD_FILE = SYNCDIR       #设置文件保存的目录
        self.LOG_PATH = SYNC_LOG_DIR            #设置日志保存的路径
	
        self.F_S_LIST = []                                          #定义一个列表，把服务器文件的文件名保存在列表中循环
        self.F_U_LIST = []                                          #定义一个列表，把同步过的文件文件名保存在列表中循环
        self.F_D_LIST = []                                          #定义一个列表，把下载过的文件文件名保存在列表中循环
	
    def connect(self):
        '''连接到ftp服务器，并实例化ftp。'''
		
        try:
            self.ftp.connect(self.FTP_HOST,self.port)
        except ftplib.error_perm:
            print('无法连接到FTP服务器：%s'%self.FTP_HOST)
        print('#'*77)
        print('\t\t\t已经连接到FTP服务器：%s'%self.FTP_HOST)
        print('#'*77)
	
    def login(self):
        '''用于登陆FTP'''
		
        try:
            self.ftp.login(self.FTP_USER_NAME,self.FTP_PASSWORD)
            self.ftp.encoding = 'GB18030'
            self.ftp.set_debuglevel(0)                              #调试函数.0：不显示  1：显示  2：显示所有
        except ftplib.error_perm:
            print('登陆失败')
            logout()
            return
        print('\t\t\t\t登陆成功')
        print('#'*77)	
		
    def download(self):
        '''在ftp服务器下载文件'''
                                                                                    
        os.chdir(self.DOWNLOAD_FILE)                                                    #切换到下载的目录
        #self.SENSE_file(datetime.now().date().isoformat() + '_D_log.txt')
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
                    
                #with open(self.LOG_PATH + datetime.now().date().isoformat() + '_D_log.txt','a') as f_log:
                #   print('%s <--*-->成功下载文件<--*-->  %s'%(datetime.now().strftime('%Y-%m-%d %H:%M'),suml),file=f_log)
                   
    def q(self):
        self.ftp.quit()

if __name__ == '__main__':
    '''主函数'''

    ftp = Myftp('1111.111.111.111', 23, '12','12')
     
    ftp.connect()
    ftp.login()
    #sftp.login()

    ftp.synchronization()
    try:
        ftp.download()
    except Exception as e:
        print('traceback.format_exc():\n%s' % traceback.format_exc())
    ftp.q()
    
    #while True:

    #    ftp.synchronization()

      #  ftp.download()

       # sftp.upload()
       
 

