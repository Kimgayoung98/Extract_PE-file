import os, pefile
import hashlib
import sys
import shutil

path = "C:\\"
username = str(os.getlogin())
dest = "C:\\Users\\"+username+"\\Desktop\\pelist\\pelist.txt"
file_dest = "C:\\Users\\"+username+"\\Desktop\\pelist\\pefiles\\"

cnt=0
list1 = []

def search(dirname): # 재귀
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                list1.append(full_filename)
    except PermissionError:
        pass

def search2(dirname): # os.walk 사용
    try:
        for (path, dir, files) in os.walk(dirname):
            for filename in files:
                list1.append(os.path.join(path, filename))
    except PermissionError:
        pass

search2(path)
f = open(dest, 'w', encoding='utf8')
for i in list1:
    f.write(i+'\n')
f.close()

def hashcalc(file):
    try:
        f = open(file, 'rb')
        data = f.read()
        hash=hashlib.sha256(data).hexdigest()
        f.close()
        return hash
    except Exception as e:
        exc_type, exc_obj, tb = sys.exc_info()
        print('[error line No = {}]'.format(tb.tb_lineno))
        print(e)
        return file+"1"

def find_pe():
    for z in list1:
        try:
            x=pefile.PE(z)
            if(hex(x.DOS_HEADER.e_magic) == "0x5a4d"):
                print(z, hex(x.DOS_HEADER.e_magic))
                print(dest+z)
                x.close()
                shutil.copy2(z, file_dest+str(hashcalc(z)))
        except Exception as e:
            exc_type, exc_obj, tb = sys.exc_info()
            print('[error line No = {}]'.format(tb.tb_lineno))
            print(e)
            continue


print("file list end")
find_pe()
