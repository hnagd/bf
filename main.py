def run():
    global list
    global nodepointer
    global programpointer
    global program
    
    global consoleout
    
    instruction = program[programpointer]
    
    if (instruction == "+"):
        list[nodepointer] = (list[nodepointer] + 1) % 256
        
    elif (instruction == "-"):
        list[nodepointer] = (list[nodepointer] - 1) % 256
        
    elif (instruction == ">"):
        nodepointer += 1
        
    elif (instruction == "<"):
        nodepointer -= 1
        
    elif (instruction == "."):
        print(hex(list[nodepointer]))
        consoleout.append(hex(list[nodepointer]))
        
    elif (instruction == ","):
        catch = 1
        while catch == 1:
            try:
                val = int(input("input:"), 16)
            except:
                print("invalaid input. Please enter a hexidecimal number between 00 and FF")
            else:
                catch = 0
        
        list[nodepointer] = val % 256
        
    elif (instruction == "["):
        if (list[nodepointer] == 0):
            depth = 1
            while (program[programpointer] != "]") or (depth != 0):
                programpointer += 1
                if (program[programpointer] == "["):
                    depth += 1
                if (program[programpointer] == "]") & (depth > 0):
                    depth -= 1
            
    elif (instruction == "]"):
        if (list[nodepointer] != 0):
            depth = 1
            while (program[programpointer] != "[") or (depth != 0):
                programpointer -= 1
                if (program[programpointer] == "]"):
                    depth += 1
                if (program[programpointer] == "[") & (depth > 0):
                    depth -= 1

    programpointer += 1

    
# print the list in hex
def renderlist():
    global consoleout
    global list
    
    print("")
    print("Output:")
    print(','.join(consoleout))
    
    print("")
    print("Cells:")
    i = 0
    while i<20:
        print(','.join(convhex(list[i*20:i*20+19])))
        i += 1

# convert int to hex
def convhex(list0):
    i = 0
    hex0 = list0
    while i<len(list0):
        hex0[i] = (hex(hex0[i]))[2:]
        
        if (len(hex0[i])<2): #prepend zeros
            hex0[i] = "0" + hex0[i]
        
        i += 1
    
    return hex0
    
    
 # remove comments from program
def processprogram():
    global rawprogram
    global program
    program = ""
    i = 0
    while (i<len(rawprogram)):
        if (rawprogram[i:i+2] == "//"):
            while (rawprogram[i] != "\n" and i < len(rawprogram)-1):
                i += 1
        elif (rawprogram[i] == "/*"):
            while (rawprogram[i:i+2] != "*/"):
                i += 1
            i += 2
        program = program + rawprogram[i]
        i +=1
        
    
def parsecommands():
    global programpointer
    global program
    global rawprogram
    global nodepointer
    global consoleout
    command = input(":")
    
    #step program
    if (command[0:2] == "st"):
        if (len(command) > 3):
            i = 0
            while i < int(command[3:]) and (programpointer < len(program)-1):
                run()
                i += 1
        else:
            run()
        renderlist()
    
    #single line
    elif (command[0:2] == "ln"):
        while program[programpointer] != "\n" and (programpointer < len(program)-1):
            run()
        programpointer += 1
        renderlist()
    
    #run program
    elif (command[0:3] == "run"):
        while programpointer < len(program):
            run()
        renderlist()
    
    elif (command[0:3] == "ref"):
        with open("program.txt") as f:
            rawprogram = f.read()
        print("\nRaw program:\n")
        print(rawprogram)
        processprogram()
        list = [0] * 30 * 1000
        nodepointer = 0
        programpointer = 0
        consoleout = []
        
    elif (command[0:3] == "raw"):
        print("\nRaw program:\n")
        print(rawprogram)
        
    elif (command[0:3] == "com"):
        print("\nFiltered program:")
        print(program)
        print("")
    elif (command[0:3] == "hlp"):
        instructions()
    else:
        print("\ninvalaid command!")
    
    
# init variables
list = [0] * 30 * 1000
nodepointer = 0
programpointer = 0
consoleout = []

# read file
with open("program.txt") as f:
    rawprogram = f.read()
processprogram()
print("File loaded.\n")
# program start
def instructions():
    print("Commands:")
    print("hlp - brings this back up")
    print("st - step program 1 instruction")
    print("st [int] - step program int instructions")
    print("ln - progress the program 1 line")
    print("run - run the program to completion")
    #print("ref - refresh program from file") doesn't work
    print("raw - print raw program")
    print("com - get filtered program (program without comments)")
    print("")
instructions()
while programpointer < len(program):
    parsecommands()
