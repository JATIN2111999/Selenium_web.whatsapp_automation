import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import io,sys,time,datetime
# you can edit 
SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive',
         "https://www.googleapis.com/auth/documents",
         "https://www.googleapis.com/auth/documents.readonly"]
# add id of the doc file
NORMAL_MSG_ID="YOUR_API_KEY"
WEEK_MSG_ID="YOUR_API_KEY"

# change followers 
GREATERTHANFOLLOWERS=3

THE_JSON="client_secret.json"
# you can edit 

class DriveHelp:
    def __init__(self):
        self.creds=ServiceAccountCredentials.from_json_keyfile_name(THE_JSON,SCOPE)
        self.pdate=datetime.datetime.now().date()

        
    def getSheetData(self,name):
        # authrize and get data from sheet
        client=gspread.authorize(self.creds)
        sheet=client.open(name).sheet1
        data=sheet.get_all_records()
        return data

    def fileData(self,filename):
        # read the data from txtfile
        try:
            data=open(filename,'r',encoding = 'utf-8')
            data=data.read().split("\n")
            data=[d.strip() for d in data]
            return data
        except Exception as e:
            print("something happen in reading name from txt or txt is empty")
            print(e)
            pass
    
    def getwholedata(self):
        # get all the sheet data 
        returnList=[]
        theuser=self.fileData("./data/drivename.txt")
        # print(theuser)    
        for usr in theuser:
            print(f"getting data from {usr} ...",end="")
            returnList+=self.getSheetData(usr)
            print("done")
        return returnList

    def getDate(self):
        # date fomrating here
        x=self.pdate
        day=int(x.strftime("%d"))
        month=int(x.strftime("%m"))
        year=int(x.strftime("%Y"))
        formatdate="{}/{}/{}".format(day,month,year)
        return formatdate

    def checkingfollow(self,number):
        # return True when the follower is greater then 3 and date is current date
        number=int(number)

        if number > GREATERTHANFOLLOWERS:  
            return True
        else:
            return False
    


class docsMessage(DriveHelp):
    def __init__(self):
        super().__init__()
        # getting data form docs file using NORMAL_MSG_ID and WEEK_MSG_ID
        print("getting docs messages... ",end="")
        self.service=build('docs','v1',credentials=self.creds)
        self.document=self.service.documents().get(documentId=NORMAL_MSG_ID).execute()
        self.doc_content=self.document.get("body").get("content")
        print(f"done")

        


    """nice function implemented"""
    def read_paragraph_element(self,element):
        """Returns the text in the given ParagraphElement.

            Args:
                element: a ParagraphElement from a Google Doc.
        """
        text_run = element.get('textRun')
        if not text_run:
            return ''
        return text_run.get('content')


    def read_strucutural_elements(self,elements):
        """Recurses through a list of Structural Elements to read a document's text where text may be
            in nested elements.

            Args:
                elements: a list of Structural Elements.
        """
        text = ''
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for elem in elements:
                    text += self.read_paragraph_element(elem)
            elif 'table' in value:
                # The text in table cells are in nested Structural Elements and tables may be
                # nested.
                table = value.get('table')
                for row in table.get('tableRows'):
                    cells = row.get('tableCells')
                    for cell in cells:
                        text += read_strucutural_elements(cell.get('content'))
            elif 'tableOfContents' in value:
                # The text in the TOC is also in a Structural Element.
                toc = value.get('tableOfContents')
                text += read_strucutural_elements(toc.get('content'))
        return text


    def replaceText(self,content,name,theDate,followerNumber):
        # replace name date and number in text
        content=content.replace("( name )",name)
        content=content.replace("( date )",theDate)
        content=content.replace("( numbers )",followerNumber)
        return content


    def getnormalmessage(self):
        # gets normal message 
        drivecontent=self.read_strucutural_elements(self.doc_content)
        return drivecontent

    def getnormalmessagewithreplace(self,name,theDate,followerNumber):
        # gets normal message 
        drivecontent=self.read_strucutural_elements(self.doc_content)
        msg =self.replaceText(drivecontent,name,theDate,str(followerNumber))
        return msg

    def getWeekMessage(self):
        # week message 
        print("getting docs messages... ",end="")
        Weekdocument=self.service.documents().get(documentId=WEEK_MSG_ID).execute()
        Weekdoc_content=Weekdocument.get("body").get("content")
        # print(Weekdoc_content) #can't get emoji
        print(f"got {Weekdocument.get('title')}")
        drivecontent=self.read_strucutural_elements(Weekdoc_content)
        print(drivecontent)
        return drivecontent

    def check_exists_by_xpath(self,webdriver,xpath):
        try:
            webdriver.find_element_by_xpath(xpath)
        except Exception as e:
            return True
        return False






    