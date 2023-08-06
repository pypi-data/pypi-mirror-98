import codecs
import time, os, sys
import shutil
import glob

'''

# os 模块

os.sep 可以取代操作系统特定的路径分隔符。windows下为 '\\'
os.name 字符串指示你正在使用的平台。比如对于Windows，它是'nt'，而对于Linux/Unix用户，它是 'posix'
os.getcwd() 函数得到当前工作目录，即当前Python脚本工作的目录路径
os.getenv() 获取一个环境变量，如果没有返回none
os.putenv(key, value) 设置一个环境变量值
os.listdir(path) 返回指定目录下的所有文件和目录名
os.remove(path) 函数用来删除一个文件
os.system(command) 函数用来运行shell命令
os.linesep 字符串给出当前平台使用的行终止符。例如，Windows使用 '\r\n'，Linux使用 '\n' 而Mac使用 '\r'
os.path.split(path)  函数返回一个路径的目录名和文件名
os.path.isfile() 和os.path.isdir()函数分别检验给出的路径是一个文件还是目录
os.path.exists() 函数用来检验给出的路径是否真地存在
os.curdir  返回当前目录 ('.')
os.mkdir(path) 创建一个目录
os.makedirs(path) 递归的创建目录
os.chdir(dirname) 改变工作目录到dirname    
os.path.getsize(name) 获得文件大小，如果name是目录返回0L
os.path.abspath(name) 获得绝对路径
os.path.normpath(path) 规范path字符串形式
os.path.splitext()  分离文件名与扩展名
os.path.join(path,name) 连接目录与文件名或目录
os.path.basename(path) 返回文件名
os.path.dirname(path) 返回文件路径
os.walk(top,topdown=True,onerror=None)  遍历迭代目录
os.rename(src, dst)  重命名file或者directory src到dst 如果dst是一个存在的directory, 将抛出OSError. 在Unix, 如果dst在存且是一个file, 如果用户有权限的话，它将被安静的替换. 操作将会失败在某些Unix 中如果src和dst在不同的文件系统中. 如果成功, 这命名操作将会是一个原子操作 (这是POSIX 需要). 在 Windows上, 如果dst已经存在, 将抛出OSError，即使它是一个文件. 在unix，Windows中有效。
os.renames(old, new) 递归重命名文件夹或者文件。像rename()
# shutil 模块

shutil.copyfile( src, dst) 从源src复制到dst中去。当然前提是目标地址是具备可写权限。抛出的异常信息为IOException. 如果当前的dst已存在的话就会被覆盖掉
shutil.move( src, dst)  移动文件或重命名
shutil.copymode( src, dst) 只是会复制其权限其他的东西是不会被复制的
shutil.copystat( src, dst) 复制权限、最后访问时间、最后修改时间
shutil.copy( src, dst)  复制一个文件到一个文件或一个目录
shutil.copy2( src, dst)  在copy上的基础上再复制文件最后访问时间与修改时间也复制过来了，类似于cp –p的东西
shutil.copy2( src, dst)  如果两个位置的文件系统是一样的话相当于是rename操作，只是改名；如果是不在相同的文件系统的话就是做move操作
shutil.copytree( olddir, newdir, True/Flase)
把olddir拷贝一份newdir，如果第3个参数是True，则复制目录时将保持文件夹下的符号连接，如果第3个参数是False，则将在复制的目录下生成物理副本来替代符号连接
shutil.rmtree( src ) 递归删除一个目录以及目录内的所有内容

'''


# 递归删除文件夹
def removerf(src):
    shutil.rmtree(src)


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print(path + ' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')

        return False


def getCurrentDirAbsPath():
    abspath = os.path.dirname(os.path.abspath(sys.argv[0]))
    return abspath


#########start 获取文件路径、文件名、后缀名############
def get_filePath_fileName_fileExt(filename):
    (filepath, tempfilename) = os.path.split(filename);
    (shotname, extension) = os.path.splitext(tempfilename);
    return filepath, shotname, extension


# 获取所有文件路径列表
def getAllFilesInDir(basedir):
    L = []
    for root, dirs, files in os.walk(basedir):
        for file in files:
            L.append(os.path.join(root, file))
    return L


# 获取所有子目录路径列表
def getAllDirsInDir(basedir):
    L = []
    for root, dirs, files in os.walk(basedir):
        for dir in dirs:
            L.append(os.path.join(root, dir))
    return L


# 获取文件夹大小
def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size


