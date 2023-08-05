from pyclibrary import CParser
import sys
import pathlib


def generateClass(struct_name, name, data):
    class_str = " "
    class_str = "\nclass "+struct_name+"(cstruct.CStruct):\n\
    __byte_order__ = cstruct.LITTLE_ENDIAN\n\
    __struct__ =\"\"\""
    temp_members = " "
    for i in range(0, len(name)):
        temp_members += "\n"
        temp_members += "       {}".format(name[i])
    class_str += temp_members+"\n       \"\"\"\n"
    temp_members    =   "\n    def get_dict(self):\n"
    temp_members    +=  "        m_json = {}\n"
    for i in range(0, len(name)):
        temp_members    +=  "        m_json['{}'] = self.{}\n".format(data[i], data[i])
    class_str       +=  temp_members+"        return m_json\n"
    '''
    Generate binary function
    '''
    temp_members    =   "\n    def get_binary(self, json_data):\n"
    for i in range(0, len(name)):
        temp_members    +=  "        self.{} = json_data['{}']\n".format(data[i], data[i])
    return class_str+temp_members

def main():
    if(len(sys.argv) > 1):
        try:
            parser = CParser([str(sys.argv[1])])
        except:
            print("Unable to parse the header file")
            sys.exit()
        data_structure = []
        d_structs = ["veryHighPriorityData_t", "highPriorityData_t", "normalPriorityData_t", "lowPriorityData_t", "veryLowPriorityData_t", "asyncData_t"]
        try:
            for i in range(0, 6):
                data_structure.append(parser.defs['types'][str(d_structs[i])])
        except:
            print("Fundamental structure key name error")
            sys.exit()
        struct_data = [0]*6
        member_name = [0]*6
        for i in range(0, len(data_structure)):
            val = data_structure[i].type_spec.split(' ')
            temp = parser.defs['structs'][str(val[1])]
            struct_data[i] = []
            member_name[i] = []
            '''
            Generate the structure string
            '''
            for j in range(0, len(temp.members)):
                temp_struct_string = " "
                temp_type = temp.members[j][1].type_spec
                temp_arrLen  = temp.members[j][1].declarators
                if(len(temp_arrLen) > 0):
                    temp_struct_string = str(temp_type)+" "+temp.members[j][0]+str(temp_arrLen[0])+";"
                else:
                    temp_struct_string = str(temp_type)+" "+temp.members[j][0]+";"
                member_name[i].append(temp.members[j][0])
                struct_data[i].append(temp_struct_string)
            print(struct_data[i])
            print("\n")
        print(member_name)
        path = pathlib.Path(__file__).parent.absolute()
        filename = str(path)+"\\jfw_structs.py"
        with open(filename, "w+") as f:
            f.write("import cstruct\n")
            for i in range(0,len(d_structs)):
                f.write(generateClass(str(d_structs[i]),struct_data[i], member_name[i]))
                f.write("\n")
        f.close()
    else:
        print("Please provide header filepath")

if __name__ == "__main__":
    main()