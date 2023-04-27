#PT_COCO30K_img 테이블

import  sqlite3
# con = sqlite3.connect("tutorial.db")
class Coco:
    #생성자  : db 연결코드 /
    def __init__(self):
        self.con = sqlite3.connect("/content/drive/MyDrive/3조/DB/coco30k_F_v3.db", timeout=100,isolation_level=None)
        self.cur = self.con.cursor()
        
            #db close 코드
    def __del__(self):
       self.cur.close();
       self.con.close();

    ##1 insert    :  insert into MyTest values ( ?,?,?) ;
    def   PT_COCO30K_img_insert(self, id_key, img_address , caption_1, caption_2, caption_3, caption_4, caption_5, caption_list ):
        sql ='insert into PT_COCO30K_img values ( ?,?,?,?,?,?,?,?)'
        self.con.execute(sql,(id_key, img_address , caption_1, caption_2, caption_3, caption_4, caption_5, caption_list))
        self.con.commit()

    ##2. update  :  update  MyTest set name =?  where no =?
    def PT_COCO30K_img_update(self, id_key, img_address , caption_1, caption_2, caption_3, caption_4, caption_5, caption_list ):
        sql ='update  PT_COCO30K_img set img_address =?,caption_1 =?,caption_2 =?,caption_3 =?,caption_4 =?,caption_5 =?,caption_list =?  where id_key =?'
        self.con.execute(sql,(img_address, caption_1, caption_2, caption_3, caption_4, caption_5, caption_list, id_key))
        self.con.commit()

    ##3 delete  : delete from MyTest  where  no =?
    def  PT_COCO30K_img_delete(self,id_key):
        sql =  'delete from PT_COCO30K_img  where  id_key =? '
        self.con.execute(sql, ( id_key))
        self.con.commit()
        
    def PT_COCO30K_img_selectall(self) :
        sql = 'select * from PT_COCO30K_img'
        res = self.cur.execute(sql)
        for row in res:
            print(row)
#         res.fetchall()
#         print(res)


    def PT_COCO30K_img_selectone(self, id_key) :
        sql = 'select * from PT_COCO30K_img Where id_key = ?'
        self.cur.execute(sql,(id_key,))
        row = self.cur.fetchone()
        print(row)
        print('id_key :',row[0])
        print('img_address :',row[1])
        print('caption_1 : ',row[2])
        print('caption_2 :',row[3])
        print('caption_3 :',row[4])
        print('caption_4 :',row[5])
        print('caption_5 : ',row[6])
        print('caption_list :',row[7])
        self.con.commit()




#customer_image  테이블


class Custo:
    #생성자  : db 연결코드 /
    def __init__(self):
        self.con = sqlite3.connect("C:\\Users\\황인\\Desktop\\DB\\coco30k_F_v3.db", timeout=100,isolation_level=None)
        self.cur = self.con.cursor()
        
            #db close 코드
    def __del__(self):
       self.cur.close();
       self.con.close();

    ##1 insert    :  insert into MyTest values ( ?,?,?) ;
    def   PT_COCO30K_img_insert(self, id_key, file , time_stamp ):
        sql ='insert into customer_image values ( ?,?,?)'
        self.con.execute(sql,(id_key, file , time_stamp))
        self.con.commit()

    ##2. update  :  update  MyTest set name =?  where no =?
    def PT_COCO30K_img_update(self, id_key, file, time_stamp ):
        sql ='update  customer_image set file =?,time_stamp =?  where id_key =?'
        self.con.execute(sql,(file, time_stamp, id_key))
        self.con.commit()

    ##3 delete  : delete from MyTest  where  no =?
    def  mPT_COCO30K_img_delete(self,id_key):
        sql =  'delete from customer_image  where  id_key =? '
        self.con.execute(sql, ( id_key))
        self.con.commit()
        
    def PT_COCO30K_img_selectall(self) :
        sql = 'select * from customer_image'
        res = self.cur.execute(sql)
        for row in res:
            print(row)
#         res.fetchall()
#         print(res)


    def PT_COCO30K_img_selectone(self, id_key) :
        sql = 'select * from customer_image Where id_key = ?'
        self.cur.execute(sql,(id_key,))
        row = self.cur.fetchone()
        print(row)
        print('id_key :',row[0])
        print('file :',row[1])
        print('time_stamp : ',row[2])
        self.con.commit()
