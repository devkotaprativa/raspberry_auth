import boto3
import os
import io
import sys
import pymysql
from subprocess import call
from paramiko import SSHClient
import paramiko
from scp import SCPClient
import requests
import polling
import time
file = open('distance.txt', 'r')
distance = float(file.read())
file.close()

db = pymysql.connect(host ='localhost', user = 'root', passwd = 'admin',db ='raspberrypi')
cur = db.cursor()
cur.execute("SELECT userimage FROM users")
images = cur.fetchall()
client = boto3.client('rekognition')

with open("image.jpg", 'rb') as imageFile:
    target_bytes = imageFile.read()

bucket='prativadb'
s3 = boto3.client('s3')
similar =0
final_image = ''
def call_api():
    global final_image
    global similar
    for userimage in images:
        with open(userimage[0],'rb') as imageFile:
            source_bytes = imageFile.read()
            response = client.compare_faces(SimilarityThreshold=50, SourceImage={'Bytes': source_bytes},TargetImage={'Bytes': target_bytes})
            for faceMatch in response['FaceMatches']:
                Similarity = faceMatch['Similarity']

                if Similarity >= similar:
                    similar = Similarity
                    final_image = userimage
    return final_image
img = call_api()

print('The face matches with '+str(final_image) ,similar)

if similar!=0:
    sql = "SELECT " + "distance" + " FROM users WHERE userimage =%s"
    cur = db.cursor()
    cur.execute(sql, (final_image,))
    dis = cur.fetchall()
    if dis >= distance+10 or dis <= distance+10:
    cmd = 'scp -i /home/pi/cnproject.pem /home/pi/CN_project/image.jpg ubuntu@ec2-52-70-92-152.compute-1.amazonaws.com:/home/ubuntu '
    call(cmd.split())

    img = final_image

    ssh = SSHClient()
    scp = SCPClient(ssh.get_transport())
    ssh.load_system_host_keys('/home/pi/cnproject.pem')
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.RSAKey.from_private_key_file ('/home/pi/cnproject.pem')
    ssh.connect('52.70.92.152', port=22, username='ubuntu', pkey=private_key)
    x = 1
    while(x):
        try:
            scp.get('/home/ubuntu/authstatus.txt','/home/pi/CN_project')
            if(os.path.exists('/home/pi/CN_project/authstatus.txt')):
                break
        except:
            print("checking for file")
            time.sleep(5)
            x=1
    auth = open('authstatus.txt', 'r')
    data = str(auth.read())
    print data
else:
    print("You do not match with any registered users")

