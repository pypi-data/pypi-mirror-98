def throw(exception):
    print(str(exception))
    exit()
def interpret(code):
    addr = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    vaddr = [0,0,0,0,0,0,0,0]
    var = {} #todo: make this impact available address space?
    opcodes = ['put', 'vput', 'prnt', 'equl', 'vequl', 'cpy', 'flsh', 'vflsh', 'mov', 'jmp', 'jie', 'dump', 'vdump']
    out = ''
    #with open(argv[1]) as file:
        #lines = [line.rstrip('\n').split(' ') for line in file]
    lines = code
    #print(lines)
    lc = 1
    for oc in lines:
        i=0
        for av in opcodes:
            i+=oc[0].find(av)
        if i == -13 and not oc[0].startswith('#') and not oc[0] == '':
            return "Unknown opcode " + str(oc[0]) + "\n(Line " + str(lc) + ")"
        lc+=1
    i=0
    infcheck = 0
    while i < len(lines):
        inst = lines[i]
        if infcheck >= 1000:
            return "Infinte loop suspected! Please fix code"
        if inst[0] == 'put':
            #check and make sure that args are within constraints
            if int(inst[1]) > 1 or int(inst[1]) < 0:
                return 'Attempted to put value other than 0 or 1 in address space'
            if int(inst[2]) > len(addr) - 1:
                return 'Attempted to write value to address index higher than available'
            #if not, actually do code
            addr[int(inst[2])] = int(inst[1])
        if inst[0] == 'vput':
            #check and make sure that args are within constraints
            if int(inst[1]) > 1 or int(inst[1]) < 0:
                return 'Attempted to put value other than 0 or 1 in address space'
            if int(inst[2]) > len(vaddr) - 1:
                return 'Attempted to write value to address index higher than available'
            #if not, actually do code
            vaddr[int(inst[2])] = int(inst[1])
        if inst[0] == 'prnt':
            newvaddr = [str(i) for i in vaddr]
            out+=chr(int(''.join(newvaddr[:-1]), 2))
            if vaddr[len(vaddr) - 1] == 1:
                out+='\n'
        if inst[0] == 'equl':
            if addr[int(inst[1])] == addr[int(inst[2])]:
                addr[int(inst[3])] = 1
            else:
                addr[int(inst[3])] = 0
        if inst[0] == 'vequl':
            if vaddr[int(inst[1])] == vaddr[int(inst[2])]:
                vaddr[int(inst[3])] = 1
            else:
                vaddr[int(inst[3])] = 0
        if inst[0] == 'cpy':
            vaddr[int(inst[2])] = addr[int(inst[1])]
        if inst[0] == 'flsh':
            addr = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        if inst[0] == 'vflsh':
            vaddr = [0,0,0,0,0,0,0,0]
        if inst[0] == 'mov':
            vaddr[int(inst[2])] = addr[int(inst[1])]
            addr[int(inst[1])] = 0
        if inst[0] == 'dump':
            out += str(addr) + '\n'
        if inst[0] == 'vdump':
            out += str(vaddr) + '\n'
        if inst[0].startswith('#'):
            pass #comments
        if inst[0] != 'jmp' and inst[0] != 'jie':
            i += 1
        if inst[0] == 'jmp':
            i = int(inst[1])
            infcheck+=1
        if inst[0] == 'jie':
            if addr[int(inst[1])] == addr[int(inst[2])]:
                i = int(inst[3])
            else:
                i += 1
    return out
if __name__ == "__main__":
    from sys import argv
    with open(argv[1]) as file:
            lines = [line.rstrip('\n').split(' ') for line in file]
    print(interpret(lines))
