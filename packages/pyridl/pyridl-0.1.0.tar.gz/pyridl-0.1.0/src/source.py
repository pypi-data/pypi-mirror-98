from pathlib import Path
import json, requests, re
from bs4 import BeautifulSoup
from .iridl_utils import sanitize_identifier, sanitize_ingrid_literal
from .dataset import DataSet

class Source:
    def __init__(self, dirname='.', parent=None, verbose=False):
        self.parent = parent
        self.invalid = []
        self.dir = Path(dirname) if self.parent is None else self.parent.dir / dirname
        self.banned = ['dir', 'invalid', 'parent', 'name', 'banned', 'banned_long', 'iridl_ds_name',  'iridl_type']
        self.iridl_type = 'Source'
        self.iridl_ds_name = self.dir.name
        self.restriction = 'Public'
        if dirname == '.':
            return 
        found_das = False
        all_members = self.dir.glob('*')                                #find all subdirs and files 
        files = [x for x in all_members if x.is_file() and 'html' not in x.name and \
            '.owl' not in x.name and '.cuf' not in x.name and '.cdf' not in x.name and \
                '.py' not in x.name  and '__pycache__' not in x.name and 'googleDrive' not in x.name]  # get only valid files as best we can
        tried = False
        for fn in files: 
            if len(files) > 1:
                if str(fn) == 'index.tex':                              #if there is an index.tex , query for a dods.das file 
                    content = self.query_das()
                    if content == 'Invalid URL':
                        stack = None
                    elif content == 'Access Restricted':
                        self.restriction = 'requires dlauth tokens'
                        stack = None
                    elif content is not None:
                        stack = self.tokenize(content)
                    else:
                        stack = None
                    if stack is not None:
                        self.parse(stack)
                        found_das = True
                    tried = True
                else:                                                   #if there is more than one file, move those files to dirs of the same name / index.tex
                    new_dir = Path(str(fn))                             #get name of file 
                    new_dir.rename(str(fn) + '_temp')                   #rename fiel to file_temp
                    new_dir = Path(str(fn))                             #make new path object with file's old  name
                    new_dir.mkdir(parents=True, exist_ok=True)          #make a new dir with files old name 
                    Path(str(fn)+'_temp').rename(new_dir / 'index.tex') #move file to new dir / index.tex
                    tried = False
            else:                                                       #if there's one file (zero files, this won't execute) 
                content = self.query_das()
                if content == 'Invalid URL':
                    stack = None
                elif content == 'Access Restricted':
                    self.restriction = 'requires dlauth tokens'
                    stack = None
                elif content is not None:
                    stack = self.tokenize(content)
                else:
                    stack = None
                if stack is not None:
                    self.parse(stack)
                    found_das = True
                tried = True
            


        if not found_das and self.restriction == 'Public':
            try:
                if not tried:
                    content = self.query_das()
                    if content == 'Invalid URL':
                        stack = None
                    elif content == 'Access Restricted':
                        self.restriction = 'requires dlauth tokens'
                        stack = None
                    elif content is not None:
                        stack = self.tokenize(content)
                    else:
                        stack = None
                    if stack is not None:
                        self.parse(stack)
                        found_das = True
                    assert found_das == True, 'dingus'
                else:
                    assert False
            except:
                all_members = self.dir.glob('*')                                #find all sub dirs and files again 
                subdirs = sorted([x for x in all_members if x.is_dir() and 'html' not in x.name and \
                    '.owl' not in x.name and '.cuf' not in x.name and '.cdf' not in x.name and \
                        '.py' not in x.name  and '__pycache__' not in x.name and 'googleDrive' not in x.name])   #get only valid subdirs as best we can

                for sd in subdirs:                                              #for each valid subdir
                    setattr(self, sanitize_identifier(sd.name), Source(sd.name, parent=self, verbose=verbose))   #make a child node of sourcetree with its name 
                
                self.banned_long = ['dir', 'invalid', 'parent', 'name', 'banned', 'banned_long', 'iridl_ds_name', 'iridl_type']
                self.banned_long.extend([sanitize_identifier(sd.name) for sd in subdirs])

        print(self)
    

    def merge(self):
        if 'Attributes' in vars(self).keys():
            setattr(self.parent, sanitize_identifier(self.dir.name), getattr(self, 'Attributes'))
            setattr(getattr(self.parent, sanitize_identifier(self.dir.name)), 'dir', self.dir)
            setattr(getattr(self.parent, sanitize_identifier(self.dir.name)), 'iridl_ds_name', self.dir.name)
            setattr(getattr(self.parent, sanitize_identifier(self.dir.name)), 'parent', self.parent)
        else:
            for child in vars(self).keys():
                if child not in self.banned and type(getattr(self, child)) == Source:
                    getattr(self, child).merge() 


    #def fill_in(self):


    def __eq__(self, otr):
        ret = True
        if type(otr) == Source:
            for child in vars(self).keys():
                #print(child)
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
                                   # print(getattr(self, child)[item], getattr(otr, child)[item])
                        ret = ret and temp
                        #if not ret:
                         #   print(getattr(self, child), getattr(otr, child), temp, ret)

                    except:
                       # print(child)
                        
                        ret = False 
        else:
            ret = False 
            print('comparing dataset to nondataset')

        return ret



    @classmethod
    def from_json(self, json, parent=None):
        new = Source()
        new.parent = parent
        for obj in json.keys():
            if  type(json[obj]) == dict and json[obj]['iridl_type'] == 'DataSet':
                setattr(new, obj, DataSet.from_json(json[obj], parent=new))
            elif type(json[obj]) == dict and json[obj]['iridl_type'] == 'Source':
                setattr(new, obj, Source.from_json(json[obj], parent=new))
            elif obj == 'dir':
                setattr(new, obj, Path(json[obj]))
            else:
                setattr(new, obj, json[obj])
        return new
            

    def parse(self, stack):
        new_object, cur_object = None, self
        prev_token, pp_token = None, None 
        cur_token = stack.pop(-1)
        while len(stack) > 0:
            if cur_token == '}':
                new_object = DataSet()
                new_object.parent = cur_object 
                cur_object = new_object 
                cur_token = stack.pop(-1)
            elif cur_token == ';':
                value = stack.pop(-1)
                cur_token = stack.pop(-1)
                while cur_token not in ['{', ';']:
                    pp_token = prev_token 
                    prev_token = cur_token
                    cur_token = stack.pop(-1)
                name = pp_token
                setattr(cur_object, sanitize_identifier(name), value)
            elif cur_token == '{':
                name = stack.pop(-1)
                cur_object.iridl_ds_name = name
                setattr(cur_object.parent, sanitize_identifier(name), cur_object)
                if len(stack) > 0:
                    cur_token = stack.pop(-1)
                cur_object = cur_object.parent
            else:
                print('should never happen {}'.format(cur_token))
                cur_token = stack.pop(-1)
            

    def tokenize(self, content):
        content = str(content).replace('\\n', '').replace('\t', '')[2:-1]
        if content[0:10] != 'Attributes':
            return None
        strings = re.split('"', content)
        tokens = ''
        for i in range(len(strings)):
            if i % 2 == 0:
                tokens += strings[i]
            else: 
                tokens += '\t{}\t'.format(strings[i])
        new_tokens, in_string = [" ", '{', '}', ';'], False 
        tokens_f, cur = [], ''
        for char in tokens:
            if not in_string and char in new_tokens:
                if cur != '':
                    tokens_f.append(cur)
                if char != " ":
                    tokens_f.append(char)
                cur = ''
            elif in_string and char == '\t':
                tokens_f.append(cur)
                cur = ''
                in_string = False 
            elif not in_string and char == '\t':
                if cur != '':
                    tokens_f.append(cur)
                cur = '' 
                in_string = True
            elif in_string and char != '\t':
                cur += char 
            else: 
                cur += char 
        return tokens_f 

    def url(self):
        """return the url-valid version of this node"""
        return self.parent.url() + '.' + str(self.dir.name) + '/' if self.parent is not None else str(self.dir.name) + '/'


    def suggest_vars(self):
        base = 'https://iridl.ldeo.columbia.edu/'
        page = requests.get(base + self.url())
        soup = BeautifulSoup(page.content, 'html.parser')
        suggestions = soup.findAll("a", {'class':'share carryLanguage'})
        suggs, titles = [], []
        for suggestion in suggestions:
            if str(suggestion['href']) not in suggs: 
                suggs.append(str(suggestion['href']))
                titles.append(str(suggestion.contents))
        for sugg in range(len(suggs)): 
            #print('  {:<30}{:>50}'.format(suggs[sugg], titles[sugg] ))
            setattr(self, suggs[sugg], titles[sugg])

    def query_das(self):
        base = 'https://iridl.ldeo.columbia.edu/'
        url = base + self.url() + 'dods'
        try:
            page = requests.get(url , timeout = 10) 
            if page.status_code not in [401, 404]:
                url = url + '.das'
                page = requests.get(url, timeout=30)
                return page.content
            elif page.status_code == 404:
                print('Invalid URL {}'.format(url))
                return 'Invalid URL'
            else: 
                print('Restricted Access to {}'.format(url))
                return 'Access Restricted'   
        except: 
            print('unable to access {}'.format(url))
            return None

    def __str__(self):
        return 'Source({})'.format(self.dir)
    
    def __repr__(self):
        return 'Source({})'.format(self.dir)

    
    def avail(self):
        for child in sorted(vars(self).keys()):
            if child not in self.banned:
                if type(getattr(self, child)) == Source and getattr(getattr(self, child), 'restriction') != 'Public':
                    print('  .{:<30}{:>50}'.format(child, getattr(vars(self)[child], 'restriction')))
                else:
                    print('  .{:<30}{:>50}'.format(child, str(vars(self)[child])))
            

    def tree(self, depth=0, deep=False):
        print('  |'*depth + '-.{:<30}{:>50}'.format(self.dir.name, str(self)))
        for child in sorted(vars(self).keys()):
            if child not in self.banned:
                try:
                    vars(self)[child].tree(depth=depth+1, deep=deep)
                except:
                    if child == 'restriction' and self.restriction == 'Public':
                        pass
                    else:
                        print('  |'*(depth+1) + '-.{:<30.30}{:>30.30}'.format(child, str(vars(self)[child])))

    


    def json(self):
        ret = {'iridl_type': 'Source'}
        for child in vars(self).keys():
            if type(getattr(self, child)) in [Source, DataSet]:
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
