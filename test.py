from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import matplotlib.pyplot as plt

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\benre\\OneDrive\\Desktop\\ComicTranslator\\total-cedar-335014-5412f0edd455.json"

#Testing Text placement within boundaries
def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=40)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text), 
                  line, font=font, fill=text_color)
        y_text += line_height

blockCon = []
symbolCon = []
wordsCon = []

#Used for graphs
def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))
            blockCon.append(block.confidence)

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))
                    wordsCon.append(word.confidence)
                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))
                        symbolCon.append(symbol.confidence)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    # [END vision_python_migration_document_text_detection]
# [END vision_fulltext_detection]

# add your own path
def Average(lst):
    return sum(lst) / len(lst)

path = "unknown (1).png"
detect_document(path)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylabel('Confidence level')
ax.set_title('OCR Confidence level of a manga')
plt.locator_params(axis="y", nbins=20)

xaxis = ['blocks','words','characters']
yaxis = [Average(blockCon),Average(wordsCon),Average(symbolCon)]
ax.bar(xaxis,yaxis)
for container in ax.containers:
    ax.bar_label(container)
plt.show()
print(blockCon)
print(wordsCon)
print(symbolCon)
