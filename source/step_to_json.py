import json

stepPath = input("Please input .setp file\n")
jsonPath = input("Please input .json file\n")

dic = {}

# read .step file to dict and only read DATA part.
with open(stepPath, 'r') as file:
    flag = True
    idx  = -1
    obj = ''
    for line in file:
        line = line.replace(' ', '')
        if flag:
            if line.strip() == 'DATA;':
                flag = False
            continue
        if line.strip() == 'ENDSEC;':
            dic[idx] = obj
            break
        if line[0] == '#' and '=' in line:
            if idx != - 1:
                dic[idx] = obj
                obj = ''
            idx = int(line.split('#')[1].split('=')[0])
            obj += line.split('=')[1]
        else:
            obj += line
        if idx != -1:
            dic[idx] = obj

def procValue(value : str) -> dict:
    lst = []
    attributeId = value[:value.find('(')]
    value = value[value.find('(')+1:value.rfind(')')]
    while value != '' and not len(value) < 2:
        if value[0] == '\'':
            pos = value.find('\'', 1)
            lst.append(value[1:pos])
            value = value[value.find('\'', 1) + 1:]
        elif value[0] == '(':
            flag = 0
            for pos in range(0, len(value)):
                if value[pos] == '(':
                    flag += 1
                elif value[pos] == ')':
                    flag -= 1
                else:
                    pass
                if flag == 0:
                    lst.append(procValue(value[0:pos+1])[''])
                    value = value[pos+2:]
                    break
        elif value[0] == '.':
            pos = value.find('.', 1)
            if value[1:pos] == 'T':
                lst.append('True')
            elif value[1:pos] == 'F':
                lst.append('False')
            elif value[1:pos] == 'UNSPECIFIED':
                lst.append('UNSPECIFIED')
            else:
                lst.append(value[1:pos])
            value = value[pos+2:]
        elif value[0] == '#':
            pos = value.find(',')
            if pos == -1:
                pos = len(value)
            index = int(value[1:pos])
            lst.append(procValue(dic[index]))
            value = value[pos+1:]
        elif value[0] == '*':
            lst.append('*')
            pos = value.find(',')
            value = value[pos+1:]
        elif value[0].isalpha():
            flag = -1
            for pos in range(0, len(value)):
                if value[pos] == '(':
                    if flag == -1:
                        flag = 1
                    else:
                        flag += 1
                elif value[pos] == ')':
                    flag -= 1
                else:
                    pass
                if flag == 0:
                    break
            lst.append(procValue(value[0:pos+1]))
            value = value[pos+1:]
        elif value[0].isdigit() or value[0] == '-':
            pos = value.find(',')
            if pos == -1:
                pos = len(value)
            num = float((value[0:pos]))
            lst.append(num)
            value = value[pos+1:]
        else:
            value = value[1:]
    return {attributeId: lst}

result = {}

# eg. CLOSED_SHELL
rootID = input("Please input root ID\n")

for key, value in dic.items():
    attributeId = value[:value.find('(')]
    if attributeId == rootID:
        result = procValue(value)
        break

with open(jsonPath, 'w+') as file:
    jsonStr = json.dumps(result, indent=2)
    file.write(jsonStr)

print("Success!")
