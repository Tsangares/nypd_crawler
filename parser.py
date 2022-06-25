from bs4 import BeautifulSoup
import pandas as pd
import pprint
pp = pprint.PrettyPrinter(indent=2)

def parseHtml(text):
    #There are odd newline \xa0 character; this deletes it
    clean = lambda string: string.replace(u'\xa0','')

    #Setup parser
    soup = BeautifulSoup(text,'html.parser')

    #Setup output
    content = []

    #Find all rows
    for row in soup.find_all(attrs={'role': 'row'}):
        rowContent = []
        #Find all cells
        for cell in row.find_all('div','pivotTableCellNoWrap'):
            #Clean and collect text
            rowContent.append(clean(cell.text))
        #Attach to main list
        content.append(rowContent)
    #Pretty print data collected.
    pp.pprint(content)

    return content

#Convert collected data to dataframe
def getDataFrame(content):
    return pd.DataFrame(content,columns=('Command','Last','First','Rank','Shield','Index'))


if __name__=="__main__":
    with open('content.html') as f:
        parseHtml(f.read())
