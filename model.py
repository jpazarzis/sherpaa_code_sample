import uuid
from collections import Counter

class Datastore(object):
    items = []

    def add(self, item):
        self.items.append(item)
        return item.itemid

    def stats(self):
        types = Counter([i.item_type for i in self.items])
        types["item"] = sum(types.values())
        return types

    def __iter__(self):
        return self.items.__iter__()


class User(object):
    item_type = "regular user"
    allowed_issuetypes = ["sick", "hurt", "mental", "insurance"]

    def __init__(self, first_name, last_name, employer, email, birthdate, state, dependent_of):
        self.first_name = first_name
        self.last_name = last_name
        self.employer = employer
        self.email = email
        self.birthdate = birthdate
        self.state = state
        self.itemid = uuid.uuid4().hex
        self.insuranse = self.state not in ['NY', 'NJ', 'CT', 'CA']
        self.dependent_of = dependent_of
        

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return "<{}: {} -- employee at {}; allowed issuetypes: {}>".format(
                self.item_type, self.name, self.employer, self.allowed_issuetypes)
