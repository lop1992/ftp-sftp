import os
import sys
import ftplib
import paramiko
from datetime import datetime
'''
这是一个自动化完成从ftp同步下载文件并实时用sftp上传文件到服务器的脚本。
<---刘志豪 www.136.om@qq.com --->


'''

FTP_HOST = '192.168.1.150'      #FTP服务器地址
FTP_HOST_NAME = 'lzh'           #账户名

FTP_PASSWORD = 'ts123456'       #密码
DOWNLOAD_FILE = 'C:\\Users\\LZH\\Desktop\\ftp'          #设置文件下载到本地的目录
LOG_PATH = 'C:\\Users\\LZH\\Desktop\\log\\'

SFTP_HOST = '192.168.1.150'     #主机
SFTP_PORT = 22                  #端口
SFTP_USER_NAME = 'lzh'          #用户名
SFTP_PASSWORD = 'ts123456'      #密码
SFTP_LOCAL_FILE = 'C:\\Users\\LZH\\Desktop\\ftp\\'      #本地目录
SFTP_REMOTE_FILE = '/'          #远程目录
F_S_LIST = []                   #定义一个列表，把服务器文件的文件名保存在列表中循环
F_U_LIST = []                   #定义一个列表，把同步过的文件文件名保存在列表中循环
F_D_LIST = []                   #定义一个列表，把下载过的文件文件名保存在列表中循环
F_C_LIST = []                   #定义一个列表，把上传过的文件文件名保存在列表中循环
DATE_NOW = datetime.now().date().isoformat()            #设置当天时间
DATE_MORE = datetime.now().strftime('%Y-%m-%d %H:%M')   #设置详细时间

try:
    ftp = ftplib.FTP(FTP_HOST)
except ftplib.error_perm:
        print('无法连接到FTP服务器：%s'%FTP_HOST)
print('#########################################\n 已经连接到FTP服务器：%s \n#########################################'%FTP_HOST)

def FTP_login():
    
    '''用于登陆FTP'''
    try:
        ftp.login(FTP_HOST_NAME,FTP_PASSWORD)
        ftp.set_debuglevel(0)                           #调试函数.0：不显示  1：显示  2：显示所有
    except ftplib.error_perm:
        print('登陆失败')

        logout()
        return
    print('\t\t登陆成功 \n#########################################\n')

def SENSE_file(filename):
    '''判断文件是否存在，如果不存在则创建，反之什么也不做。'''
    if not os.path.exists(LOG_PATH + filename):
        touchfile = open(LOG_PATH + filename,'a')
        touchfile.close()
    else:
        pass

def UPDATE_list(filename,LIST,rwa):
    '''更新存储文件名的列表，在下载，更新，同步都有引用'''
    with open(filename,rwa) as f:
        f.seek(0)
        for file in f.readlines():
            file = file.replace('\n','')                                 
            if file not in LIST:
                LIST.append(file)
            else:
                pass
   
def FTP_synchronization():
    '''同步FTP服务器上的文件(文件名)'''
    
    SENSE_file('ftp_server_file_list.txt')                                      #判断同步汇总文件是否存在
    SENSE_file(DATE_NOW + '_updata.txt')                                        #判断同步更新文件是否存在
    UPDATE_list(LOG_PATH +  'ftp_server_file_list.txt',F_S_LIST,'a+')           #更新同步服务器文件的列表
    with open(LOG_PATH +  'ftp_server_file_list.txt','a+') as file_server_list: #a代表以读写追加的方式打开文件，with open...可以不用close文件
        for suml in ftp.nlst():                                                 #把FTP服务器的文件遍历并添加到filelog文件下
            if suml in F_S_LIST:
                pass
            else :
                file_server_list.write(suml +'\n')
                with open(LOG_PATH+(DATE_NOW)+'_updata.txt','a') as f_updata:
                    f_updata.write(suml+'\n')
                    
def FTP_download():
    '''在ftp服务器下载文件'''
                                                                                
    os.chdir(DOWNLOAD_FILE)                                                     #切换到下载的目录
    SENSE_file((DATE_NOW) + '_D_log.txt')
    SENSE_file((DATE_NOW) + '_down.txt')                                        #判断文件是否存在
    UPDATE_list(LOG_PATH + DATE_NOW + '_updata.txt',F_U_LIST,'r')        
    UPDATE_list(LOG_PATH + DATE_NOW + '_down.txt',F_D_LIST,'r')
    
    for suml in F_U_LIST:
        if suml in F_D_LIST:
            pass
        else:
            ftp.retrbinary('RETR %s'%suml,open(suml,'wb').write)
            
            with open(LOG_PATH + DATE_NOW + '_down.txt','a') as f_downup:
                f_downup.write(suml+'\n')
                
            with open(LOG_PATH + DATE_NOW + '_D_log.txt','a') as f_log:
               print('%s <--*-->成功下载文件<--*-->  %s'%(DATE_MORE,suml),file=f_log)
    
def SFTP_upload():
    '''完成sftp文件上传功能'''
    SENSE_file((DATE_NOW) + '_C_log.txt')
    sf = paramiko.Transport((SFTP_HOST,SFTP_PORT))
    sf.connect(username = SFTP_USER_NAME,password = SFTP_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(sf)
    
    SENSE_file((DATE_NOW) + '_commit.txt')
    UPDATE_list(LOG_PATH+(DATE_NOW)+'_commit.txt',F_C_LIST,'r')
    for suml in F_D_LIST:
        if suml in F_C_LIST:
            pass
        else:
            sftp.put(SFTP_LOCAL_FILE + suml,SFTP_REMOTE_FILE + suml)            #上传文件
            #print('文件%s 上传成功\n'%(os.path.join(SFTP_LOCAL_FILE,suml)))
                        
            with open(LOG_PATH + DATE_NOW + '_commit.txt','a') as f_commit:
                f_commit.write(suml+'\n')
                            
            with open(LOG_PATH + DATE_NOW + '_C_log.txt','a') as f_log:
               print('%s <--*-->成功上传文件<--*-->  %s'%(DATE_MORE,suml),file=f_log)
    
    #sf.close()

def FTP_logout():
    '''退出登陆FTP'''
    ftp.quit()

if __name__ == '__main__':
    '''主函数'''
    FTP_login()

    while True:

        FTP_synchronization()

        FTP_download()

        SFTP_upload()
