import csv
import os
import filetype
import boto3
import re
import time
def loop(rootdir):
    bucket='grey_campus'
    myFile = open('mapping.csv', 'w')
    myFields = ['courses','paths','upload_path']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader()
    myFile.close()
    path(rootdir)
    count=0
    with open('courses.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(row[0])
                line_count += 1
            else:
               if count<20:
                   destination_path=row[1]
                   unzip=row[1]
                   file=row[2]
                   count=count+1
                   upload(unzip,file,bucket,destination_path.replace(rootdir,''))
                   print('uploaded')
               else:
                   count=0

def upload(file,tag,bucket_name,destinaton_path):
            place_mp4='path'
            palce_file='path'
            s3 = boto3.client('s3')
            myFile = open('mapping.csv', 'a')
            myFields = ['courses','paths','upload_path']
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            path=str(destinaton_path)
            destinaton_path=destinaton_path.replace(tag,'')
            ex=os.path.splitext(tag)[1]
            tag=re.sub('[^A-Za-z0-9.]+', '_',os.path.splitext(tag)[0])
            tag=tag+str(int(time.time()))+ex     
            
            destinaton_path=re.sub('[^A-Za-z0-9]+', '_',destinaton_path)
            destinaton_path=destinaton_path+tag
            guess=filetype.guess(file)
            if guess is not None:
             if 'video' in str(guess.mime) :
              #  s3.upload_file(file,str(bucket_name),place_mp4+'/'+destinaton_path)
                os.system("aws s3 cp --content-type 'video/mp4' --acl public-read '"+file+"' s3://url/"+place_mp4+"/"+destinaton_path+" --metadata-directive REPLACE")
                writer.writerow({'courses': path.split('/')[0],'paths':path,'upload_path':'https://url'+place_mp4+'/'+destinaton_path})
                print(destinaton_path)
             else:
               # s3.upload_file(file,str(bucket_name),palce_file+'/'+destinaton_path)
                os.system("aws s3 cp --content-type 'binary/octet-stream' --acl public-read '"+file+"' url"+palce_file+'/'+destinaton_path+" --metadata-directive REPLACE")
                writer.writerow({'courses': path.split('/')[0],'paths':path,'upload_path':'https://url'+palce_file+'/'+destinaton_path})
            else:
                  # s3.upload_file(file,str(bucket_name),palce_file+'/'+destinaton_path)
                os.system("aws s3 cp --content-type 'binary/octet-stream' --acl public-read '"+file+"' s3://url/"+palce_file+'/'+destinaton_path+" --metadata-directive REPLACE")
                writer.writerow({'courses': path.split('/')[0],'paths':path,'upload_path':'https://url/'+palce_file+'/'+destinaton_path})
            myFile.close()



def path(rootdir):
     
     myFile = open('courses.csv', 'w')
     myFields = ['courses','paths','file']
     writer = csv.DictWriter(myFile, fieldnames=myFields)
     writer.writeheader()
     for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                unzip=os.path.join(subdir,file)
                destination_path=unzip
                writer.writerow({'courses':destination_path.split('/')[0], 'paths':destination_path,'file':file})
     myFile.close()
def download():
    rootdir=os.path.dirname(os.path.realpath(__file__))
                    
    if not os.path.exists(rootdir+'/newdir'):
       os.makedirs(rootdir+'/newdir')
    with open('pending files srinu.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(row[0])
                line_count += 1
            else:
                if 'Not available' not in  row[2]:
                    file=row[1].replace('(',' ').replace(')',' ').replace(' ','_')
                    os.system('curl   -L -J -O '+row[2])
                    unzip(rootdir)		       

def unzip(rootdir):
    for file in os.listdir(rootdir):
                
                unzip=os.path.join(rootdir, file)
                print(unzip)
                if '.zip' in unzip: 
                    os.system('unzip -o "'+unzip+'" -d videos"'+unzip.replace('.zip','').replace(rootdir,'')+'"')
                    os.system('rm "'+unzip+'"')

download()
rootdir=os.path.dirname(os.path.realpath(__file__))
path(rootdir+'/videos/')
loop(rootdir+'/videos/')
               

