import base64
from PIL.Image import Image
from io import BytesIO
from typing import Union, IO

ImageType = Union[str, bytes, IO, Image, None]

class ImageTool:
    @staticmethod
    def is_accepted_format(binary_data: bytes) -> str:
        if binary_data.startswith(b'\xFF\xD8\xFF'):
            return "image/jpeg"
        elif binary_data.startswith(b'\x89PNG\r\n\x1a\n'):
            return "image/png"
        elif binary_data.startswith(b'GIF87a') or binary_data.startswith(b'GIF89a'):
            return "image/gif"
        elif binary_data.startswith(b'\x89JFIF') or binary_data.startswith(b'JFIF\x00'):
            return "image/jpeg"
        elif binary_data.startswith(b'\xFF\xD8'):
            return "image/jpeg"
        elif binary_data.startswith(b'RIFF') and binary_data[8:12] == b'WEBP':
            return "image/webp"
        else:
            raise ValueError("Invalid image format (from magic code).")
    
    @staticmethod
    def to_bytes(image: ImageType) -> bytes:
        try:
            if isinstance(image, str) and not image.startswith('data:'):
                with open(image, 'rb') as f:
                    return f.read()
                
            elif hasattr(image, 'read'):
                chunks = []
                while True:
                    chunk = image.read(8192)
                    if not chunk:
                        break
                    chunks.append(chunk)
                if hasattr(image, 'seek'):
                    try:
                        image.seek(0)
                    except (OSError, IOError):
                        pass
                return b''.join(chunks)
            
            elif isinstance(image, bytes):
                return image
            
            elif isinstance(image, Image):
                bytes_io = BytesIO()
                image.save(bytes_io, format=image.format or 'JPEG')
                return bytes_io.getvalue()
            
            elif isinstance(image, str) and image.startswith('data:'):
                return ImageTool.extract_data_uri(image)
            
            else:
                raise ValueError("Unsupported image type")
            
        except Exception as e:
            raise ValueError(f"Failed to convert image to bytes: {str(e)}")

    @staticmethod
    def image_to_base64(image: ImageType) -> str:
        try:
            if isinstance(image, str) and image.startswith('data:'):
                return image
            
            data = ImageTool.to_bytes(image)
        
            mime_type = ImageTool.is_accepted_format(data)
        
            base64_data = base64.b64encode(data).decode('utf-8')
        
            return f"data:{mime_type};base64,{base64_data}"
        
        except Exception as e:
            raise ValueError(f"Failed to convert image to base64: {str(e)}")

    @staticmethod
    def extract_data_uri(data_uri: str) -> bytes:
        data = data_uri.split(",")[-1]
        return base64.b64decode(data)