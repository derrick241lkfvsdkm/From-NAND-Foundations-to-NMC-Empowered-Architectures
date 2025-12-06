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
