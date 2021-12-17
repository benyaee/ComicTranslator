import os
from google.cloud import vision
from tkinter import filedialog as fd
from tkinter import *
import inpaint
import translate
import inpaint
import replaceText

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\benre\\OneDrive\\Desktop\\ComicTranslator\\total-cedar-335014-5412f0edd455.json"

#Main Text Detection Method
def detect_text(path,lang,type):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    #If these return text detections worked
    response = client.text_detection(image=image)
    texts = response.text_annotations
    pages = response.full_text_annotation.pages

    #Blocked based inpainting, keeps the bounding box vertices
    if (type=="Bounding block Based Inpainting"):
        for page in pages:
            for block in page.blocks:
                vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in block.bounding_box.vertices])
                    
                vert = inpaint.boundRect(vertices)
                if os.path.isfile("temp.png"):
                    temp = inpaint.inpaint("temp.png",vert)
                else:
                    temp = inpaint.inpaint(path,vert)

    #Inpainting only if user chooses
    elif (type=="Remove text only"):
        for text in texts[1:]:
            print('\n"{}"'.format(text.description))
            translate.translate_text("eng",text.description)
            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])
            vert = inpaint.boundRect(vertices)
            if os.path.isfile("temp.png"):
                temp = inpaint.inpaint("temp.png",vert)
            else:
                temp = inpaint.inpaint(path,vert)
        os.rename("temp.png","final.png")
        return None

    #Word based Inpainting
    else:
        for text in texts[1:]:
            print(text.confidence)
            print('\n"{}"'.format(text.description))
            translate.translate_text("eng",text.description)
            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])
            vert = inpaint.boundRect(vertices)
            if os.path.isfile("temp.png"):
                temp = inpaint.inpaint("temp.png",vert)
            else:
                temp = inpaint.inpaint(path,vert)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    fn = fileName("completed.png")
    os.rename("temp.png",fn)
    replaceText.replaceText(path,fn,lang)

#Used for multiple files
def fileName(file):
    count=0
    while os.path.isfile(file):
        file = "completed{0}.png".format(count)
        count=count+1
    return file

#Processes through every file uploaded
def multiTrans(fn,lang,type):
    for x in fn:
        detect_text(x,lang,type)


