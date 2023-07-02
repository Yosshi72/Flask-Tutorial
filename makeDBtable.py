from models.database import db_session, init_db
from models.models import TopoContent

# initialize DB table 
init_db()

c1 = TopoContent("full-mesh", "a fully connected network")
c2 = TopoContent("line", "each node is directly connected to two other nodes, except for first and last nodes")
c3 = TopoContent("ring", "each node is directly connected to two other nodes")
c4 = TopoContent("star", "the central node acts as a central point of control and communication, while the other nodes are connected directly to it")

db_session.add(c1)
db_session.add(c2)
db_session.add(c3)
db_session.add(c4)
db_session.commit()