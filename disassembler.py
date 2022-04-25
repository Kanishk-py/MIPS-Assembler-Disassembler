from bitstring import BitArray

# We have here defined a dict that stores the information of the type of instruction through the opcode:
opcode_data = {}

opcode_data['0'] = {'type': 'R'}

opcode_data['8'] = {'type': 'I', 'opperation': 'addi', 'format': 0}
opcode_data['c'] = {'type': 'I', 'opperation': 'andi', 'format': 0}
opcode_data['a'] = {'type': 'I', 'opperation': 'slti', 'format': 0}
opcode_data['b'] = {'type': 'I', 'opperation': 'sltiu', 'format': 0}
opcode_data['d'] = {'type': 'I', 'opperation': 'or', 'format': 0}

opcode_data['23'] = {'type': 'I', 'opperation': 'lw', 'format': 1}
opcode_data['2b'] = {'type': 'I', 'opperation': 'sw', 'format': 1}

opcode_data['4'] = {'type': 'I', 'opperation': 'beq', 'format': 2}
opcode_data['5'] = {'type': 'I', 'opperation': 'bne', 'format': 2}

opcode_data['2'] = {'type': 'J', 'opperation': 'j'}
opcode_data['3'] = {'type': 'J', 'opperation': 'jal'}


# We have here defined a dict that stores the information of the type of instruction through the function code for R type instruction:
func_data = {}

func_data['20'] = {'opperation': 'add', 'format': 0}
func_data['22'] = {'opperation': 'sub', 'format': 0}
func_data['24'] = {'opperation': 'and', 'format': 0}
func_data['25'] = {'opperation': 'or', 'format': 0}
func_data['27'] = {'opperation': 'nor', 'format': 0}
func_data['2a'] = {'opperation': 'slt', 'format': 0}
func_data['0'] = {'opperation': 'sll', 'format': 1}
func_data['2'] = {'opperation': 'srl', 'format': 1}
func_data['12'] = {'opperation': 'mflo', 'format': 2}
func_data['10'] = {'opperation': 'mfhi', 'format': 2}
func_data['8'] = {'opperation': 'jr', 'format': 2}

# We have here stored the value of each register
registers = {}
registers[0] = '$zero'
registers[1] = '$at'
registers[2] = '$v0'
registers[3] = '$v1'
registers[4] = '$a0'
registers[5] = '$a1'
registers[6] = '$a2'
registers[7] = '$a3'
registers[8] = '$t0'
registers[9] = '$t1'
registers[10] = '$t2'
registers[11] = '$t3'
registers[12] = '$t4'
registers[13] = '$t5'
registers[14] = '$t6'
registers[15] = '$t7'
registers[16] = '$s0'
registers[17] = '$s1'
registers[18] = '$s2'
registers[19] = '$s3'
registers[20] = '$s4'
registers[21] = '$s5'
registers[22] = '$s6'
registers[23] = '$s7'
registers[24] = '$t8'
registers[25] = '$t9'
registers[26] = '$k0'
registers[27] = '$k1'
registers[28] = '$gp'
registers[29] = '$sp'
registers[30] = '$fp'
registers[31] = '$ra'

# Functions that convert Hex, Decimal and Binary to each other :


def hex_to_bin(hex_str, n_bits):
    return bin(int(hex_str, 16))[2:].zfill(n_bits)


def dec_to_bin(dec, n_bits):
    if int(dec) < 0:
        dec = int(dec)
        b = BitArray(int=dec, length=n_bits)
        return b.bin
    else:
        return bin(int(dec))[2:].zfill(n_bits)


def bin_to_dec(bin_str, n_bits):
    sign = bin_str[0]
    if sign == '0':
        return int(bin_str, 2)
    elif sign == '1':
        comp = int(bin_str[1:], 2)
        dec = (2**(n_bits-1)) - comp
        return -1*dec


