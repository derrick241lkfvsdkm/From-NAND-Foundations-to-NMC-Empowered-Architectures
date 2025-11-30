# Hack CPU Benchmark Suite

This directory contains a complete Python-based implementation of the Hack CPU simulator and benchmarking tools for comparing standard Hack CPU performance against an NMC (Near-Memory Computing) augmented version.

## Files

### Core Implementation
- **assembler.py** - Hack assembler that converts .asm files to .hack binary
- **hack_cpu.py** - Standard Hack CPU simulator
- **hack_cpu_nmc.py** - NMC-augmented Hack CPU simulator with cycle cost estimation
- **benchmark.py** - Benchmark harness to compare both simulators

### Test Programs
- **Add.asm** - Simple addition test
- **MatMul2x2.asm** - 2×2 matrix multiplication with initialization
- **MatMul.asm** - 4×4 matrix multiplication (core logic)
- **MatMul_Full.asm** - 4×4 matrix multiplication with data initialization
- **SimpleStore.asm** - Test for indirect addressing

### Utilities
- **init_matmul.py** - Generates MatMul_Full.asm with matrix initialization

## Key Fixes Applied

### 1. Assembler Improvements
- Added proper error handling for unknown mnemonics
- Fixed comment parsing
- Improved symbol table management

### 2. CPU Simulator Fixes
- **Signed arithmetic**: Properly handles 16-bit two's complement arithmetic
- **Halt detection**: Detects infinite loops (e.g., `@HALT; 0;JMP`)
- **Indirect addressing**: Fixed bug where A register was overwritten during indirect writes

### 3. Matrix Multiplication Bug Fixes
- **Address calculation**: Fixed i*4 and k*4 calculations
  - Original code: `temp=i; D=temp+temp; D=D+temp` → 3*i (WRONG)
  - Fixed code: `temp=i; D=i+i; temp=2*i; D=2*i+2*i` → 4*i (CORRECT)
- **Indirect write**: Fixed sequence to load D before overwriting A
  - Original: `A=RAM[addr]; A=33; D=RAM[33]; M=D` (writes to RAM[33])
  - Fixed: `D=RAM[33]; A=RAM[addr]; M=D` (writes to RAM[addr])

### 4. NMC Acceleration Model
The NMC simulator models near-memory computing by reducing cycle costs for memory-intensive operations:
- Operations like `D+M` with M destination: 0.3 cycles (vs 1.0)
- Other M-based operations: 0.5 cycles
- Demonstrates ~1-2% speedup on matrix multiplication workloads

## Usage

### 1. Assemble a program
```bash
python3 assembler.py program.asm
```

### 2. Run on standard CPU
```bash
python3 hack_cpu.py program.hack
```

### 3. Run on NMC CPU
```bash
python3 hack_cpu_nmc.py program.hack
```

### 4. Run benchmark comparison
```bash
python3 benchmark.py program.hack
```

## Example Output

```
======================================================================
Benchmarking: MatMul_Full.hack
======================================================================
Running Standard Hack CPU:
----------------------------------------------------------------------
Final A=256, D=0, PC=257, RAM[0..5]=[0, 0, 0, 0, 0, 0]
Instructions executed: 5223
Matrix C result (RAM[48..63]):
  Row 0: [1, 2, 3, 4]
  Row 1: [5, 6, 7, 8]
  Row 2: [9, 10, 11, 12]
  Row 3: [13, 14, 15, 16]

Running NMC-Augmented Hack CPU:
----------------------------------------------------------------------
(NMC-sim) Final A=256, D=0, PC=257, RAM[0..5]=[0, 0, 0, 0, 0, 0]
(NMC-sim) Instructions executed: 5223
(NMC-sim) Estimated weighted cycles: 5164.20
(NMC-sim) Speedup factor: 1.01x
(NMC-sim) Matrix C result (RAM[48..63]):
  Row 0: [1, 2, 3, 4]
  Row 1: [5, 6, 7, 8]
  Row 2: [9, 10, 11, 12]
  Row 3: [13, 14, 15, 16]
======================================================================
```

## Technical Details

### Hack Architecture
- 16-bit CPU with two registers: A (address) and D (data)
- 32K RAM (addresses 0-32767)
- Harvard architecture (separate instruction and data memory)
- Two instruction types:
  - A-instruction: `@value` → loads value into A register
  - C-instruction: `dest=comp;jump` → ALU operation with conditional jump

### Memory Map for Matrix Multiplication
- Matrix A: RAM[16..31] (4×4 = 16 words)
- Matrix B: RAM[32..47] (4×4 = 16 words)
- Matrix C: RAM[48..63] (4×4 = 16 words)
- Loop variables: RAM[65-67] (i, j, k)
- Temporary variables: RAM[68-76]

## Requirements
- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Notes
- The matrix multiplication uses repeated addition for multiplication (no hardware multiply)
- The 4×4 matrix multiplication takes ~5,200 instructions
- The 2×2 matrix multiplication takes ~720 instructions
- Halt detection triggers after 10+ cycles of PC not advancing
