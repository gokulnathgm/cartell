import commands
import os

import cv2

SCALAR_BLUE = (255.0, 0.0, 0.0)
index = ('mahindra', 'honda', 'toyota', 'suzuki', 'tata', 'ford', 'hyundai', 'volkswagen')

cwd = os.getcwd()
files = os.listdir(cwd + '/iteration-1/false')
rel_path = '/iteration-1/false/'
path = cwd + rel_path

def writeResultOnImage(openCVImage, resultText):
    # ToDo: this function may take some further fine-tuning to show the text well given any possible image size

    imageHeight, imageWidth, sceneNumChannels = openCVImage.shape

    # choose a font
    fontFace = cv2.FONT_HERSHEY_TRIPLEX

    # chose the font size and thickness as a fraction of the image size
    fontScale = 1.0
    fontThickness = 2

    # make sure font thickness is an integer, if not, the OpenCV functions that use this may crash
    fontThickness = int(fontThickness)

    upperLeftTextOriginX = int(imageWidth * 0.05)
    upperLeftTextOriginY = int(imageHeight * 0.05)

    textSize, baseline = cv2.getTextSize(resultText, fontFace, fontScale, fontThickness)
    textSizeWidth, textSizeHeight = textSize

    # calculate the lower left origin of the text area based on the text area center, width, and height
    lowerLeftTextOriginX = upperLeftTextOriginX
    lowerLeftTextOriginY = upperLeftTextOriginY + textSizeHeight

    # write the text on the image
    cv2.putText(openCVImage, resultText, (lowerLeftTextOriginX, lowerLeftTextOriginY), fontFace, fontScale, SCALAR_BLUE,
                fontThickness)


for image in files:
    command = "python label_image.py \
    --graph=output/output_graph.pb \
    --labels=output/output_labels.txt \
    --input_layer=Placeholder \
    --output_layer=final_result \
    --image={path}{image}".format(path=path, image=image)

    status, result = commands.getstatusoutput(command)
    result_list = result.split('\n')
    result = ''
    for results in result_list:
        if results.startswith(index):
            result += results
            result += '\n'
    print result
    text = result.split('\n')[0]
    im = cv2.imread(path + image)
    writeResultOnImage(im, text)
    cv2.imshow('image', im)
    cv2.waitKey()
