from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def compress_image(image, quality=60):
    """
    Reusable image compressor for all models
    """
    img = Image.open(image)

     # convert png/webp etc to rgb
    if img.mode != 'RGB':
        img = img.convert('RGB')   
        '''ensures image works in JPEG format'''

     # ✅ resize large images
    max_size = (1000, 1000)

    img.thumbnail(max_size)
    '''thumbnail keep image retio correct'''

    output = BytesIO() 
    '''temporary storage in RAM (not disk)'''

    # optimize=True reduces size more
    img.save(
        output,
        format='JPEG',
        quality=quality,
        optimize=True
    )  
    '''quality is for compresss img like make 500kb '''

    print("Compressed Size:", output.tell() / 1024, "KB")
    
    output.seek(0)                                     
    '''go back to start of file'''

    return ContentFile(output.read(), name=image.name)