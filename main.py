#import pandas as pd
from bs4 import BeautifulSoup
import json

def Add(a,b):
    return a+b

def Hello():
    print("Hello Luck, 2.0")

'''
def parseExcel():
    excel_data_df = pd.read_excel('Alerts.xlsx', sheet_name='UCSAlerts', skiprows=range(0, 4), engine='openpyxl')
    json_str = excel_data_df.to_json(orient='records')
    parsed = json.loads(json_str)
    with open('Alerts.json', 'w') as f:
        f.write(json.dumps(parsed,indent=2))

    fault_df = pd.read_json('Alerts.json')
    fault_df = fault_df[fault_df.Severity != 'cleared']
    al_str=fault_df.to_json(orient='index')
    al =  json.loads(al_str)

    with open('AlertsNoCleared.json', 'w') as f:
        f.write(json.dumps(al,indent=2))
'''

def getData():
    html_data = ""
    columnNames = []
    #file_name="C://Users//lramamur//PycharmProjects//NAA_Processor//ExceptionTables153875//PA_NXOS_CPU_RESOURCE.html"
    file_name='PA_NXOS_OSPF_SPF_TIMERS.html'
    with open(file_name, "r") as f:
        html_data = f.read()

    html_data = html_data.replace("<B>", "")
    html_data = html_data.replace("</B>", "")

    soup = BeautifulSoup(html_data, features="html.parser")
    x = soup.find("thead")
    rows = x.findChildren('tr')
    print("Heading Rows : ", len(rows))
    if (len(rows) > 1):
        rows = rows[1:]
    k = 0
    for row in reversed(rows):
        k = k + 1
        currentPointer = 0
        cols = row.findChildren('td')

        for col in cols:
            if (int(col["colspan"]) == 1 and int(col["rowspan"]) == k):
                columnNames.insert(currentPointer, col.getText().replace("\xa0", ""))
                currentPointer = currentPointer + 1
            else:
                for i in range(0, int(col["colspan"])):
                    # print(i)
                    temp = columnNames[currentPointer + i]
                    temp = col.getText() + " - " + temp
                    columnNames[currentPointer + i] = temp
                currentPointer = currentPointer + int(col["colspan"])
    print(columnNames)
    table_data = []
    stat_table = soup.find('table')
    data=[]
    for row in stat_table.find_all('tr'):
        col={}
        col_no=0
        for cell in row.find_all('td', class_=True):
            cell_data={}
            cell_value=[]
            y = cell.text.replace("\xa0", " ")
            sev = cell["class"][0]
            if 'ADDFFF' in sev:
                color="Critical"
            elif 'FF0000' in sev:
                color="High"
            elif 'F9966B' in sev:
                color="Medium"
            elif 'FFFF00' in sev:
                color="Low"
            elif '00FF00' in sev:
                color="Informational"
            else:
                color="White"
            cell_data["Value"]=y
            cell_data["Sverity"]=color
            #print(cell_data)
            cell_value.append(cell_data)
            col[columnNames[col_no]] = cell_value
            col_no=col_no+1
            #print(col)


        #print(col)
        data.append(col)

    print(data)
getData()
if __name__ == '__main__':
    getData()
