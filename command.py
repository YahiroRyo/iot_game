from distutils import command

commandmsg_1=["はい","いいえ"]
command_1=["1","0"]
command_1msgwordcount=[0,3]

def command_select(A):
    if A == 1:
        return commandmsg_1,command_1,command_1msgwordcount
