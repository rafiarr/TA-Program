from __future__ import division

def ipToBinary(ipAddr):
    
    ip = ipAddr.split(".")
    print ip
    fullBinary = ''
    for number in ip:
        binary = "{0:08b}".format(int(number))
        print binary
        fullBinary += binary
    print fullBinary    
    return fullBinary

def compareUrutan(string1,string2):
    
    count = 0
    for x in range(len(string1)):
        # printString = "index : " + str(x) + " string 1 : " + string1[x] + " string 2 : " + string2[x] 
        # print printString   
        if(string1[x] == string2[x]):
            count = count + 1

    return count

def compareIP(ipAddr1,ipAddr2):
    ipBin1 = ipToBinary(ipAddr1)
    # print ipToBinary(ipAddr1)
    ipBin2 = ipToBinary(ipAddr2)
    # print ipToBinary(ipAddr2)
    # print compareUrutan(ipBin1,ipBin2)
    return compareUrutan(ipBin1,ipBin2)

print compareIP("192.168.56.101","192.168.56.102")

# print fValue1("192.168.56.101","192.168.56.102")/32

# fValue = float(fValue1("192.168.56.101","192.168.56.102")/32)

# printString = "nilai F1 : " + str(fValue) 


n = 1596
array = [[0 for x in range(n)] for y in range(n)]
for i in range(1596):
    for j in range(1596):
        array[i][j] = 1 + i + j

print array[1][1]
print array[1595][1595]



def comparePort(portNumber1,portNumber2):
    if(portNumber1 == portNumber2):
        return True
    else:
        return False

if(comparePort(1,1)):
    print "sama"
else:
    print "beda"