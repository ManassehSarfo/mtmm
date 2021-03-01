from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from zosftplib import Zftp
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Check
import csv
import os


# Create your views here.
def index(request):
    letscheck = Check.objects.get(pk=1)
    
    if request.method == 'POST':
        uservalue = int(request.POST['numrec'])
        letscheck.dcheck = True

        Myzftp = Zftp('192.86.32.153', "Z01117", "salad234")

        Myzftp.submit_wait_job("//Z01117  JOB 1 \n"
                                "//COBRUN  EXEC IGYWCL,PARM='NOSEQ'\n"
                                "//COBOL.SYSIN  DD DSN=&SYSUID..GRANDF(GFCCG),DISP=SHR\n"
                                "//LKED.SYSLMOD DD DSN=&SYSUID..LOAD(GFCCG),DISP=SHR\n"
                                "// IF RC = 0 THEN\n"
                                f"//RUN     EXEC PGM=GFCCG,PARM='{uservalue}'\n"
                                "//STEPLIB   DD DSN=&SYSUID..LOAD,DISP=SHR\n"
                                #"//STEP1   EXEC PGM=IEFBR14\n"
                                "//PRTLINE   DD DSN=Z01117.OUTPUT(GFOUT),DISP=SHR\n"
                                "//SYSOUT    DD SYSOUT=*,OUTLIM=15000\n"
                                "//CEEDUMP   DD DUMMY\n"
                                "//SYSUDUMP  DD DUMMY\n"
                                "// ELSE\n"
                                "// ENDIF\n",
                                purge=True)
        # easy job for zos:
        '''
        Myzftp.submit_wait_job(f"//Z01117  JOB 1 \n"
                                "//COBRUN  EXEC IGYWCL,PARM='NOSEQ'\n"
                                "//COBOL.SYSIN  DD DSN=&SYSUID..GRANDF(GFCCG),DISP=SHR\n"
                                "//LKED.SYSLMOD DD DSN=&SYSUID..LOAD(GFCCG),DISP=SHR\n"
                                "// IF RC = 0 THEN\n"
                                '//RUN     EXEC PGM=GFCCG,PARM="{uservalue}"\n'
                                "//STEPLIB   DD DSN=&SYSUID..LOAD,DISP=SHR\n"
                                #"//STEP1   EXEC PGM=IEFBR14\n"
                                "//PRTLINE   DD DSN=Z01117.OUTPUT(GFOUT),DISP=SHR\n"
                                "//SYSOUT    DD SYSOUT=*,OUTLIM=15000\n"
                                "//CEEDUMP   DD DUMMY\n"
                                "//SYSUDUMP  DD DUMMY\n"
                                "// ELSE\n"
                                "// ENDIF\n",
                                purge=True)
                                '''

        messages.success(request, f'Submitted')

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.HttpResponseRedirect(reverse('index', args=({"check":letscheck.dcheck})))
        #return redirect(reverse('index')+'#tryout', check=letscheck.dcheck, message=messages)
        return render(request, 'index.html', {"check":letscheck.dcheck})
    else:
     
        return render(request, 'index.html', {"check":letscheck.dcheck})
    

def download(request):

    letscheck = Check.objects.get(pk=1)
    letscheck.dcheck = False
    
    Myzftp = Zftp('192.86.32.153', "Z01117", "salad234", timeout=500.0)
    #Myzftp.get_members('Z01117.OUTPUT.CUSTOMER','/')
    #Myzftp.download_binary('Z01117.OUTPUT.CUSTOMER', '/')
    Myzftp.download_text('Z01117.OUTPUT(GFOUT)', './results.txt')

    #mf_file = open('./results.txt', 'r+', encoding="utf-8")
    #ffa = mf_file.read(16)
    #print("Read record is :", ffa)
    #mf_file.close()
    Myzftp.close()

    data = open('./results.txt','r').read()
    resp = HttpResponse(data, content_type="text/txt")
    resp['Content-Disposition'] = 'attachment;filename=results.txt'
    return resp
    
    #from django.views.static import serve
    #filepath = './results.txt'
    #return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    
    return redirect('index')

