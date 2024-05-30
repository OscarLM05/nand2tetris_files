import sys

def init_symbol_table():
    """Initializes symbol table with predefined symbols and their address"""
    symbol_table={}
    symbol_table["SP"]=0
    symbol_table["LCL"]=1
    symbol_table["ARG"]=2
    symbol_table["THIS"]=3
    symbol_table["THAT"]=4
    symbol_table["R0"]=0
    symbol_table["R1"]=1
    symbol_table["R2"]=2
    symbol_table["R3"]=3
    symbol_table["R4"]=4
    symbol_table["R5"]=5
    symbol_table["R6"]=6
    symbol_table["R7"]=7
    symbol_table["R8"]=8
    symbol_table["R9"]=9
    symbol_table["R10"]=10
    symbol_table["R11"]=11
    symbol_table["R12"]=12
    symbol_table["R13"]=13
    symbol_table["R14"]=14
    symbol_table["R15"]=15
    symbol_table["SCREEN"]=16384
    symbol_table["KBD"]=24576

    return symbol_table

def label_process(input_lines, symbol_table):
    """Takes care of labels to make the code usable"""
    line_number=0
    used_lines=[]

    for line in input_lines:
        parsed_line=parse(line)
        if parsed_line.startswith("(") and parsed_line.endswith(")"):
            needed=parsed_line[1:-1] #This gets just the label name.
            symbol_table[needed]=line_number #This adds the label and its line number to symbol_table.
        elif parsed_line:
            used_lines.append(parsed_line)
            line_number+=1

    return used_lines

def generate_machine_code(line, symbol_table, next_address):
    """Converts assembly code into binary"""
    jump_lookup=init_jump_lookup_dict()
    dest_lookup=init_dest_lookup_dict()
    comp_lookup=init_comp_lookup_dict()

    if line.startswith("@"):
        symbol=line[1:]
        if symbol.isdigit():
            address=int(symbol)
        else:
            if symbol not in symbol_table:
                symbol_table[symbol]=next_address
                next_address+=1
            address=symbol_table[symbol]
        return f"0{address:015b}", next_address #015b is what changes it to binary.
    
    else:
        dest,comp,jump="null",line,"null"
        if "=" in line:
            dest,comp=line.split("=")
        elif ";" in comp:
            comp,jump=comp.split(";")

        return f"111{comp_lookup[comp]}{dest_lookup[dest]}{jump_lookup[jump]}", next_address

def init_jump_lookup_dict():
    """Initializes jump table with predefined symbols and their address"""
    jump_lookup={}
    jump_lookup["null"]="000"
    jump_lookup["JGT"]= "001"
    jump_lookup["JEQ"]= "010"
    jump_lookup["JGE"]= "011"
    jump_lookup["JLT"]= "100"
    jump_lookup["JNE"]= "101"
    jump_lookup["JLE"]= "110"
    jump_lookup["JMP"]= "111"

    return jump_lookup

def init_dest_lookup_dict():
    """Initializes destination table with predefined symbols and their address"""
    dest_lookup={}
    dest_lookup["null"]="000"
    dest_lookup["M"]=   "001"
    dest_lookup["D"]=   "010"
    dest_lookup["DM"]=  "011"
    dest_lookup["MD"]=  "011"
    dest_lookup["A"]=   "100"
    dest_lookup["AM"]=  "101"
    dest_lookup["MA"]=  "101"
    dest_lookup["AD"]=  "110"
    dest_lookup["DA"]=  "110"
    dest_lookup["ADM"]= "111"
    dest_lookup["AMD"]= "111"
    dest_lookup["DAM"]= "111"
    dest_lookup["DMA"]= "111"
    dest_lookup["MAD"]= "111"
    dest_lookup["MDA"]= "111"

    return dest_lookup

def init_comp_lookup_dict():
    """Initializes computation table with predefined symbols and their address"""
    comp_lookup={}
    comp_lookup["0"]=   "0101010"
    comp_lookup["1"]=   "0111111"
    comp_lookup["-1"]=  "0111010"
    comp_lookup["D"]=   "0001100"
    comp_lookup["A"]=   "0110000"
    comp_lookup["!D"]=  "0001101"
    comp_lookup["!A"]=  "0110001"
    comp_lookup["-D"]=  "0001111"
    comp_lookup["-A"]=  "0110011"
    comp_lookup["D+1"]= "0011111"
    comp_lookup["A+1"]= "0110111"
    comp_lookup["D-1"]= "0001110"
    comp_lookup["A-1"]= "0110010"
    comp_lookup["D+A"]= "0000010"
    comp_lookup["D-A"]= "0010011"
    comp_lookup["A-D"]= "0000111"
    comp_lookup["D&A"]= "0000000"
    comp_lookup["D|A"]= "0010101"
    comp_lookup["M"]=   "1110000"
    comp_lookup["!M"]=  "1110001"
    comp_lookup["-M"]=  "1110011"
    comp_lookup["M+1"]= "1110111"
    comp_lookup["M-1"]= "1110010"
    comp_lookup["D+M"]= "1000010"
    comp_lookup["D-M"]= "1010011"
    comp_lookup["M-D"]= "1000111"
    comp_lookup["D&M"]= "1000000"
    comp_lookup["D|M"]= "1010101"

    return comp_lookup

def parse(input_line):
    """Removes whitespace and comments from the assembly code"""
    # strip white space
    output_line=input_line.strip()

    # double forward slash dectector with split
    output_line=output_line.split("//")[0].strip()

    return output_line


def main():
    """Opens file, converts to binary, and makes a .hack file with the binary"""
    input_filename=sys.argv[1]
    output_filename=input_filename.replace(".asm",".hack")

    input_file_contents=[]

    with open(input_filename, "r") as input_file:
        input_file_contents=input_file.readlines()

    symbol_table=init_symbol_table()
    good_lines=label_process(input_file_contents,symbol_table)

    machine_code_lines=[]
    next_address=16

    for line in good_lines:
        machine_code, next_address=generate_machine_code(line,symbol_table ,next_address)
        machine_code_lines.append(machine_code)

    with open(output_filename,"w") as output_file:
        for code in machine_code_lines:
            output_file.write(code+"\n")


if __name__=="__main__":
    main()