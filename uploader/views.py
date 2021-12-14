
from rest_framework.views import APIView

from . import models

from .utils.response import validData, Success, Error
from .utils.uploader import ImageFileUploader

UPLOAD_SUC = Success(1002, 'Upload Success')
UPLOAD_Err = Error(2002, 'Upload Error')

class Upload(APIView):

    def getUploader(self, file, file_type, file_name_body):
        img_type = ('png', 'gif', 'jpeg', 'bmp', 'jpg', 'tif', 'svg', 'webp')

        if file_type in img_type:
            return ImageFileUploader(file)

        raise Exception('Image Type Not Supported')

    @validData(UPLOAD_SUC, UPLOAD_Err, valid=False)
    def post(self, request, *args, **kwargs):

        file = request.FILES.get('file')

        assert file is not None, 'Image File Can"t Be Empty'

        file.name = file.name.replace('\"', '') or file.name
        file_name_body, file_type = (file.name).split('.') or (file.name, None)

        assert file_type is not None, 'Image File Error'

        host = request.get_host()
        Uploader = self.getUploader(file, file_type, file_name_body) # type: ImageFileUploader

        assert Uploader is not None, 'Image Type Not Supported'

        Uploader.upload()
        file_path = Uploader.get_file_path(host)
        models.Image.objects.create(name=file.name)
        return { 'path': file_path }

