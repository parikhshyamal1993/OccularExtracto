import os
import fitz
import cv2
import numpy as np
import json
import tqdm

def yeildImage(inFile,Zoomfactor):

    if os.path.exists(inFile):
        pass
    else:
        raise IOError("Failed to load file please check file path")

    file = fitz.open(inFile)
    pdfDict = dict()
    for PageID, pages in enumerate(file):
        textList = ''
        rectList = []
        mat = fitz.Matrix(Zoomfactor,Zoomfactor)
        pix = pages.get_pixmap(matrix=mat)
        text = pages.getText('words')
        imageData = pix.getImageData("png")
        nparr = np.frombuffer(imageData, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        yield PageID,img


def extractText(inFile , Zoomfactor):
    """"
    PDF Extract text with hOCR and Image 
    
    """
    if os.path.exists(inFile):
        pass
    else:
        raise IOError("Failed to load file please check file path")

    
    file = fitz.open(inFile)
    pdfDict = dict()
    for PageID , pages in enumerate(tqdm.tqdm(file)):
        textList = ''
        rectList = []
        #qmat = fitz.Matrix(Zoomfactor,Zoomfactor)
        #pix = pages.get_pixmap(matrix=mat)
        text = pages.getText('words')
        #imageData = pix.getImageData("png")
        #nparr = np.frombuffer(imageData, np.uint8)
        #img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        block=0
        lines = 0
        
        for words in text:
            #cv2.rectangle(img,(int(words[0]*Zoomfactor),int(words[1]*Zoomfactor)),(int(words[2]*Zoomfactor),int(words[3]*Zoomfactor)),(255,0,0),2,)
            
            if block<words[5]:
                block = words[5]
                lines=words[6]
                textList+="\n"
            if lines<words[6]:
                lines=words[6]
                textList+="\n"
            textList+= words[4]+" "
            rectList.append([int(words[0]*Zoomfactor),int(words[1]*Zoomfactor),int(words[2]*Zoomfactor),int(words[3]*Zoomfactor)])
            
            #print("words",words)
        pdfDict[PageID]=[textList,rectList]
        # cv2.imshow("show image",img)
        # if cv2.waitKey(0):
        #     cv2.destroyAllWindows()
        #print("text",text)
        #print("texts : ",textList)
    return pdfDict


def generateTextfile(inFile,outfilebase=None,Zoomfactor=1):
    if os.path.exists(inFile):
        pass
    else:
        raise IOError("Failed to load file please check file path")
    if outfilebase==None:
        filePath = os.path.basename(inFile).split('.')[0]+".txt"
        print("filename:",filePath)
    else:
        fileName = os.path.basename(inFile).split('/')[-1].split('.')[0]+".txt"
        filePath = os.path.join(outfilebase,fileName)
        print("filename:",filePath)

    OutDict = extractText(inFile,Zoomfactor)

    with open(filePath,'w') as textFile:
        json.dump(OutDict,textFile,indent=6)
    return True

def generateText(inFile,Zoomfactor=1):
    if os.path.exists(inFile):
        pass
    else:
        raise IOError("Failed to load file please check file path")

    
    file = fitz.open(inFile)
    pdfDict = dict()
    for PageID , pages in enumerate(file):
        textList = ''
        rectList = []
        text = pages.getText('words')
        block=0
        lines = 0
        
        for words in text:
            if block<words[5]:
                block = words[5]
                lines=words[6]
                textList+="\n"
            if lines<words[6]:
                lines=words[6]
                textList+="\n"
            textList+= words[4]+" "
            rectList.append([int(words[0]*Zoomfactor),int(words[1]*Zoomfactor),int(words[2]*Zoomfactor),int(words[3]*Zoomfactor)])
        yield textList , rectList

def plotPdf(inFile,Zoomfactor=1):
    """"
    PDF Extract text with hOCR and Image 
    
    """
    if os.path.exists(inFile):
        pass
    else:
        raise IOError("Failed to load file please check file path")

    
    file = fitz.open(inFile)
    pdfDict = dict()
    for PageID , pages in enumerate(tqdm.tqdm(file)):
        textList = ''
        rectList = []
        mat = fitz.Matrix(Zoomfactor,Zoomfactor)
        pix = pages.get_pixmap(matrix=mat)
        text = pages.getText('words')
        imageData = pix.getImageData("png")
        nparr = np.frombuffer(imageData, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        block=0
        lines = 0
        
        for words in text:
            cv2.rectangle(img,(int(words[0]*Zoomfactor),int(words[1]*Zoomfactor)),(int(words[2]*Zoomfactor),int(words[3]*Zoomfactor)),(255,0,0),2,)
            
            if block<words[5]:
                block = words[5]
                lines=words[6]
                textList+="\n"
            if lines<words[6]:
                lines=words[6]
                textList+="\n"
            textList+= words[4]+" "
            rectList.append([int(words[0]*Zoomfactor),int(words[1]*Zoomfactor),int(words[2]*Zoomfactor),int(words[3]*Zoomfactor)])
            
            
        yield textList,rectList, img

if __name__ =="__main__":
    file = "/home/shyamal/Documents/FullStack/ImageProcessing/AutoContentSearch/assets/TestData/3c976c41-f8ca-43fd-8860-51d09e4fb365.pdf"
    
    ########################
    # extractText(file,1)

    # #########################

    # for PageID , img in yeildImage(file,2):
    #     print('page :',PageID,img.shape)


    # for text, rect , img in plotPdf(file,2):
    #     print('page :',text,img.shape)
    #     cv2.imshow("show image",img)
    #     if cv2.waitKey(0):
    #         cv2.destroyAllWindows()
    
    
    ################################
    for text , rect  in generateText(file,2):
        print(text)
        break
    ################################