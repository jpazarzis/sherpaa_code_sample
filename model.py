import uuid
from collections import Counter

class Datastore(object):
    items = []
    need_to_assign_parent = {}

    def add(self, item):
        self.items.append(item)

        name_key = '{0} {1}'.format(item.last_name, item.first_name)
        if item.needs_to_assign_parent:
            if item.dependent_of not in self.need_to_assign_parent:
                self.need_to_assign_parent[item.dependent_of] = [item]
            else:
                self.need_to_assign_parent[item.dependent_of].append(item)

        elif name_key in self.need_to_assign_parent:

            for i in self.need_to_assign_parent[name_key]:
                i.self.dependent_of = item.itemid
                i.needs_to_assign_parent = False
            
            del self.need_to_assign_parent[name_key]


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
        self.needs_to_assign_parent = len(self.dependent_of) > 0
        

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        if self.dependent_of == '':
            return "<{}: {} -- employee at {}; allowed issuetypes: {}>".format(
                    self.item_type, self.name, self.employer, self.allowed_issuetypes)
        else:
            return "<{}: {} -- dependent of {}>".format(
                    self.item_type, self.name, self.dependent_of)
        

