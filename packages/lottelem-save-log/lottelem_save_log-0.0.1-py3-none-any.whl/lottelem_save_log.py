#################################################
#작성자 : 박상혁(기기개발팀)
#ProgramVersion : 1.0
#FileName : Save_Log.py
#History
# - Create : 2021-03-04 파일 수신 프로그램
# - Update #1 : 2021-03-04 파일 수신 프로그램
# - Update #2 : 2021-03-05 DB INSERT 기능 추가
# - Update #3 : 2021-03-08 시간 substring 변경
#################################################

import os
import pymssql
import datetime

from flask import Flask, render_template, request
from flask import send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/upload')
#def load_file():
#   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])

#File 저장 함수
def upload_file():

   if request.method == 'POST': #POST 방식
      
      f = request.files['file']
      filename = f.filename
      
      path = 'c:/smart_log'
      #path = 'f:/smart_log'
      firstClassCode = filename[0:4]
      machineId = filename[4:6]
      date = filename[6:14]
      time = filename[14:20]
      base_dir = path + '/' + firstClassCode + '/' + machineId + '/' + date
      now = str(datetime.datetime.now())[0:23]

      try:

         if not os.path.isdir(base_dir): #Directory Check
            os.makedirs(base_dir) #
            os.chdir(base_dir)
         else:
            print(base_dir + '해당 폴더가 이미 존재합니다.')   

         f.save(secure_filename(f.filename))
         dbInsert(base_dir, filename, firstClassCode, machineId, date, time, now)         

         return 'file uploaded successfully' + '  ' + 'Path : ' + base_dir #MSG 및 저장 경로
      
      except: 
         return 'Error'
         #return 'Except Error'

# dbInsert 함수
def dbInsert(base_dir, filename, firstClassCode, machineId, date, time, now):

   try:
      with open(base_dir + '/' + filename, mode="r") as file:
         lines = file.read()
         print(lines)       

      # 개발 Connection 정보
      conn = pymssql.connect(host="10.4.1.143", user='lcms_dev', password='lccms!!lem0601', database='LCMS', charset='EUC-KR')  
      
      # 운영 Connection 정보
      #conn = pymssql.connect(host="10.4.1.143", user='lcms_dev', password='lccms!!lem0601', database='LCMS', charset='EUC-KR')
      
      cursor = conn.cursor()
      sql = "INSERT INTO [dbo].[MachineStatusLogDetail] ([FirstClassCode], [MachineID], [FileName], [SaveDt], [Savetime], [LogDetail], [OccurDT]) VALUES ( %s, %d, %s, %s, %s, %s, %s )"
      val = (firstClassCode, machineId, filename, date, time, lines, now)
      cursor.execute(sql, val)
      conn.commit()
      conn.close()
      print(sql, val)

   except: 
      return 'Error[DB]'

if __name__ == '__main__':
   #app.run(host='10.4.1.140', port = '49351')
   app.run(host='localhost', port = '5000')