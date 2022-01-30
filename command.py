from enum import Enum

class Command(Enum):
    NONE = 0
    YES_OR_NO = 1
    BATTLE_SELECT = 2

def command_select(num: Command):
    command_term_cnt = [0]
    unique_name = ""
    commands = []
    if num == Command.YES_OR_NO:
        commands = ["はい", "いいえ"]
        unique_name = "yes_or_no"
    elif num == Command.BATTLE_SELECT:
        commands=["攻撃", "魔法", "特技", "道具", "防御", "逃げる"]
        unique_name = "battle_select"
    sum = 0
    for i in range(1, len(commands)):
        sum += len(commands[i - 1]) + 1
        command_term_cnt.append(sum)
    return unique_name, commands, command_term_cnt