import copy
import json
import os
from json import JSONDecodeError
from shutil import copyfile

NUMPY_AVAILABLE = 0
try:
    import numpy as np

    NUMPY_AVAILABLE = 1
except:
    pass

VERBOSE = False


class JsonMultiEncoder(json.JSONEncoder):
    def default(self, obj):
        if NUMPY_AVAILABLE:
            if isinstance(obj, np.ndarray):
                return obj.tolist()

            if isinstance(obj, np.number):
                if obj.itemsize > 6:
                    return str(obj.item())
                return obj.item()

        if isinstance(obj, set):
            return list(obj)

        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)



class AbstractJsonDict:
    def __init__(self, data=None, autosave=False, encoder=JsonMultiEncoder, backup=True, check_timestamp=True,
                 check_filesize=True,default_as_json_dict=True):

        self.default_as_json_dict = default_as_json_dict
        self.check_filesize = check_filesize
        self.check_timestamp = check_timestamp
        if encoder is None:
            encoder = JsonMultiEncoder
        self.backup = backup
        self._encoder = None
        self.encoder = encoder
        self._autosave = autosave
        self._data = {}
        self._file = None
        if data is not None:
            self.data = data
        if autosave:
            self.autosave = autosave

    def _set_data(self, data,save=True):
        self._data = data
        if save and self.file:
            self.save()

    def _get_data(self, reload=True):
        if self.file and reload:
            if self.check_timestamp or self.check_filesize:
                if (self.check_timestamp and os.path.getmtime(self.file) > self._timestamp) or \
                        (self.check_filesize and os.path.getsize(self.file) != self._file_size and os.path.getsize(self.file) > 0):
                    if VERBOSE:
                        print("relaod file", self.file)
                    self.read(self.file)
        return self._data

    def _update_data(self, target, source, overwrite=True):
        for key, value in source.items():
            if not key in target:
                target[key] = value
            elif isinstance(target.get(key), dict) and isinstance(value, dict):
                self._update_data(target.get(key), value, overwrite=overwrite)
            elif overwrite:
                target[key] = value

    def update_data(self, dict_like, overwrite=True, autosave=True):
        if isinstance(dict_like, AbstractJsonDict):
            dict_like = dict_like.data
        assert isinstance(dict_like, dict), dict_like.__class__.__name__ + " is not a dict object"
        self._update_data(self.data, dict_like, overwrite=overwrite)
        if self.autosave and autosave:
            self.save()

    def set_data(self, data,save=True):
        self._set_data(data,save=save)

    def get_data(self, reload=True):
        return self._get_data(reload=reload)

    data = property(get_data, set_data)

    def _set_file(self, file):
        if not os.path.exists(file):
            raise FileNotFoundError(file)
        if self.check_timestamp:
            self._timestamp = os.path.getmtime(file)
        if self.check_filesize:
            self._file_size = os.path.getsize(file)
        self._file = file

    def _get_file(self):
        return self._file

    def set_file(self, file):
        self._set_file(file)

    def get_file(self):
        return self._get_file()

    file = property(get_file, set_file)

    def _set_encoder(self, encoder):
        self._encoder = encoder

    def _get_encoder(self):
        return self._encoder

    def set_encoder(self, encoder):
        self._set_encoder(encoder)

    def get_encoder(self):
        return self._get_encoder()

    encoder = property(get_encoder, set_encoder)

    def _set_autosave(self, autosave):
        self._autosave = autosave

    def _get_autosave(self):
        return self._autosave

    def set_autosave(self, autosave):
        self._set_autosave(autosave)

    def get_autosave(self):
        return self._get_autosave()

    autosave = property(get_autosave, set_autosave)

    def read(self, file):
        if VERBOSE:
            print("read file", file)
        with open(file) as f:
            self.data = json.loads(f.read())
        self._timestamp = os.path.getmtime(file)
        self._file_size = os.path.getsize(file)

    def get(self, *args, default=None, autosave=True, as_json_dict=None, reload=True):
        if as_json_dict is None:
            as_json_dict=self.default_as_json_dict
        d = self.get_data(reload=reload)
        args = [str(arg) for arg in args]
        for arg in args[:-1]:
            if arg not in d and autosave:
                d[arg] = {}
            if arg not in d:
                return default
            d = d[arg]

        if args[-1] not in d and autosave:
            self.put(*args, value=default, autosave=autosave, reload=False)
        if args[-1] not in d:
            return default

        o = d[args[-1]]

        if isinstance(o, dict) and as_json_dict:
            return self.getsubdict(*args)
        if isinstance(o, list) and as_json_dict:
            return JsonList(preamble=args,jsondict=self)
        try:
            o = copy.deepcopy(o)
        except:
            pass
        return o

    def put(self, *args, value, autosave=True, reload=True):
        d = self.get_data(reload=reload)
        args = [str(arg) for arg in args]
        for arg in args[:-1]:
            if arg not in d:
                d[arg] = {}
            d = d[arg]

        new = False
        if args[-1] not in d:
            new = True
            d[args[-1]] = None
        elif d[args[-1]] != value:
            new = True
        preval = d[args[-1]]
        d[args[-1]] = value

        if new or (preval != value):
            if self.autosave and autosave and self.file:
                self.save()

        return value, new

    def save(self):
        assert self.file is not None, "no file specified"
        if self.file is not None:
            if VERBOSE:
                print("save file", self.file)
            with open(self.file, "w+") as outfile:
                self.stringify_keys()
                self.to_json_stream(outfile,reload=False, indent=4, sort_keys=True)
            if self.backup:
                copyfile(self.file, self.file + "_bu")
            if self.check_timestamp:
                self._timestamp = os.path.getmtime(self.file)
            if self.check_filesize:
                self._file_size = os.path.getsize(self.file)

    def __getitem__(self, key):
        return self.data[key]

    def stringify_keys(self, diction=None):
        if diction is None:
            diction = self.get_data(reload=False)
        for k in list(diction.keys()):
            if isinstance(diction[k], dict):
                self.stringify_keys(diction=diction[k])
            diction[str(k)] = diction.pop(k)

    def to_json_string(self, reload=True, cls=None, **kwargs):
        if cls is None:
            cls = self.encoder
        return json.dumps(
            self.get_data(reload=reload), cls=cls, **kwargs
        )

    def to_json_stream(self, fp, reload=True, cls=None, **kwargs):
        if cls is None:
            cls = self.encoder
        return json.dump(self.get_data(reload=reload), fp, cls=cls, **kwargs)

    def to_json(self, *args, **kwargs, ):
        return self.to_json_string(*args, **kwargs)

    def get_base_dict(self):
        return self.get_parent(highest=True)

    def get_parent(self, highest=False):
        if not highest:
            return self.parent
        return self.parent.get_parent(highest=highest)

    def getsubdict(self, preamble=None, *args):
        if preamble is None:
            preamble = []
        if isinstance(preamble, tuple):
            preamble = list(preamble)
        if not isinstance(preamble, list):
            preamble = [preamble]
        preamble = preamble + list(args)
        return JsonSubDict(parent=self, preamble=preamble)

    def __str__(self):
        return self.to_json_string()


