class Log(object):
    enable = False

    def __new__(cls, enable):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Log, cls).__new__(cls)
            cls.enable = enable
        return cls.instance

    def log(*arg):
        if Log.enable is not True:
            return
        for i in arg:
            print("log:" + str(i))
