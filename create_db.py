from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User

engine = create_engine('sqlite:///database1.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# User
user1 = User(name = "Hello World", email = "hello.world@gmail.com")
session.add(user1)
session.commit()

user2 = User(name = "James Harden", email = "james.harden@gmail.com")
session.add(user2)
session.commit()

print "added catalog items!"
