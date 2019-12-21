#!/usr/bin/env python
import paramiko
import sys
import zipfile,os
import logging
import datetime
logging.basicConfig(filename='log/file_transfer.log', level=logging.DEBUG)

HOST = '127.0.0.1'
PORT = 2222 # SFTPのポート
USER = 'vagrant'
KEY_FILE = '/Users/tomoki/vagrant/ubunt_server/.vagrant/machines/default/virtualbox/private_key' # 秘密鍵ファイル

# 秘密鍵ファイルからキーを取得
rsa_key = paramiko.RSAKey.from_private_key_file(KEY_FILE)

# 秘密鍵ファイルにパスフレーズを設定している場合は下記
# PASSPHRASE = 'passphrase'
# rsa_key = paramiko.RSAKey.from_private_key_file(KEY_FILE, PASSPHRASE)

args = sys.argv

current_time = datetime.datetime.today()
print("現在時刻："+str(current_time))
print("転送ファイル名：" + args[1])
#os.chdir('/Users/tomoki/dev2')
zip_f_name = str(args[1])+".zip"

# 圧縮するファイルのディレクトリへ移動
#os.chdir('C:\\user1\\data')

# ZIPファイルを作成/ZIPファイルに追加
with zipfile.ZipFile(zip_f_name,'w') as zip_f:
    zip_f.write(args[1], compress_type=zipfile.ZIP_DEFLATED)


print(zip_f_name)

local_path = zip_f_name
remote_path = "/home/vagrant/files/"+current_time.strftime("%Y%m%d_%H%M%S")+"/"


def main(local_file,remote_file):
    """
    SFTPでファイル転送
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, PORT, USER, pkey=rsa_key) # キーを指定することでパスワードは必要なし
        sftp = client.open_sftp()
        sftp.mkdir(remote_path)
        sftp.put(local_file,remote_file+zip_f_name)
        print("転送完了")

    except Exception as e:
        logging.error(e)
        print(e)
        print("転送失敗")

    finally:
        sftp.close()
        client.close()

if __name__ == "__main__":
    main(local_path,remote_path)