def disassemble(bin_input):
    input_file = open("machine.txt", 'r')  # Input File
    output_file = open('MIPS.txt', 'w')  # Output File

    # Defining Initial address as the start of the memory. We could even take this as an input from users
    initial_address = 0
    # Defining PC
    PC = initial_address

    instructions = []  # List that stores all the instructions
    addresses = []  # List that stores all the addresses that come up through various instructions
    labels = {}  # Dict that stores the Label values for each of the address

    try:
        for line in input_file:
            if line == '\n':
                instruction = None
                break
            if bin_input == 0:
                line = str(hex_to_bin(line, 32))
                if(len(line) == 10):
                    line = line[:2]

            # Converting Binary opcode to hex and removing leading '0x'
            opcode = hex(int(line[0:6], 2))[2:]
            # Data here stores the information of the instruction
            data = opcode_data[opcode]
            PC += 4  # Incrementing PC

            # For R type instructions
            if data['type'] == 'R':
                rs = registers[int(line[6:11], 2)]
                rt = registers[int(line[11:16], 2)]
                rd = registers[int(line[16:21], 2)]
                shamt = int(line[21:26], 2)
                funct = hex(int(line[26:32], 2))[2:]
                opperation = func_data[funct]['opperation']
                format = func_data[funct]['format']

                # Here we have stored the R type instruction depending on the format of the instruction
                if format == 0:
                    instruction = [opperation + ' ' +                   # We can see that each instruction has 2 attributes where the 2nd
                                   rd + ', ' + rs + ', ' + rt, None]    # attribute tells weather that particular instruction uses some
                # address in it. Here as we can see no address has to be reffered
                if format == 1:
                    instruction = [opperation + ' ' + rd + ', ' +       # in these R type instructions, so the 2nd attribute is None.
                                   rt + ', ' + str(shamt), None]
                if format == 2:
                    instruction = [opperation + ' ' + rs, None]

            # For I type instructions
            if data['type'] == 'I':
                opperation = data['opperation']
                format = data['format']
                rs = registers[int(line[6:11], 2)]
                rt = registers[int(line[11:16], 2)]
                immediate_value = str(bin_to_dec(line[16:], 16))

                # Here we have stored the I type instruction depending on the format of the instruction
                if format == 0:
                    instruction = [opperation + ' ' + rt +
                                   ', ' + rs + ', ' + immediate_value, None]
                if format == 1:
                    instruction = [opperation + ' ' + rt +
                                   ', ' + immediate_value + '(' + rs + ')', None]
                if format == 2:
                    address = PC + int(immediate_value)*4
                    if address not in addresses:
                        addresses.append(address)
                    instruction = [opperation + ' ' +
                                   rs + ', ' + rt + ', ', address]

            # For J type instructions
            if data['type'] == 'J':
                opperation = data['opperation']

                address = int(line[6:], 2) << 2
                address = dec_to_bin(address, 28)
                address = dec_to_bin(PC, 32)[0:4] + address
                address = int(address, 2)

                if address not in addresses:
                    addresses.append(address)
                instruction = [opperation + ' ', address]

            instructions.append(instruction)

        addresses.sort()                    # Here we will assign each address that comes up
        i = 1                               # in the instructions with a Label
        for address in addresses:
            labels[address] = 'Label%d' % i
            i += 1

        mem = 0
        for instruction in instructions:    # We will add each instruction to the output file through this loop
            if instruction == None:
                continue

            instruction_address = initial_address + mem
            # If a particular instruction address has a label then we store it in the label variable
            if labels.get(instruction_address) is not None:
                label = labels.get(instruction_address)
            else:
                label = ''

            if instruction[1] == None:
                if label == '':
                    output_file.write(instruction[0] + '\n')
                else:
                    output_file.write(label + ': ' + instruction[0] + '\n')
            else:
                if label == '':
                    output_file.write(
                        instruction[0] + labels[instruction[1]] + '\n')
                else:
                    output_file.write(
                        label + ': ' + instruction[0] + labels[instruction[1]] + '\n')
            mem += 4

        output_file.close()
        input_file.close()
    except:
        output_file.write("Error !" '\n')
        output_file.close()
        input_file.close()
