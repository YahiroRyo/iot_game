from distutils import command

def command_select(num: int):
    if num == 1:
        command_msgs=["はい", "いいえ"]
        command_term_cnt = [0]
        sum = 0
        for i in range(1, len(command_msgs)):
            sum += len(command_msgs[i - 1]) + 1
            command_term_cnt.append(sum)
        return command_msgs, command_term_cnt
