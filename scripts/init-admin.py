#!/usr/bin/env python3
import mongoengine as me
import sys
from funlab import models




def init_admin():


   if models.User.objects(username="admin").first():
       print("already have admin user in database")
       return
  
   admin_user = models.User(
       username="admin",
       email="admin@example.com",
       first_name="admin",
       last_name="admin",
       roles=["admin"],
   )
   admin_user.set_password("!q2w3e4r5t")
   admin_user.save()
   print("create admin user username: admin password: !q2w3e4r5t")




if __name__ == "__main__":
   DB_NAME = "funlabdb"
   if len(sys.argv) > 1:
       me.connect(db=DB_NAME, host=sys.argv[1])
   else:
       me.connect(db=DB_NAME)
   print(f"connect to {DB_NAME}")


   init_admin()
   print("======= create user success ========")