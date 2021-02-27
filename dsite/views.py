from django.shortcuts import render
from zosftplib import Zftp
import csv



# Create your views here.
def index(request):
     
     return render(request, 'index.html')
    

def download(request):

    Myzftp = Zftp('192.86.32.153', "Z01117", "salad234", timeout=500.0, sbdataconn='(ibm-1147,iso8859-1)')
    #Myzftp.get_members('Z01117.OUTPUT.CUSTOMER','/')
    #Myzftp.download_binary('Z01117.OUTPUT.CUSTOMER', '/')
    Myzftp.download_text('Z01117.GRANDF.CCNUM', './results.txt')

    mf_file = open('./results.txt', 'r+')
    ffa = mf_file.read(16)
    print("Read record is :", ffa)
    mf_file.close()
    Myzftp.close()

    print(Myzftp)

    return render(request, 'index.html')


'''
with open('test.csv', mode='w') as test:
    writer = csv.writer(test, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    with open("results.txt", "r") as a_file:
        for line in a_file:
            stripped_line = line.strip()
            print(stripped_line)

            writer.writerow(stripped_line)
            #writer.writerow(['Erica Meyers', 'IT', 'March'])
            a_file.close()

           
'''