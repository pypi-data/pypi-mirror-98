import logging
class Logging:
    @staticmethod
    def print(file,line,func,excepiton,level=0):
        logging.error("[+++++]file:{},line:{},Function:{},Exception:{}".format(file, line,
                                                                               func, str(excepiton)))