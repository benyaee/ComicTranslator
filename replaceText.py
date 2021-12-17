from google.cloud import vision
import os,io
import textwrap

from PIL import Image, ImageDraw, ImageFont
import inpaint
import translate

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="Put your .json Google Cloud API Path Key Here"
client = vision.ImageAnnotatorClient()
path = "msedge_fiCagpYbjE.png"
def fileName(file):
    count=0
    while os.path.isfile(file):
        file = "final{0}.png".format(count)
        count=count+1
    return file


def drawText(vert,text,clearedout):
    if os.path.isfile("replaceTemp.png"):
        path = "replaceTemp.png"
    else:
        path = clearedout
    vert = inpaint.boundRect(vert)
    x0=int(vert[0][0])
    x2=int(vert[2][0])
    y0=int(vert[0][1])
    y2=int(vert[2][1])
    print(vert)


    str = " "
    str = str.join(text)
    text = textwrap.fill(text=str, width=20)
    img = Image.open(path)
    draw = ImageDraw.Draw(img)
    box = (x0,y0,x2,y2)
    #Used to check the boundary box on the image
    # draw.rectangle(box)

    #Rescaling text font to fit within boundary box, starts large then decreases
    font_size = 100
    size = None
    while (size is None or size[0] > box[2] - box[0] or size[1] > box[3] - box[1]) and font_size > 0:
        font = ImageFont.truetype("cc-wild-words-roman.ttf", font_size)
        size = font.getsize_multiline(text)
        font_size -= 1
    draw.multiline_text((box[0], box[1]), text, "#000", font)
    img.save("replaceTemp.png")

#Main Method to grab text from original image then pass through to translate and calls drawText
def replaceText(path,clearedout,lang):
    with io.open(path,'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    pages = response.full_text_annotation.pages
    for page in pages:
        for block in page.blocks:
            vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in block.bounding_box.vertices])
            txt=[]
            print('block confidence:', block.confidence)
            for paragraph in block.paragraphs:
                            for word in paragraph.words:
                                word_text = ''.join([symbol.text for symbol in word.symbols])
                                txt.append(translate.translate_text(lang,word_text))
            print(vertices)
            drawText(vertices,txt,clearedout)
    fn = fileName("final.png")
    os.rename("replaceTemp.png",fn)


    
