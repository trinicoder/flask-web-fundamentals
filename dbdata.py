from sqlalchemy import create_engine
import os

if os.path.exists("hotspot.db"):
    os.remove("hotspot.db")
e = create_engine("sqlite:///hotspot.db")
e.execute("""
    create table users (
        id integer primary key,
        username varchar
    )
""")



e.execute("""insert into users(username) values ('Varoon')""")
e.execute("""insert into users(username) values ('Jerry')""")
e.execute("""insert into users(username) values ('Divya')""")
