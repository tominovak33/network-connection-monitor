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

cars = Table('Cars', metadata, autoload=True)

# stm = select([cars])
# stm = select([cars.c.Price])

stm = select([cars]).where(and_(cars.c.Price > 5000,
                                cars.c.Price < 1000000))

rs = conn.execute(stm)

print rs.fetchall()