class JsonDict(AbstractJsonDict):
    def __init__(
            self, file=None, data=None, createfile=True, autosave=True, *args, **kwargs,

    ):
        if data is not None:
            if isinstance(data, str):
                data = json.loads(data)
            elif isinstance(data, JsonDict):
                data = data.data

        self._timestamp = 0
        self._file_size = 0
        super().__init__(data=data, autosave=autosave, *args, **kwargs)

        if file is not None:
            if data is None:
                self.read(file, createfile=createfile)
            else:
                self.save(file)
    def read(self, file, createfile=False):
        if file:
            file = os.path.abspath(file)
        try:
            super().read(file)
            self.file = os.path.abspath(file)
            self.timestamp = os.path.getmtime(file)
        except JSONDecodeError:
            self.read(file + "_bu", createfile=False)
        except (FileNotFoundError, JSONDecodeError) as e:
            if createfile:
                os.makedirs(os.path.dirname(file), exist_ok=True)
                self.save(file=file)
                self.read(file, createfile=False)
            else:
                raise e

   # def _set_data(self, data, file=None,save=True):
   #     if file is not None:
   #         self.file = os.path.abspath(file)
   #     super()._set_data(data,save=save)

    def save(self, file=None):
        if file is not None:
            os.makedirs(os.path.dirname(file), exist_ok=True)
            if not os.path.exists(file):
                with open(file, "w+") as outfile:
                    pass
            self.file = os.path.abspath(file)
        super().save()

    def get_parent(self, highest=True):
        return self


class JsonSubDict(AbstractJsonDict):
    def _set_data(self, data,save=True):
        assert isinstance(data, dict), "data is not a dictionary"
        self.parent.put(*self.preamble, value=data,autosave=save)

    def _get_data(self, reload=True):
        return self.parent.get(*self.preamble, default={}, as_json_dict=False, reload=reload)

    def _get_file(self):
        return self.parent.get_file()

    def _get_autosave(self):
        return self.parent.get_autosave()

    def _get_encoder(self):
        return self.parent.get_encoder()

    def save(self):
        self.parent.save()

    def __init__(self, parent, preamble):
        super().__init__(default_as_json_dict=parent.default_as_json_dict)
        if isinstance(preamble, tuple):
            preamble = list(preamble)
        if not isinstance(preamble, list):
            preamble = [preamble]
        self.preamble = preamble
        self.parent = parent
        self.parent.get(*self.preamble, default={}, as_json_dict=False)

    @property
    def _timestamp(self):
        return self.parent._timestamp

    @property
    def _file_size(self):
        return self.parent._file_size

    def get(self, *args, **kwargs):
        return self.parent.get(
            *(self.preamble + list(args)), **kwargs
        )

    def put(self, *args, value, **kwargs):
        return self.parent.put(*(self.preamble + list(args)), value=value, **kwargs)

class JsonList():
    def __init__(self,preamble,jsondict:JsonDict):
        self._jsondict = jsondict
        self._preamble=preamble

    @property
    def list(self):
        return list(self._jsondict.get(*self._preamble, as_json_dict=False))

    def __getitem__(self, item):
        return self.list[item]

    def __setitem__(self, key, value):
        l=self.list
        l[key]=value
        self._jsondict.put(*self._preamble,value=l)

    def __len__(self):
        return len(self.list)

    def __getattr__(self, item):
        l=self.list
        attr=getattr(l,item)
        self._jsondict.put(*self._preamble,value=l)
        return attr

    def __str__(self):
        return str(self.list)

if __name__ == "__main__":
    d1 = JsonDict('{"test":[1,2.5,{}]}')
    print(d1)
    a = d1.get("test", default=[])
    a[2]["foo"] = "bar"
    d1.put("test", value=a)
    print(d1)
    d2 = d1.getsubdict("sub1")
    d2.put("sub_", value="folder")
    print(d1)
    print(d2.data)
    d3 = d2.getsubdict(["sub", "dic"])
    print(d2)
    print(d1)
    print(d3.get_base_dict())
    print(d3.get_parent())
    print(d3.get_parent(highest=True))
    print(d3)
