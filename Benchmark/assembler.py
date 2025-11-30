#!/usr/bin/env python3
# assembler.py
# Simple Hack assembler (Hack assembly -> Hack binary)
import sys
import os

class Assembler:
    def __init__(self, file_path):
        self.codes = []
        self.binary = []
        self.allo = 16
        # Predefined symbols (R0-R15, SCREEN, KBD, etc.)
        self.sym = {
            "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
            "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7,
            "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
            "SCREEN": 16384, "KBD": 24576
        }
        # Code tables for C-instructions (comp, dest, jump)
        self.comp = {
            "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000", "M": "1110000",
            "!D": "0001101", "!A": "0110001", "!M": "1110001", "-D": "0001111", "-A": "0110011", "-M": "1110011",
            "D+1": "0011111", "A+1": "0110111", "M+1": "1110111", "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
            "D+A": "0000010", "D+M": "1000010", "D-A": "0010011", "D-M": "1010011", "A-D": "0000111", "M-D": "1000111",
            "D&A": "0000000", "D&M": "1000000", "D|A": "0010101", "D|M": "1010101"
        }
        self.dest = {
            "null": "000", "M": "001", "D": "010", "MD": "011",
            "A": "100", "AM": "101", "AD": "110", "AMD": "111"
        }
        self.jump = {
            "null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
            "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
        }
        self.file = os.path.basename(file_path)
        assert self.file.endswith(".asm"), "Input file must be .asm"
        # Read and clean lines
        with open(file_path) as f:
            for line in f:
                line = line.split('//')[0].strip()  # remove comments
                if line:
                    self.codes.append(line)

    def first_pass(self):
        """First pass: process labels and build symbol table"""
        new_codes, pc = [], 0
        for line in self.codes:
            if line.startswith('(') and line.endswith(')'):
                label = line[1:-1]
                self.sym[label] = pc
            else:
                new_codes.append(line)
                pc += 1
        self.codes = new_codes

    def to_binary(self):
        """Second pass: convert instructions to binary"""
        for line in self.codes:
            if line.startswith('@'):  # A-instruction
                symbol = line[1:]
                if symbol.isdigit():
                    addr = int(symbol)
                else:
                    if symbol not in self.sym:
                        self.sym[symbol] = self.allo
                        self.allo += 1
                    addr = self.sym[symbol]
                self.binary.append(f"{addr:016b}")
            else:  # C-instruction
                # Split dest=comp;jump
                if '=' in line:
                    dest, rest = line.split('=', 1)
                    dest = dest.strip()
                else:
                    dest, rest = "null", line
                if ';' in rest:
                    comp, jmp = rest.split(';', 1)
                    comp = comp.strip()
                    jmp = jmp.strip()
                else:
                    comp, jmp = rest.strip(), "null"
                
                if comp not in self.comp:
                    raise ValueError(f"Unknown comp mnemonic: {comp} in line: {line}")
                if dest not in self.dest:
                    raise ValueError(f"Unknown dest mnemonic: {dest} in line: {line}")
                if jmp not in self.jump:
                    raise ValueError(f"Unknown jump mnemonic: {jmp} in line: {line}")
                
                bits = "111" + self.comp[comp] + self.dest[dest] + self.jump[jmp]
                self.binary.append(bits)

    def write_out(self):
        """Write binary output to .hack file"""
        out_file = self.file[:-4] + ".hack"
        with open(out_file, 'w') as f:
            for code in self.binary:
                f.write(code + "\n")
        print(f"Assembled {len(self.binary)} instructions to {out_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 assembler.py <file.asm>")
        sys.exit(1)
    path = sys.argv[1]
    asm = Assembler(path)
    asm.first_pass()
    asm.to_binary()
    asm.write_out()

if __name__ == "__main__":
    main()