def dload(request):

    data = open('./results.txt','r').read()
    resp = HttpResponse(data, content_type="text/txt")
    resp['Content-Disposition'] = 'attachment;filename=results.txt'
    return resp


def submitjob(request):
    
    Myzftp = Zftp('192.86.32.153', "Z01117", "salad234", timeout=500.0, sbdataconn='(ibm-1147,iso8859-1)')
    # easy job for zos:
    Myzftp.submit_wait_job(f"//Z01117  JOB 1 \n"
                                "//COBRUN  EXEC IGYWCL,PARM='NOSEQ'\n"
                                "//COBOL.SYSIN  DD DSN=&SYSUID..GRANDF(GFCCG),DISP=SHR\n"
                                "//LKED.SYSLMOD DD DSN=&SYSUID..LOAD(GFCCG),DISP=SHR\n"
                                "// IF RC = 0 THEN\n"
                                "//RUN     EXEC PGM=GFCCG,PARM='2000'\n"
                                "//STEP1   EXEC PGM=IEFBR14\n"
                                "//STEPLIB   DD DSN=&SYSUID..LOAD,DISP=SHR\n"
                                "//PRTLINE   DD DSN=Z01117.GRANDF(OUTPUT),DISP=NEW\n"
                                "//SYSOUT    DD SYSOUT=*,OUTLIM=15000\n"
                                "//CEEDUMP   DD DUMMY\n"
                                "//SYSUDUMP  DD DUMMY\n"
                                "// ELSE\n"
                                "// ENDIF\n",
                                purge=True)

    #print("rc:", job["rc"], "Jes status:", job["status"])
    #for line in job["output"]:
        #print(line)
    return redirect('index')


def testing(request):
    userval = 300
    a = f'''
    //Z01117  JOB 1 
    //COBRUN  EXEC IGYWCL,PARM='NOSEQ'
    //COBOL.SYSIN  DD DSN=&SYSUID..GRANDF(GFCCG),DISP=SHR
    //LKED.SYSLMOD DD DSN=&SYSUID..LOAD(GFCCG),DISP=SHR
    // IF RC = 0 THEN
    //RUN     EXEC PGM=GFCCG,PARM='{userval}'
    //STEP1   EXEC PGM=IEFBR14
    //STEPLIB   DD DSN=&SYSUID..LOAD,DISP=SHR
    //PRTLINE   DD DSN=Z01117.GRANDF(OUTPUT),DISP=NEW
    //SYSOUT    DD SYSOUT=*,OUTLIM=15000
    //CEEDUMP   DD DUMMY
    //SYSUDUMP  DD DUMMY
    // ELSE
    // ENDIF
    '''

    print(a)    
    return redirect('index')



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


    Myzftp = Zftp('192.86.32.153', "Z01117", "salad234", timeout=500.0, sbdataconn='(ibm-1147,iso8859-1)')
    # easy job for zos:
    job = Myzftp.submit_wait_job("//GFJCL  JOB TESTING,NOTIFY=&SYSUID\n"
                                "//COBRUN  EXEC IGYWCL,PARM='NOSEQ'\n"
                                "//COBOL.SYSIN  DD DSN=&SYSUID..GRANDF(GFCCG),DISP=SHR\n"
                                "//LKED.SYSLMOD DD DSN=&SYSUID..LOAD(GFCCG),DISP=SHR\n"
                                "// IF RC = 0 THEN\n"
                                "//RUN     EXEC PGM=GFCCG,PARM='1500'\n"
                                "//STEPLIB   DD DSN=&SYSUID..LOAD,DISP=SHR\n"
                                "//PRTLINE   DD DSN=Z01117.GRANDF(OUTPUT),DISP=SHR\n"
                                "//SYSOUT    DD SYSOUT=*,OUTLIM=15000\n"
                                "//CEEDUMP   DD DUMMY\n"
                                "//SYSUDUMP  DD DUMMY\n"
                                "// ELSE\n"
                                "// ENDIF\n",
                                purge=True)

    print("rc:", job["rc"], "Jes status:", job["status"])
    for line in job["output"]:
        print(line)

           
'''