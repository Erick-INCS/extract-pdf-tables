import tabula
import pandas as pd
import re
from sys import argv

fileName = ''
for i, arg in enumerate(argv):
    if '.pdf' in arg:
        fileName = arg
        break

if fileName:
    data = tabula.read_pdf(fileName,multiple_tables=True, pages=6)

    data = list(filter(lambda e: e.shape[0] > 1 and e.shape[1] > 3, data))
    names = [e.columns[0] for e in data]
    data = list(map(lambda e: e.rename(columns={vl:'C' + str(i) for i,vl in enumerate(e.columns)}), data))

    rg = re.compile('^[^\d]+')
    endData = []
    endNames= []

    for i, nm in enumerate(names):
        if rg.match(nm):
            endData.append(data[i])
            endNames.append(nm)
        else:
            endData[-1] = pd.concat([endData[-1], data[i]])

    for i, dt in enumerate(endData):
        vals = dt.values
        nms = vals[0]
        df = {}
        
        for ii, nm in enumerate(nms):
            df[nm] = vals[1:, ii]
        
            endData[i] = pd.DataFrame(df)

    print(len(data), 'tables')

    for i, nm in enumerate(endNames):
        endData[i].to_csv(f"data/{nm}.csv", index=False)
else:
    print('Es necesario especificar un archivo PDF.')