# 根据后缀名获取所有文件路径列表
def getAllFilesInDirByExt(basedir, ext):
    L = []
    for root, dirs, files in os.walk(basedir):
        for file in files:
            if os.path.splitext(file)[1] == ext:
                L.append(os.path.join(root, file))
    return L


# 删除目录中直接的文件
def removeFileInFirstDir(targetDir):
    for file in os.listdir(targetDir):
        targetFile = os.path.join(targetDir, file)
        if os.path.isfile(targetFile):
            os.remove(targetFile)


# 目录拷贝
def copyDir(sourceDir, targetDir):
    if sourceDir.find(".svn") > 0:
        return
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, file)
        targetFile = os.path.join(targetDir, file)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or (
                        os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())
        if os.path.isdir(sourceFile):
            First_Directory = False
            copyDir(sourceFile, targetFile)


def remove_empty_files_dirs(path):
    """
    CLean empty files, 清理空文件夹和空文件
    :param path: 文件路径，检查此文件路径下的子文件
    :return: None
    """
    files = os.listdir(path)  # 获取路径下的子文件(夹)列表
    for file in files:
        print('Traversal at', file)
        if os.path.isdir(file):  # 如果是文件夹
            if not os.listdir(file):  # 如果子文件为空
                os.rmdir(file)  # 删除这个空文件夹
        elif os.path.isfile(file):  # 如果是文件
            if os.path.getsize(file) == 0:  # 文件大小为0
                os.remove(file)  # 删除这个文件
    print(path, 'Dispose over!')


# 读取文件内容
def read_text(filepath):
    file_object = open(filepath)
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close()
    return all_the_text


# 读取文件内容，建议用这个
def read_content(filepath, charset='utf-8'):
    file_object = codecs.open(filepath, "r", charset)
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close()
    return all_the_text


# 读取文本文件所有行
def read_all_lines(filepath, charset='utf-8'):
    file_object = codecs.open(filepath, "r", charset)
    try:
        list_of_all_the_lines = file_object.readlines()
    finally:
        file_object.close()
    return list_of_all_the_lines


# 限制每次读行大小，callback中传的读出的行
def read_lines_limit_size(filepath, size_kb, line_func):
    file = open(filepath, 'r')
    sizehint = size_kb * 1024  # 200M
    position = 0
    lines = file.readlines(sizehint)
    while not file.tell() - position < 0:
        line_func(lines)
        # 继续读下一批
        position = file.tell()
        lines = file.readlines(sizehint)


# 写文件
def write_file(filepath, content):
    fw = codecs.open(filepath, "w", "utf-8")
    # html = unicode(html, "utf-8")
    fw.write(content)
    fw.close()


# 写入每行组成的列表
def write_file_txt_list(filepath, list):
    fw = codecs.open(filepath, 'w')
    fw.writelines(list)
    fw.close()


# 追加文件
def append_file(filepath, content, encoding='utf-8'):
    if not os.path.exists(filepath):
        fw = codecs.open(filepath, 'w', encoding)
        fw.close()
    fw = codecs.open(filepath, 'a', encoding)
    fw.write(content)
    fw.write(os.linesep)
    fw.close()


# 创建文件，如果不存在才创建
def create_file(filepath, encoding='utf-8'):
    if not os.path.exists(filepath):
        fw = codecs.open(filepath, 'w', encoding)
        fw.close()


'''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


'''获取文件的大小,结果保留两位小数，单位为MB'''


def get_FileSize(filePath):
    # filePath = unicode(filePath, 'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


'''获取文件的访问时间'''


def get_FileAccessTime(filePath):
    # filePath = unicode(filePath, 'utf8')
    t = os.path.getatime(filePath)
    return TimeStampToTime(t)


'''获取文件的创建时间'''


def get_FileCreateTime(filePath):
    # filePath = unicode(filePath, 'utf8')
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


'''获取文件的修改时间'''


def get_FileModifyTime(filePath):
    # filePath = unicode(filePath, 'utf8')
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)


# 用于判断文件后缀
# allowed_extensions=set(['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF'])
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


# 支持正则表达式 '/Volumes/Public/5演讲/xs金融(18.12.10完结)/6月/*/*.mp3'
def find_files(path_rule, recursive=False):
    files1 = glob.glob(path_rule, recursive=recursive)
    return files1


# 检查文本是否在文件中
def is_in_file(filePath, match_content):
    if not os.path.exists(filePath):
        return False
    content = read_content(filePath)
    if content and content.find(match_content) > -1:
        return True
    return False


def is_exsit(file):
    return os.path.exists(file)
