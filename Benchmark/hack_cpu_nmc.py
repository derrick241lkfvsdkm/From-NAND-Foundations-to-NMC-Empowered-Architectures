#!/usr/bin/env python3
# hack_cpu_nmc.py
# Hack CPU emulator with NMC extension (Near-Memory Computing)
# This version estimates cycle costs with acceleration for certain memory operations
import sys

def to_signed(val):
    """Convert 16-bit unsigned to signed (two's complement)"""
    if val & 0x8000:
        return val - 0x10000
    return val

def to_unsigned(val):
    """Convert signed to 16-bit unsigned"""
    return val & 0xFFFF

# Load hack binary file
if len(sys.argv) < 2:
    print("Usage: python3 hack_cpu_nmc.py <file.hack>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    instrs = [line.strip() for line in f if line.strip()]

# Initialize registers and 32K memory
A = 0
D = 0
PC = 0
RAM = [0] * 32768
instr_count = 0
cycle_cost = 0.0
max_cycles = 10000000

# Comp table
def compute_alu(comp_bits, D, A, RAM):
    """Compute ALU result based on comp bits"""
    D_signed = to_signed(D)
    A_signed = to_signed(A)
    M_signed = to_signed(RAM[A])
    
    comp_map = {
        "0101010": 0,                           # 0
        "0111111": 1,                           # 1
        "0111010": -1,                          # -1
        "0001100": D_signed,                    # D
        "0110000": A_signed,                    # A
        "1110000": M_signed,                    # M
        "0001101": ~D_signed,                   # !D
        "0110001": ~A_signed,                   # !A
        "1110001": ~M_signed,                   # !M
        "0001111": -D_signed,                   # -D
        "0110011": -A_signed,                   # -A
        "1110011": -M_signed,                   # -M
        "0011111": D_signed + 1,                # D+1
        "0110111": A_signed + 1,                # A+1
        "1110111": M_signed + 1,                # M+1
        "0001110": D_signed - 1,                # D-1
        "0110010": A_signed - 1,                # A-1
        "1110010": M_signed - 1,                # M-1
        "0000010": D_signed + A_signed,         # D+A
        "1000010": D_signed + M_signed,         # D+M
        "0010011": D_signed - A_signed,         # D-A
        "1010011": D_signed - M_signed,         # D-M
        "0000111": A_signed - D_signed,         # A-D
        "1000111": M_signed - D_signed,         # M-D
        "0000000": D_signed & A_signed,         # D&A
        "1000000": D_signed & M_signed,         # D&M
        "0010101": D_signed | A_signed,         # D|A
        "1010101": D_signed | M_signed,         # D|M
    }
    
    if comp_bits not in comp_map:
        raise ValueError(f"Unknown comp bits: {comp_bits}")
    
    result = comp_map[comp_bits]
    return to_unsigned(result)

def should_jump(jump_bits, val):
    """Determine if jump condition is met"""
    if jump_bits == "000":
        return False
    
    val_signed = to_signed(val)
    
    if jump_bits == "001":  # JGT
        return val_signed > 0
    elif jump_bits == "010":  # JEQ
        return val_signed == 0
    elif jump_bits == "011":  # JGE
        return val_signed >= 0
    elif jump_bits == "100":  # JLT
        return val_signed < 0
    elif jump_bits == "101":  # JNE
        return val_signed != 0
    elif jump_bits == "110":  # JLE
        return val_signed <= 0
    elif jump_bits == "111":  # JMP
        return True
    
    return False

# NMC acceleration patterns
# Pattern 1: D+M with M destination (read-modify-write on memory)
ACCEL_COMP_D_PLUS_M = "1000010"  # D+M
# Pattern 2: M+1 with M destination (increment memory)
ACCEL_COMP_M_PLUS_1 = "1110111"  # M+1
# Pattern 3: M-1 with M destination (decrement memory)
ACCEL_COMP_M_MINUS_1 = "1110010"  # M-1

# Execute instructions
pc_history = []

while 0 <= PC < len(instrs) and instr_count < max_cycles:
    # Detect halt: if PC cycles through same small set of addresses
    if len(pc_history) > 20:
        pc_history.pop(0)
    pc_history.append(PC)
    if len(pc_history) >= 20 and len(set(pc_history[-20:])) <= 2:
        # Stuck in a loop of 1-2 instructions
        break
    instr = instrs[PC]
    instr_count += 1
    
    if instr[0] == '0':
        # A-instruction: baseline cost
        A = int(instr, 2)
        cycle_cost += 1.0
        PC += 1
    else:
        # C-instruction: decode
        comp_bits = instr[3:10]
        dest_bits = instr[10:13]
        jump_bits = instr[13:16]
        
        # Compute ALU output
        val = compute_alu(comp_bits, D, A, RAM)
        
        # Determine cycle cost for this instruction
        cost = 1.0  # baseline
        
        # NMC acceleration: operations that read and write memory can be accelerated
        # because NMC performs computation near the memory
        if dest_bits[2] == '1':  # Writing to M (memory)
            if comp_bits in [ACCEL_COMP_D_PLUS_M, ACCEL_COMP_M_PLUS_1, ACCEL_COMP_M_MINUS_1]:
                # These operations benefit from near-memory computing
                # Reduced cost: 0.3 cycles instead of 1.0
                cost = 0.3
            elif comp_bits[0] == '1':  # Any M-based computation
                # Other M operations get moderate speedup
                cost = 0.5
        
        cycle_cost += cost
        
        # Write destinations (in parallel)
        old_A = A
        if dest_bits[0] == '1':  # A register
            A = val
        if dest_bits[1] == '1':  # D register
            D = val
        if dest_bits[2] == '1':  # M (RAM[A])
            RAM[old_A] = val
        
        # Compute next PC
        if should_jump(jump_bits, val):
            new_PC = A
            # Detect halt: unconditional jump to self
            if jump_bits == "111" and new_PC == PC:
                break  # Halted
            PC = new_PC
        else:
            PC += 1

# Print final state and metrics
print(f"(NMC-sim) Final A={A}, D={D}, PC={PC}, RAM[0..5]={RAM[:6]}")
print(f"(NMC-sim) Instructions executed: {instr_count}")
print(f"(NMC-sim) Estimated weighted cycles: {cycle_cost:.2f}")
print(f"(NMC-sim) Speedup factor: {instr_count / cycle_cost:.2f}x")

# Print matrix result if applicable
if RAM[65] != 0 or RAM[48] != 0:
    print(f"(NMC-sim) Matrix C result (RAM[48..63]):")
    for i in range(4):
        row = RAM[48 + i*4 : 48 + i*4 + 4]
        print(f"  Row {i}: {row}")
