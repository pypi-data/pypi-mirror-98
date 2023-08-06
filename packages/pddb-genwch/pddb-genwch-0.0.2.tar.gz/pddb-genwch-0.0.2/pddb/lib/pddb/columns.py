from abc import ABC


class Column(ABC):
    def __init__(self, *args, **kwargs):
        self.set_col(*args, **kwargs)

    def set_col(self, *args, **kwargs):
        for a in args:
            kwargs.update(a)
            break
        self.idx = kwargs.get("iloc", 0)
        self.name = kwargs.get("name", f"col{self.idx}")
        self.type = kwargs.get("type", str)
        self.key = kwargs.get("key", False)
        self.uuid = kwargs.get("uuid", False)
        self.md5 = kwargs.get("md5", False)
        self.owner = kwargs.get("owner", False)
        self.curdtm = kwargs.get("curdtm", False)
        self.igncre = kwargs.get("igncre", False)
        self.ignupd = kwargs.get("ignupd", False)
        self.require = kwargs.get("require", False or self.key)
        self.default = kwargs.get("default", None)

    def get(self, attr, default=None):
        default=self.default if default==None else default
        attrs=self.__dict__
        return attrs.get(attr, default)

    def __repr__(self):
        d=[f"{k}: {v}" for k, v in self.__dict__.items()]
        # rtn="{%s}" % (", ".join(d))
        return "{%s}" % (", ".join(d))
