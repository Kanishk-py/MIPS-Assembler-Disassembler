from pyparsing import *
from bitstring import BitArray

#helper conversion functions

def bin_to_hex(bin_str):
    decimal_representation = int(bin_str, 2)
    return hex(decimal_representation)
    

def decimal_to_binary(dec, n_bits):
    if int(dec) < 0:
        dec = int(dec)
        b = BitArray(int=dec,length=n_bits)
        return b.bin
    else:
        return bin(int(dec))[2:].zfill(n_bits)


#We are identifying different ways in which the mips instructions can appear:

#format 0: operation reg,reg,reg
#format 1: operation reg,reg,integer
#format 2: operation reg
#format 3: operation reg,integer
#format 4: operation reg,intger(reg)
#format 5: operation reg,reg,address

instruction_data = {} #This dictionary contains details about each instruction 

#Arithmetic Operations:
instruction_data['add']   =   {'type': 'R', 'format': 0, 'opcode': '000000', 'funct': '100000'}
instruction_data['sub']   =   {'type': 'R', 'format': 0, 'opcode': '000000', 'funct': '100010'}
instruction_data['addi']  =   {'type': 'I', 'format': 1, 'opcode': '001000'}
instruction_data['addu']  =   {'type': 'R', 'format': 0, 'opcode': '000000', 'funct': '100001'}
instruction_data['subu']  =   {'type': 'R', 'format': 0, 'opcode': '000000', 'funct': '100011'}
instruction_data['addiu'] =   {'type': 'I', 'format': 1, 'opcode': '001001'}
instruction_data['mflo']  =   {'type': 'R', 'format': 2, 'opcode': '000000', 'funct': '010010'}
instruction_data['mfhi']  =   {'type': 'R', 'format': 2, 'opcode': '000000', 'funct': '010000'}
#Data Transfer Operations
instruction_data['lw']    =   {'type': 'I', 'format': 4, 'opcode': '100011'}
instruction_data['sw']    =   {'type': 'I', 'format': 4, 'opcode': '101011'}
instruction_data['lhu']   =   {'type': 'I', 'format': 4, 'opcode': '100101'}
instruction_data['sh']    =   {'type': 'I', 'format': 4, 'opcode': '101001'}
instruction_data['lbu']   =   {'type': 'I', 'format': 4, 'opcode': '100100'}
instruction_data['sb']    =   {'type': 'I', 'format': 4, 'opcode': '101000'}
instruction_data['ll']    =   {'type': 'I', 'format': 1, 'opcode': '110000'}
instruction_data['sc']    =   {'type': 'I', 'format': 4, 'opcode': '111000'}
instruction_data['lui']   =   {'type': 'I', 'format': 3, 'opcode': '001111'}
#Logical Operations
instruction_data['and']   =   {'type': 'R', 'format': 0, 'opcode': '000000', 'funct': '100100'}
instruction_data['or']    =   {'type': 'R', 'format': 0, 'opcode': '000000', 'funct': '100101'}
instruction_data['nor']   =   {'type': 'R', 'format': 0, 'opcode': '000000', 'funct': '100111'}
instruction_data['andi']  =   {'type': 'I', 'format': 1, 'opcode': '001100'}
instruction_data['ori']   =   {'type': 'I', 'format': 1, 'opcode': '001101'}
instruction_data['sll']   =   {'type': 'R', 'format': 1, 'opcode': '000000', 'funct': '000000'}
instruction_data['srl']   =   {'type': 'R', 'format': 1, 'opcode': '000000', 'funct': '000010'}
#Conditional Branching Operations
instruction_data['beq']   =   {'type': 'I', 'format': 5, 'opcode': '000100'}
instruction_data['bne']   =   {'type': 'I', 'format': 5, 'opcode': '000101'}
instruction_data['slt']   =   {'type': 'R', 'format': 0, 'opcode': '000000', 'funct': '101010'}
instruction_data['slti']  =   {'type': 'I', 'format': 1, 'opcode': '001010'}
instruction_data['sltu']  =   {'type': 'R', 'format': 0, 'opcode': '000000', 'funct': '101011'}
instruction_data['sltiu'] =   {'type': 'I', 'format': 1, 'opcode': '001011'} 
#Unconditional Jump Operations
instruction_data['j']     =   {'type': 'J', 'opcode': '000010'}
instruction_data['jr']    =   {'type': 'R', 'format': 2, 'opcode': '000000', 'funct': '001000'}
instruction_data['jal']   =   {'type': 'J', 'opcode': '000011'}


#Classifying operations
R_format_0 = []
R_format_1 = []
R_format_2 = []
I_format_1 = []
I_format_3 = []
I_format_4 = []
I_format_5 = []
J  = []

for instruction in instruction_data.keys():
    if instruction_data[instruction]['type'] == 'R':
        if instruction_data[instruction]['format'] == 0: R_format_0.append(instruction)
        if instruction_data[instruction]['format'] == 1: R_format_1.append(instruction)
        if instruction_data[instruction]['format'] == 2: R_format_2.append(instruction)
        
    if instruction_data[instruction]['type'] == 'I':
        if instruction_data[instruction]['format'] == 1: I_format_1.append(instruction)
        if instruction_data[instruction]['format'] == 3: I_format_3.append(instruction)
        if instruction_data[instruction]['format'] == 4: I_format_4.append(instruction)
        if instruction_data[instruction]['format'] == 5: I_format_5.append(instruction)
    
    if instruction_data[instruction]['type'] == 'J': J.append(instruction) 

#register dictionary:

