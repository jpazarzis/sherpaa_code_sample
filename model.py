import uuid
from collections import Counter


DATA_STATS_DESCRITION = '''There are {0} items in the datastore.  There are {1} regular users in the
 datastore.  There are {2} insurance-only users in the datastore.  There are {3}
 HR admins in the datastore.'''


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

    def get_data_stats(self):

        count_regular_users = len([x for x in self.items if x.item_type == "regular user"])
        count_insurance_only = len([x for x in self.items if x.item_type == "insurance only"])
        count_hr_admins = len([x for x in self.items if x.hr_admin])

        return DATA_STATS_DESCRITION.format(
                    len(self.items), 
                    count_regular_users,
                    count_insurance_only,
                    count_hr_admins
                )



    def length(self):   
        return len(self.items)

    def __iter__(self):
        return self.items.__iter__()


class User(object):
    item_type = "regular user"
    allowed_issuetypes = ["sick", "hurt", "mental", "insurance"]

    def __init__(self, first_name, last_name, employer, email, birthdate, state, dependent_of, hr_admin):
        self.first_name = first_name
        self.last_name = last_name
        self.employer = employer
        self.email = email
        self.birthdate = birthdate
        self.state = state
        self.itemid = uuid.uuid4().hex

        if self.state not in ['NY', 'NJ', 'CT', 'CA']:
            self.item_type = "insurance only"

        dependent_of = dependent_of.strip()

        if len(dependent_of) > 0:
            self.dependent_of_as_name = dependent_of

        self.hr_admin = hr_admin.strip() == 'x'

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
        

