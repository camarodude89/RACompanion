from pony.orm import *

db = Database()


class User(db.Entity):

    name = Required(str)
    city = Required(str)
    machines = Set('Machine')


class Machine(db.Entity):

    name = Required(str)
    description = Optional(str)
    users = Set(User)