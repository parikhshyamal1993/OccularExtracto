from src.TextExtract import *

# #########################
def yeildImagetest(file):
    for PageID , img in yeildImage(file,2):
            print('page :',PageID,img.shape)


##############################
def plotPdftest(file):
    for text, rect , img in plotPdf(file,2):
        print('page :',text,img.shape)
        cv2.imshow("show image",img)
        if cv2.waitKey(0):
            cv2.destroyAllWindows()


################################
def generateText(file):
    for text , rect  in generateText(file,2):
        print(text)

################################

if __name__=="__main__":
    file = "/home/shyamal/Documents/FullStack/ImageProcessing/AnnualReportData/TestData/3c976c41-f8ca-43fd-8860-51d09e4fb365.pdf"
    
    ########################
    textDict = extractText(file,1)
    print("text",textDict[0][0])