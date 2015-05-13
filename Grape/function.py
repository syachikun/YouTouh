#-*-coding:utf-8-*-
import MySQLdb
from config import *

class Group:

    def __init__(self, name):
        ##名字与数据库中相同
        self.name=name
        data=self.get_data()
        self.group_id = data['group_id']
        self.topic=data['topic']
        self.confirmMessage=data['confirmMessage']
        self.leadername=data['leadername']

    def get_members(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select membername from groupMemberAssosiation where groupname="+"'"+self.name+"';")
        members=cursor.fetchall()
        conn.close()
        return members

    def get_data(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from groups where name="+"'"+self.name+"';")
        data=cursor.fetchall()
        conn.close()
        return data[0]  

class User:

    def __init__(self, name = '', email = ''):
        self.username = name
        self.email = email

    def create_group(self,groupname,topic,confirmMessage):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在
        cursor.execute("select name from groups where name='"+groupname+"';")
        exist=cursor.fetchall()
        if(exist):
            print 'failed to create group :',groupname
            return False
        cursor.execute("insert into groupMemberAssosiation(groupname,membername) values(%s,%s);",(groupname,self.username))
        conn.commit()
        cursor.execute("insert into groups(name,topic,confirmMessage,leadername) values(%s,%s,%s,%s);",\
            (groupname,topic,confirmMessage,self.username))
        conn.commit()
        conn.close()
        print 'created group successfully:',groupname
        return True

    def delete_group(self,groupname):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在且用户为leader
        cursor.execute("select name from groups where name='"+groupname+"' and leadername='"+self.username+"';")
        exist=cursor.fetchall()
        if(exist):
            cursor.execute("delete from groups where name='"+groupname+"';")
            conn.commit()
            cursor.execute("delete from groupMemberAssosiation where groupname='"+groupname+"';")
            conn.commit()
            conn.close()
            print 'deleted group successfully :',groupname
            return True
        conn.close()
        print 'failed to delete group :',groupname
        return False

    def get_groups(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select groupname from groupMemberAssosiation where membername='"+self.username+"';")
        attendedGroups=cursor.fetchall()
        cursor.execute("select name from groups where leadername='"+self.username+"';")
        ownGroups=cursor.fetchall()
        conn.close()
        return attendedGroups,ownGroups

    def join_group(self,groupname):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select name from groups where name='"+groupname+"';")
        exist=cursor.fetchall()
        if(exist):
            cursor.execute("insert into groupMemberAssosiation(groupname,membername) values(%s,%s);",(groupname,self.username))
            conn.commit()
            conn.close()
            print 'joined group successfully :',groupname
            return True
        conn.close()
        print 'failed to join group :',groupname
        return False

    def quit_group(self,groupname):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from groupMemberAssosiation where membername='"+self.username+"' and groupname='"+groupname+"';")
        exist=cursor.fetchall()    
        if(exist):
            cursor.execute("delete from groupMemberAssosiation where membername='"+self.username+"' and groupname='"+groupname+"';")   
            conn.commit()
            #whether he's leader
            cursor.execute("select name from groups where name='"+groupname+"' and leadername='"+self.username+"';")            
            isLeader=cursor.fetchall()  
            if(isLeader):
                print "the user trying to quit is LEADER!"
                cursor.execute("delete from groups where name='"+groupname+"';")
                conn.commit()

            conn.close()
            print 'quit group successfully :',groupname
            return True
        print 'failed to quit group :',groupname
        conn.close()
        return False

        

    def search_group(self,groupname):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在
        cursor.execute("select name from groups where name='"+groupname+"';")
        exist=cursor.fetchall()
        if(exist):
            Group1=Group(groupname)
            return Group1
        return None

    def check_u(self):
        conn = MySQLdb.connect(host=self.db_host,port=self.db_port,user=self.db_user,passwd=self.db_passwd,db=self.db_name,charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('select * from user')
        for row in cursor.fetchall():
            if row[1] == self.username:
                return 0
        return 1

    def check_e(self):
        conn = MySQLdb.connect(host=self.db_host,port=self.db_port,user=self.db_user,passwd=self.db_passwd,db=self.db_name,charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('select * from user')
        for row in cursor.fetchall():
            if row[3] == self.email:
                return 0
        return 1


class Question:

    def __init__(self, user_id, group_id, content = ''):
        self.user_id = user_id
        self.group_id = group_id
        self.content = content

    def get_questions(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select membername from groupMemberAssosiation where groupname="+"'"+self.groupname+"';")
        members=cursor.fetchall()
        conn.close()
        return members
