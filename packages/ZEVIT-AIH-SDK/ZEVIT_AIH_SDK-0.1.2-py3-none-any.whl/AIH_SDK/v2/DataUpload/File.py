from AIH_SDK.v2.v2Object import v2Object
from AIH_SDK.AIHExceptions import AIHException
from PIL import Image
import io

class File(v2Object):
    
    def __init__(self):
        super().__init__()
        
        self._api = 'du'
        self._endpoint = 'Files'
        self._image_extensions = ['jpg', 'jpeg', 'png']

    
    def get(self, file_id:str=None, datatype_id:str=None):
        """
        get gets the file with the specific id or a list of files with the datatype_id.
        Exactly one of the ids should be stated. 
            If both None: Error will be raised.
            If both stated: Only file_id will be used.

        IN: file_id (str)     - The id of the file to get.
            datatype_id (str) - The id of the datatype to get a list of files from.

        OUT: self
        """

        if file_id:
            self.value = self._client.get(self._api, f'{self._endpoint}/definition/{file_id}')
        elif datatype_id:
            self.value = self._client.get(self._api, f'{self._endpoint}/{datatype_id}')
        else:
            raise AIHException('file_id or datatype_id must be stated.')
        
        return self
    
        
            
    def download(self):
        f"""
        download create a generator that downloads the file or files if a list.

        OUT (generator) - A generator where each object is bytes for files. 
                          If file extension is in {self._image_extensions} the object will be a PIL Image.
        """

        if type(self.value) == dict:
            content = self._client.download_file(self.value["id"])

            # If file is an image, set content to PIL.Image
            if self.value['name'].split('.')[-1] in self._image_extensions:
                content = Image.open(io.BytesIO(content))

            yield content

        elif type(self.value) == list:
            for val in self.value:
                content = self._client.download_file(val["id"])
                
                # If file is an image, set content to PIL.Image
                if val['name'].split('.')[-1].lower() in self._image_extensions:
                    content = Image.open(io.BytesIO(content))

                yield content
    

    def upload(self, file, datatype_id:str, name:str, exif:bytes=None):
        """
        To post the updates that have been made.
        IN: file     - The that should be uploaded
            name     - The name of the file that should be uploaded. Should contain the file extention
            exif     - Exif dictionary that is converted to bytes. Is used to set the metadata.
        """
        
        fileextension = name.split('.')[-1]
        _file = io.BytesIO()
        
        if fileextension.lower() in self._image_extensions:
            if exif:
                file.save(_file, format='jpeg' if fileextension.lower() == 'jpg' else fileextension, exif=exif)
            else:
                file.save(_file, format='jpeg' if fileextension.lower() == 'jpg' else fileextension)

            _file.seek(0)
        else:
            _file = file
        
        response_json = self._client.upload_file(datatype_id, _file, name)
        self.value = response_json
        
        return self