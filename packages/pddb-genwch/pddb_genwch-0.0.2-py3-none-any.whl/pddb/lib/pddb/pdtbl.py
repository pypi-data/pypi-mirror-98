from abc import ABC, abstractmethod
import pandas as pd
from .columns import Column


class pdtbl(ABC):
    def __init__(self, owner: str = "system", debug: bool = False):
        (obj, path) = self.init_obj()
        obj = self.__set_sys_obj(obj)
        self._obj = self.__obj2col(obj)
        self._df = self.init_df(cols=[o.name for o in self._obj])
        self.__upddtm()
        self.set_owner(owner)
        self.set_debug(debug)
        self._path = path
        self.load()
        pass

    def set_owner(self, owner: str):
        self.owner = owner

    def set_debug(self, debug: bool):
        self.debug = debug

    def __set_sys_obj(self, obj: dict) -> dict:
        from datetime import datetime
        obj.update({"cre_dtm": {"type": datetime, "curdtm": True, "ignupd": True},
                    "cre_by": {"type": str, "owner": True, "ignupd": True},
                    "upd_dtm": {"type": datetime, "curdtm": True},
                    "upd_by": {"type": str, "owner": True}})
        return obj

    def cols(self, attr: str = None) -> list:
        if attr == None:
            return [o.name for o in self._obj]
        return [o.name for o in self._obj if o.get(attr, False)]

    def __upddtm(self) -> bool:
        from datetime import datetime
        self.datetime = datetime.now()
        return True

    def __obj2col(self, obj: dict) -> list:
        cnt = 0
        rtn = []
        for k, v in obj.items():
            if isinstance(v, type):
                v = {"type": v}
            v.update({"name": k, "iloc": cnt})
            rtn.append(self.__set_col(v))
            cnt += 1
        return rtn

    def __set_col(self, *args, **kwargs) -> Column:
        return Column(*args, **kwargs)

    @abstractmethod
    def init_obj(self) -> dict:
        pass

    def init_df(self, cols: list = []) -> pd.DataFrame:
        cols = self.cols() if cols == [] else cols
        return pd.DataFrame(columns=cols)

    def __conv_args(self, *args, **kwargs) -> dict:
        rtn = []
        for a in args:
            rtn = [a] if isinstance(a, dict) else a
            break
        if rtn == []:
            rtn = [kwargs]
        if kwargs != {}:
            nrtn = []
            for r in rtn:
                r.update(kwargs)
                nrtn.append(r)
            rtn = nrtn
        return rtn

    def filter(self, *args, **kwargs) -> (pd.DataFrame, list):
        df = kwargs.get("__df", pd.DataFrame())
        df = self._df if df.empty else df
        kwargs.update({"__gen_uuid": False})
        kwargs.update({"__cur_dtm": False})
        data = self.__prepare_data(*args, **kwargs)
        for d in data:
            for k, v in d.items():
                df = df[df[k] == v]
            break
        return (df, df.index.to_list())

    def isexists(self, *args, **kwargs) -> bool:
        df = kwargs.get("__df", pd.DataFrame())
        if not(df.empty):
            df = self._df if df.empty else df
            kwargs.update({"__df": df})
        _, idx = self.filter(*args, **kwargs)
        if idx == []:
            return False
        return True

    def check_require(self, data: dict) -> bool:
        for r in self.cols(attr="require"):
            if data.get(r, None) == None:
                return False
        return True

    def __set_uuid(self, data: dict) -> dict:
        import uuid
        for g in self.cols(attr="uuid"):
            if data.get(g, None) == None:
                data.update({g: str(uuid.uuid4())})
        return data

    def __set_md5(self, data: dict) -> dict:
        import hashlib
        for g in self.cols(attr="md5"):
            val = data.get(g, None)
            if val != None:
                data.update({g: hashlib.md5(val.encode()).hexdigest()})
        return data

    def __set_now(self, data: dict) -> dict:
        for g in self.cols(attr="curdtm"):
            val = data.get(g, None)
            if val == None:
                data.update({g: self.datetime})
        return data

    def __set_owner(self, data: dict) -> dict:
        for g in self.cols(attr="owner"):
            val = data.get(g, None)
            if val == None:
                data.update({g: self.owner})
        return data

    def __prepare_data(self, *args, **kwargs) -> list:
        data = self.__conv_args(*args, **kwargs)
        rtn = []
        for d in data:
            if d.get("__gen_uuid", True):
                d = self.__set_uuid(data=d)
            if d.get("__mask_md5", True):
                d = self.__set_md5(data=d)
            if d.get("__cur_dtm", True):
                d = self.__set_now(data=d)
                d = self.__set_owner(data=d)
            newd = {k: v for k, v in d.items() if k in self.cols()}
            rtn.append(newd)
        return rtn

    def update(self, *args, **kwargs) -> bool:
        if kwargs.get("__upddtm", True):
            self.__upddtm()
        data = self.__prepare_data(*args, **kwargs)
        df = self._df
        for d in data:
            if not(self.check_require(data=d)):
                return False
            filt = {k: v for k, v in d.items() if k in self.cols(attr="key")}
            df_filt, idx = self.filter(filt)
            if idx != []:
                if self.debug:
                    print(f"update {d}")
                for k, v in d.items():
                    if k not in self.cols(attr="key") and k not in self.cols(attr="uuid") and k not in self.cols(attr="ignupd"):
                        upd = pd.Series({i: v for i in idx})
                        df[k].update(upd)
            else:
                if self.debug:
                    print("not found")
                return False
        self._df = df
        return True

    def insert(self, *args, **kwargs) -> bool:
        import copy
        if kwargs.get("__upddtm", True):
            self.__upddtm()
        data = self.__prepare_data(*args, **kwargs)
        df = self._df
        for d in data:
            if not(self.check_require(data=d)):
                return False
            newd = copy.deepcopy(d)
            newd.update({"__df": df})
            exists = self.isexists(newd)
            if not exists:
                if self.debug:
                    print("insert", d)
                df = df.append(d, ignore_index=True)
            else:
                if self.debug:
                    print("exists")
                return False
        self._df = df
        return True

    def upsert(self, *args, **kwargs) -> bool:
        self.__upddtm()
        kwargs.update({"__upddtm": False})
        kwargs.update({"__mask_md5": False})
        data = self.__prepare_data(*args, **kwargs)
        df = self._df
        upd = []
        ins = []
        for d in data:
            newd = {k: v for k, v in d.items() if k in self.cols(attr="key")}
            if self.isexists(newd):
                upd.append(d)
            else:
                ins.append(d)
        if self.debug:
            print(f"ins {ins}")
        if not(self.insert(ins)):
            self._df = df
            return False
        if self.debug:
            print(f"upd {upd}")
        if not(self.update(upd)):
            self._df = df
            return False
        return True

    def __repr__(self) -> dict:
        return self._df.to_dict("records")

    def to_dict(self, df: pd.DataFrame) -> dict:
        df = self._df if df.empty else df
        return df.to_dict("records")

    def __str__(self) -> str:
        return self._df.to_string()

    def save(self, path: str = None) -> bool:
        path = self._path if path == None else path
        try:
            self._df.to_parquet(path=path, compression='gzip')
        except:
            return False
        return True

    def load(self, path: str = None) -> bool:
        path = self._path if path == None else path
        try:
            self._df = pd.read_parquet(path=path)
        except:
            return False
        return True
