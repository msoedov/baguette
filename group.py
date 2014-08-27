import re


class Route(object):
    compiled = False

    def __init__(self, regexp, fn, name=None):
        self.regexp = regexp
        self.fn = fn
        self.name = None
        self.uses = []

    def compile(self):
        if self.compiled:
            raise ValueError('Already compiled')
        self.regexp = re.compile(self.regexp + '$')
        self.compiled = True
        return self

    def use(self, *mw):
        self.uses.extend(mw)
        return self

    def __repr__(self):
        return "path=%s, uses=%r" % (self.regexp, self.uses)


class Group(object):

    def __init__(self, path, *handlers):
        self.uses = []
        self.skipped = []
        self.handlers = handlers
        self.path = path
        
    def use(self, *mw):
        self.uses.extend(mw)
        return self

    def skip(self, *mw):
        self.skipped.extend(mw)
        return self

    def prepend(self, mws):
        self.uses = [m for m in mws if m not in self.skipped] + self.uses
        return self
    
    def as_handlers(self):
        as_result = []
        to_use = [m for m in self.uses if m not in self.skipped]
        for h in self.handlers:
            if isinstance(h, tuple):
                r, *_ = h
                r = Route(self.path + r, *_)
                r.uses = to_use
                as_result.append(r)
            elif isinstance(h, Route):
                h.use(*to_use[:])
                as_result.append(h)
                h.regexp = self.path + h.regexp
            elif isinstance(h, Group):
                rs = h.prepend(to_use).as_handlers()
                as_result.extend(rs)
        return as_result
