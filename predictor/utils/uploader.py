
import os, uuid, re

# 修改项目名称 * hcShoppingMallBackend *
import stock.settings as settings

BASE_DIR = settings.BASE_DIR


class COMMON_FILE_DIR:
    RET_DIR = 'static//file'
    ABS_DIR = os.path.join(BASE_DIR, 'static', 'file')

def getFiles(dir):
    return os.listdir(dir)

def generateUUID(filename): # 创建唯一的文件名
    id = str(uuid.uuid4())
    extend = os.path.splitext(filename)[1]
    return id + extend


def chunkFileWriter(file, path):
    destination = open(path, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()


def commonFileWriter(file, path):
    with open(path, 'wb+') as file_obj:
        file_obj.write(file)


def merge(dir):
    dir = os.path.join(COMMON_FILE_DIR.ABS_DIR, dir) # f"{getBaseDirname()}\\static\\{dir}"
    files = getFiles(dir)
    type = files[0].split('.')[1]
    with open(os.path.join(dir, files[0]), 'ab+') as head:
        i = 1
        while 1:
            try:
                other = os.path.join(dir, f"{i}.{type}")
                with open(other, 'rb+') as body:
                    head.write(body.read())
                os.remove(other)
            except FileNotFoundError as e:
                print(e)
                break
            i += 1
    if len(getFiles(dir)) == 1:
        return True
    return False


class FileInfo:
    file_name = ''
    file_type = ''


class FileUploader():

    def __init__(self, file: any, _file: dict):
        self.file = file
        self.file_name_body = _file['name']
        self.file_type = _file['type']

    def upload(self):
        raise Exception(
            'Class {} upload method should be override!'
            .format(self.__class__.__name__)
        )

    def getFilePath(self, host):
        pass

    def __str__(self):
        return self.file_name_body


class ImageFileUploader():

    BASE_DIR = BASE_DIR
    RET_DIR = 'static/'
    ABS_DIR = os.path.join(BASE_DIR, 'static')
    IMG_TYPE = ('png', 'gif', 'jpeg', 'bmp',
                'jpg', 'tif', 'svg', 'webp')

    def __init__(self, file):
        self.check_type(file)
        self.file = file
        self.file_name = self.get_unique_name(file.name)

    def check_type(self, file):
        _, file_type = (file.name).split('.')
        assert file_type in self.IMG_TYPE, '图片类型不符合'

    def get_unique_name(self, filename):
        id = str(uuid.uuid4())
        extend = os.path.splitext(filename)[1]
        return id + extend

    def upload(self):
        img_path = os.path.join(self.ABS_DIR, self.file_name)
        self.perform_write(self.file, img_path)

    def perform_write(self, file, path):
        destination = open(path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

    def get_file_path(self, host):
        # static//xxx.png 不能是双斜杠
        # static/xxx.png Yes!
        return f"http://{host}/{self.RET_DIR}{self.file_name}"

    @staticmethod
    def get_files(self):
        return os.listdir(self.ABS_DIR)

    @staticmethod
    def delete(cls, url):
        def get_name(url: str):
            matches = re.findall(r'[a-zA-Z0-9-]+', url)
            file_name, file_type = matches[-2], matches[-1]
            return '{0}.{1}'.format(file_name, file_type)
        file_name = get_name(url)
        path = os.path.join(cls.ABS_DIR, file_name)
        try:
            os.remove(path)
        except Exception:
            assert False, '文件不存在'







class CommonFileUploader(FileUploader):

    def __init__(self, file: any, _file: dict):
        self.index = _file.get('index', -1)
        super().__init__(file, _file)

    def upload(self):
        file_dir = os.path.join(COMMON_FILE_DIR.ABS_DIR, self.file_name_body)
        try:
            os.makedirs(file_dir)
        except FileExistsError as e:
            print(e)
        file_path = os.path.join(file_dir, f"{str(self.index)}.{self.file_type}")
        chunkFileWriter(self.file, file_path)


    def getFilePath(self, host):
        return f"http://{host}/{COMMON_FILE_DIR.RET_DIR}/{self.file_name_body}/{self.index}.{self.file_type}"







