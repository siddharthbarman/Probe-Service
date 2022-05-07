import sys

class CmdLine:
    def __init__(self, flag_prefix, argv):
        self.argv = argv
        self.flag_prefix = flag_prefix
        self.dict = {}
        self.arglist = []
        self.__parse()

    def __parse(self):        
        flag_name = None        
        for arg in self.argv:            
            if self.__is_flag(arg):
                flag_name = self.__get_flag_name(arg)
                self.dict[flag_name] = None                
            else:
                if flag_name == None:
                    self.arglist.append(arg)
                else:
                    self.dict[flag_name] = arg
                    flag_name = None
            
            print(arg, "is flag:", self.__is_flag(arg))

    def is_flag_present(self, flag):
        return flag in self.dict

    def get_flag_value(self, flag):
        return self.dict[flag]

    def get_flag_value_default(self, flag, default_value):        
        try:
            result = self.dict[flag]
        except:
            result = default_value
        return result

    def __is_flag(self, value):
        return value.startswith(self.flag_prefix) and len(value) > len(self.flag_prefix)

    def __get_flag_name(self, value):
        if self.__is_flag(value):
            result = value[len(self.flag_prefix):]
        else:
            result = value        
        return result

#cmd = CmdLine('-', sys.argv)
#print("Is bar a flag?", cmd.is_flag_present("bar"))
#print("Is foo a flag?", cmd.is_flag_present("foo"))
#print("Value of a foo:", cmd.get_flag_value("foo"))