registers = {}
registers['$zero']=0
registers['$at']=1
registers['$v0']=2
registers['$v1']=3
registers['$a0']=4
registers['$a1']=5
registers['$a2']=6
registers['$a3']=7
registers['$t0']=8
registers['$t1']=9
registers['$t2']=10
registers['$t3']=11
registers['$t4']=12
registers['$t5']=13
registers['$t6']=14
registers['$t7']=15
registers['$s0']=16
registers['$s1']=17
registers['$s2']=18
registers['$s3']=19
registers['$s4']=20
registers['$s5']=21
registers['$s6']=22
registers['$s7']=23
registers['$t8']=24
registers['$t9']=25
registers['$k0']=26
registers['$k1']=27
registers['$gp']=28
registers['$sp']=29
registers['$fp']=30
registers['$ra']=31
for s in range(0,31):
    registers['$%d'%s]=s
registers[''] = 0
    
valid_regs = list(registers.keys())
valid_regs.remove('')


# Making datatypes to store MIPS instructions
label_address =  Word(alphas+"_",alphanums+"_")
register = oneOf(valid_regs)
number = Combine(Optional('-') + Word(nums))
EOL = OneOrMore(LineEnd())

Label = label_address.setResultsName("label") + Suppress(":")
register_rs = register.setResultsName('rs')
register_rt = register.setResultsName('rt')
register_rd = register.setResultsName('rd')
immediate_value = number.setResultsName('imm')
addr = label_address.setResultsName("address")

# Setting data types of R,I and J type Instructions
R_format = (oneOf(R_format_0).setResultsName('operation') + White() + register_rd + ',' + register_rs + ',' + register_rt) ^\
           (oneOf(R_format_1).setResultsName('operation') + White() + register_rd + ',' + register_rt + ',' + number.setResultsName('shamt')) ^\
           (oneOf(R_format_2).setResultsName('operation') + White() + register_rs)

I_format = (oneOf(I_format_1).setResultsName('operation') + White() + register_rt + ',' + register_rs + ',' + immediate_value) ^\
           (oneOf(I_format_3).setResultsName('operation') + White() + register_rt + ',' + immediate_value) ^\
           (oneOf(I_format_4).setResultsName('operation') + White() + register_rt + ',' + immediate_value + '(' + register_rs + ')') ^\
           (oneOf(I_format_5).setResultsName('operation') + White() + register_rs + ',' + register_rt + ',' + addr)

J_format = oneOf(J).setResultsName('operation') + White() + addr

# Setting data type for Instruction
Instruction =   ((Label) + (R_format ^ I_format ^ J_format)) ^\
                (Label) ^ (R_format ^ I_format ^ J_format) ^ EOL.setResultsName('EOL')


def assemble(bin_input):
    initial_address = 0
    # Opening Input file
    input_file = open("MIPS.txt", 'r')
    # Opening output file
    output_file = open('machine.txt','w')

    Instruction_Memory = []
    Labels = {}

    line_address = initial_address
    try:
        # Parsing the input Instruction in Instruction_Memory array
        for instructions in input_file:
            current_instruction = Instruction.parseString(instructions)    
            if len(current_instruction) == 0: 
                continue
            if current_instruction[0] == '\n': 
                continue
            Instruction_Memory.append(current_instruction)
            # If the address of Instruction is Labelled
            if current_instruction.label != '':
                if current_instruction.operation != '': 
                    Labels[current_instruction.label] = line_address
                else :  
                    Labels[current_instruction.label] = line_address
                    continue
            line_address += 4 

        input_file.close()

        #Assembling the parsed code
        PC = initial_address
        for instructions in Instruction_Memory:
            if instructions.operation == '':
                continue
            oper = instruction_data[instructions.operation]
            PC += 4
            
            # Writing Machine code on basis of R type, I type or J type instructions
            if oper['type'] == 'R':
                opcode = oper['opcode']
                funct = oper['funct']
                # Calculation of Shift amount
                if instructions.shamt != '': 
                    shamt = instructions.shamt
                else: 
                    shamt = 0
                rs_code = registers[instructions.rs]
                rt_code = registers[instructions.rt]
                rd_code = registers[instructions.rd]
                # Writing Instruction code
                inst_mcode = opcode + decimal_to_binary(rs_code,5) + decimal_to_binary(rt_code,5) + decimal_to_binary(rd_code,5) +\
                            decimal_to_binary(shamt,5) + funct
                if bin_input == 0 :
                    inst_mcode = str(bin_to_hex(inst_mcode))
                output_file.write(inst_mcode + '\n')
                # print(inst_mcode)
            
            if oper['type'] == 'I':
                opcode = oper['opcode']
                rs_code = registers[instructions.rs]
                rt_code = registers[instructions.rt]
                if instructions.imm != '': 
                    imm = instructions.imm
                else:
                    address = Labels[instructions.address]
                    imm = (address - PC)/4
                # Writing Instruction code
                inst_mcode = opcode + decimal_to_binary(rs_code,5) + decimal_to_binary(rt_code,5) + decimal_to_binary(imm,16)
                if bin_input == 0 :
                    inst_mcode = str(bin_to_hex(inst_mcode))
                output_file.write(inst_mcode + '\n')
                # print(inst_mcode)
                
            if oper['type'] == 'J':
                opcode = oper['opcode']
                address = Labels[instructions.address]
                address = decimal_to_binary(address,32)
                address = address[4:]
                address = int(address,2)
                address = address/4
                address = decimal_to_binary(address,26)
                # Writing Instruction code
                inst_mcode = opcode + address
                if bin_input == 0 :
                    inst_mcode = str(bin_to_hex(inst_mcode))
                output_file.write(inst_mcode + '\n')
                # print(inst_mcode)
        
        output_file.close()
    except:
        # Error handling
        output_file.write("Error !" '\n')
        output_file.close()
        input_file.close()