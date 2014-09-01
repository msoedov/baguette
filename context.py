class Context(object):

    def __getattr__(self, attr):
        return self.__dict__.get(attr, None)
