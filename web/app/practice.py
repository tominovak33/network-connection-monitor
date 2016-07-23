import os
import sys

# # Add vendor directory to module search path
# current_dir = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(current_dir)
#
# vendor_dir = os.path.join(current_dir, 'lib')
# sys.path.append(vendor_dir)

import sqlalchemy
from sqlalchemy import *

db = create_engine('mysql://root:root@localhost/practicedb')
conn = db.connect()

metadata = MetaData(db)
# metadata.bind = db

cars = Table('Cars', metadata,
     Column('Id', Integer, primary_key=True),
     Column('Name', String(64)),
     Column('Price', Integer)
)

metadata.create_all()
