from pathlib import Path


class DataSet: 
    def __init__(self):
        self.iridl_type = 'DataSet'
        self.iridl_ds_name = 'None'
        self.banned = ['dir', 'invalid', 'parent', 'name', 'banned', 'banned_long', 'iridl_ds_name',  'iridl_type']

    def __eq__(self, otr):
        ret = True
        if type(otr) == DataSet:
            for child in vars(self).keys():
                if child != 'parent':
                    try:
                        temp = (getattr(self, child) == getattr(otr, child))
                        if getattr(self, child) is None and getattr(self, child) is None: 
                            temp = True
                        if type(getattr(self, child)) == list and len(getattr(self, child)) == 0 and type(getattr(otr, child)) == list and len(getattr(otr, child)) == 0:
                            temp = True
                        elif type(getattr(self, child)) == list: 
                            for item in range(len(getattr(self, child))):
                                if getattr(otr, child)[item] != getattr(self, child)[item]:
                                    temp = False
                        ret = ret and temp
                    except:
                        ret = False 
        else:
            print('comparing dataset to nondataset')
            ret = False 
        return ret

    def __repr__(self):
        return 'dataset'

    def __str__(self):
        return 'dataset'

    def url(self):
        return self.parent.url() + '.' + self.iridl_ds_name  + '/' if self.parent is not None else '.'+ self.iridl_ds_name + '/'

    def json(self):
        ret = {'iridl_type': 'DataSet'}
        for child in vars(self).keys():
            if type(getattr(self, child)) in [DataSet]: #datasets do not have source children
                if child == 'parent':
                    pass 
                else:
                    ret[child] = getattr(self, child).json()
            else:
                if child == 'dir':
                    ret[child] = str(getattr(self, child))
                else:
                    ret[child] = getattr(self, child)
        return ret   

    @classmethod
    def from_json(self, json, parent=None):
        new = DataSet()
        new.parent = parent
        for obj in json.keys():
            if  type(json[obj]) == dict and json[obj]['iridl_type'] == 'DataSet':
                setattr(new, obj, DataSet.from_json(json[obj], parent=new))
            #elif type(json[obj]) == dict and json[obj]['iridl_type'] == 'Source':              #datasets do not have source children 
             #   setattr(new, obj, Source.from_json(json[obj], parent=new))
            elif obj == 'dir':
                setattr(new, obj, Path(json[obj]))
            else:
                setattr(new, obj, json[obj])
        return new

    def tree(self, depth=0, deep=False):
        print('  |'*depth + '-.{:<30}{:>50}'.format(self.iridl_ds_name, str(self)))
        for child in sorted(vars(self).keys()):
            if child not in self.banned and deep:
                try:
                    vars(self)[child].tree(depth=depth+1, deep=deep)
                except:
                    print('  |'*(depth+1) + '-.{:<30.30}{:>30.30}'.format(child, str(vars(self)[child])))

    def avail(self):
        for child in vars(self).keys():
            if child not in self.banned:
                print('  .{:<30.30}{:>30.30}'.format(child, str(getattr(self, child))))
