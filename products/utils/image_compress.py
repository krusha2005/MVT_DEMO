from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def compress_image(image, quality=60):
    """
    Reusable image compressor for all models
    """
    img = Image.open(image)

    if img.mode != 'RGB':
        img = img.convert('RGB')   
        '''ensures image works in JPEG format'''

    output = BytesIO()       
    '''temporary storage in RAM (not disk)'''

    img.save(output, format='JPEG', quality=quality)   
    '''quality is for compresss img like make 500kb '''
    output.seek(0)                                     
    '''go back to start of file'''

    return ContentFile(output.read(), name=image.name)