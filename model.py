import uuid
from collections import Counter

class Datastore(object):
    items = []
    item_map = {}
    need_to_assign_parent = []

    def clear(self):
        self.items = []
        
    def size(self):
        return len(self.items)

    def count_dependents(self):
        return len([x for x in self.items if hasattr(x , 'dependent_of')])

    def add(self, item):
        if hasattr(item, 'dependent_of_as_name'):
            self.need_to_assign_parent.append(item)
        else:
            self.items.append(item)
            self.item_map[item.name] = item.itemid
        self._assign_parents()
        return item.itemid

    def _assign_parents(self):
        for item in self.need_to_assign_parent:
            if item.dependent_of_as_name in self.item_map:
                item.dependent_of = self.item_map[item.dependent_of_as_name]
                del item.dependent_of_as_name
                self.items.append(item)

        self.need_to_assign_parent = [item for item in self.need_to_assign_parent 
                                        if hasattr(item, 'dependent_of_as_name' )]

    def stats(self):
        types = Counter([i.item_type for i in self.items])
        types["item"] = sum(types.values())
        return types

    def length(self):   
        return len(self.items)

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

        dependent_of = dependent_of.strip()

        if len(dependent_of) > 0:
            self.dependent_of_as_name = dependent_of

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        
        if not hasattr(self, 'dependent_of'):
            return "<{}: {} -- employee at {}; allowed issuetypes: {}>".format(
                    self.item_type, self.name, self.employer, self.allowed_issuetypes)
        else:
            return "<{}: {} -- dependent of {}>".format(
                    self.item_type, self.name, self.dependent_of)
        

