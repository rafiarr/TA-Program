import csv
import sys
import os
import time
from alert import *
from oshandler import *
from classificationhandler import *
from graphdrawer import *

def main():
    
    os = OSHandler()
    
    alerts = os.getAlertinDataset('dataset/lldos1/')
    
    alertList = []

    for i in range(len(alerts)):
        if( (alerts[i].sig_name in alertList) == False):
            alertList.append(alerts[i].sig_name)
    
    trainReader = os.dataTrainReader('dataset/DataTrain/')

    svmHandler = SVMHandler(trainReader)

    acm = AlertCausalityMatrix(alertList)

    # count = 0
    # path = os.outputFileDirPath + "correlated-value.txt"
    # outputFile = open(path,"wb")
    
    output = "Hasil correlation"
    count = 0

    start_time = time.time()

    for i in range(len(alerts)):
        for j in range(len(alerts)):
            correlation = AlertCorrelation(alerts[i],alerts[j])
            alert1 = correlation.alert1.sig_name
            alert2 = correlation.alert2.sig_name
             
            correlationValues = correlation.getValues()
            
            # print correlationValues
            # print "prediction : " + str(svmHandler.predict(correlationValues))
            if(svmHandler.predict(correlationValues) == '1'):
                acm.incrementACMValue(alert1,alert2)
                # output = alert1 + "," +alert2+" : "+str(correlationValues)+"\n"
                # outputFile.write(output)
                count = count +1
            # else:
                
                # print alert1
                # print alert2

            # count = count+1
            # if(count == 5):
            #     break

        # if(count == 5):
        #     break,.
    # outputFile.close()
    print count
    print "selesai alert correlation"
    print "--- "+str(time.time() - start_time) +" seconds ---"

    acm.calculateAllSigmaValue()
    for row in acm.causalityMatrix:
        print row

    relatedList = acm.getRelatedList() 
    edgeList = []
    labelList = []
    for row in relatedList:
        edgeList.append(row.keys()[0])
        labelList.append(row.values()[0])
    
    graphDrawer = GraphDrawer(edgeList,labelList)
    print graphDrawer.graph 
    print graphDrawer.labels

    graphDrawer.draw_graph()
    
if __name__ == '__main__':
    main()



