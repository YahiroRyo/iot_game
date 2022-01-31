from enum import Enum
import scene

class Command(Enum):
    NONE = 0
    YES_OR_NO = 1
    BATTLE_SELECT = 2

def command_select(num: Command):
    command_term_cnts = []
    unique_name = ""
    commands = []
    tmp_commands = []
    if num == Command.YES_OR_NO:
        tmp_commands = ["はい", "いいえ"]
        unique_name = "yes_or_no"
    elif num == Command.BATTLE_SELECT:
        tmp_commands = ["攻撃", "魔法", "特技", "道具", "防御", "逃げる"]
        unique_name = "battle_select"

    command_term_cnt = [0]
    tmp_command = []
    sum = 0
    print(tmp_commands)
    for tmp_cmd in tmp_commands:
        if sum * 24 + (len(tmp_cmd) - 1) * 24 >= scene.SW:
            sum = 0
            command_term_cnts.append(command_term_cnt)
            commands.append(tmp_command)
            command_term_cnt = [0]
            tmp_command = []
        sum += len(tmp_cmd) + 1
        tmp_command.append(tmp_cmd)
        command_term_cnt.append(sum)
    command_term_cnts.append(command_term_cnt)
    commands.append(tmp_command)
    return unique_name, commands, command_term_cnts