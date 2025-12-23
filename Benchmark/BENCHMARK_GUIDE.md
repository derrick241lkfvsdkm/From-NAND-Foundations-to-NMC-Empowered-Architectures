# Matrix Multiplication Benchmark Guide

This guide explains how to benchmark matrix multiplication operations on the Hack CPU (standard vs NMC-augmented) using matrices of different sizes.

## Table of Contents
1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [System Components](#system-components)
4. [Creating Custom Matrix Sizes](#creating-custom-matrix-sizes)
5. [Running Benchmarks](#running-benchmarks)
6. [Understanding Results](#understanding-results)
7. [Troubleshooting](#troubleshooting)

---

## Overview

The benchmark system compares the performance of:
- **Standard Hack CPU**: Traditional CPU without near-memory computing
- **NMC-Augmented Hack CPU**: Enhanced CPU with near-memory computing capabilities

The system measures cycle counts and execution time for matrix multiplication operations.

---

## Quick Start

For the default 4×4 matrix benchmark:

```bash
# 1. Generate the matrix initialization code
python3 init_matmul.py

# 2. Assemble the program
python3 assembler.py MatMul_Full.asm

# 3. Run the benchmark
python3 benchmark.py MatMul_Full.hack
```

---

## System Components

### Core Files

- **[assembler.py](assembler.py)**: Converts Hack assembly (.asm) to machine code (.hack)
- **[benchmark.py](benchmark.py)**: Runs both CPU simulators and compares performance
- **[init_matmul.py](init_matmul.py)**: Generates matrix initialization code
- **[MatMul.asm](MatMul.asm)**: Matrix multiplication algorithm (4×4 by default)
- **hack_cpu.py**: Standard Hack CPU simulator
- **hack_cpu_nmc.py**: NMC-augmented CPU simulator

### Memory Layout

The default memory organization for 4×4 matrices:
- **Matrix A**: RAM[16..31] (16 locations for 4×4 matrix)
- **Matrix B**: RAM[32..47] (16 locations for 4×4 matrix)
- **Matrix C**: RAM[48..63] (16 locations for result)
- **Variables**: RAM[65+] (loop counters, temporary values)

---

## Creating Custom Matrix Sizes

### Step 1: Modify the Initialization Script

Edit [init_matmul.py](init_matmul.py) to support your desired matrix size. Here's an example for 8×8 matrices:

```python
#!/usr/bin/env python3
# init_matmul.py
# Initialize matrix data in RAM for testing MatMul

def create_matmul_init():
    """Create an assembly program that initializes matrices A and B"""
    asm_code = []

    # Define matrix size
    MATRIX_SIZE = 8  # Change this for different sizes

    # Matrix A: Identity matrix for easy verification
    A = [[1 if i == j else 0 for j in range(MATRIX_SIZE)]
         for i in range(MATRIX_SIZE)]

    # Matrix B: Sequential values for testing
    B = [[i * MATRIX_SIZE + j + 1 for j in range(MATRIX_SIZE)]
         for i in range(MATRIX_SIZE)]

    # Base addresses - adjust spacing based on matrix size
    BASE_A = 16
    BASE_B = 16 + MATRIX_SIZE * MATRIX_SIZE

    asm_code.append(f"// Initialize Matrix A at RAM[{BASE_A}..{BASE_A + MATRIX_SIZE * MATRIX_SIZE - 1}]")
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            addr = BASE_A + i * MATRIX_SIZE + j
            val = A[i][j]
            asm_code.append(f"@{val}")
            asm_code.append("D=A")
            asm_code.append(f"@{addr}")
            asm_code.append("M=D")

    asm_code.append(f"\n// Initialize Matrix B at RAM[{BASE_B}..{BASE_B + MATRIX_SIZE * MATRIX_SIZE - 1}]")
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            addr = BASE_B + i * MATRIX_SIZE + j
            val = B[i][j]
            asm_code.append(f"@{val}")
            asm_code.append("D=A")
            asm_code.append(f"@{addr}")
            asm_code.append("M=D")

    asm_code.append("\n// End initialization")
    asm_code.append("@END_INIT")
    asm_code.append("0;JMP")
    asm_code.append("(END_INIT)")

    return "\n".join(asm_code)

def create_matmul_with_init():
    """Create complete MatMul program with initialization"""
    init_code = create_matmul_init()

    with open("MatMul.asm", "r") as f:
        matmul_code = f.read()

    # Combine initialization with matrix multiplication
    full_program = init_code + "\n\n" + matmul_code

    with open("MatMul_Full.asm", "w") as f:
        f.write(full_program)

    print("Created MatMul_Full.asm with matrix initialization")

if __name__ == "__main__":
    create_matmul_with_init()
```

### Step 2: Create the Matrix Multiplication Algorithm

Create a new assembly file (e.g., `MatMul8x8.asm`) or modify [MatMul.asm](MatMul.asm). Here's a template for N×N matrices:

```assembly
// N×N MATRIX MULTIPLICATION
// A: RAM[BASE_A..BASE_A + N*N - 1]
// B: RAM[BASE_B..BASE_B + N*N - 1]
// C: RAM[BASE_C..BASE_C + N*N - 1]

// For 8×8 matrices:
// A: RAM[16..79]   (64 elements)
// B: RAM[80..143]  (64 elements)
// C: RAM[144..207] (64 elements)

// Constants
@8
D=A
@SIZE
M=D     // Store N=8

@16
D=A
@BASE_A
M=D     // Base address of matrix A

@80
D=A
@BASE_B
M=D     // Base address of matrix B

@144
D=A
@BASE_C
M=D     // Base address of matrix C

// i = 0
@i
M=0

(LOOP_i)
@i
D=M
@SIZE
D=D-M   // i - N
@END_ALL
D;JGE   // if i >= N, end

// j = 0
@j
M=0

(LOOP_j)
@j
D=M
@SIZE
D=D-M   // j - N
@END_j
D;JGE   // if j >= N, end j-loop

// sum = 0
@sum
M=0

// k = 0
@k
M=0

(LOOP_k)
@k
D=M
@SIZE
D=D-M   // k - N
@END_k
D;JGE   // if k >= N, break

// Calculate address: BASE_A + (i * N) + k
@i
D=M
@SIZE
D=D*M   // i * N (requires multiplication - use repeated addition)
@k
D=D+M   // (i * N) + k
@BASE_A
D=D+M   // BASE_A + (i * N) + k
A=D
D=M
@A_val
M=D     // Store A[i][k]

// Calculate address: BASE_B + (k * N) + j
@k
D=M
@SIZE
D=D*M   // k * N (requires multiplication - use repeated addition)
@j
D=D+M   // (k * N) + j
@BASE_B
D=D+M   // BASE_B + (k * N) + j
A=D
D=M
@B_val
M=D     // Store B[k][j]

// Multiply A_val * B_val (repeated addition)
@product
M=0
@A_val
D=M
@mult_count
M=D

(LOOP_mult)
@mult_count
D=M
@AFTER_mult
D;JEQ   // if count == 0, done

@product
D=M
@B_val
D=D+M
@product
M=D     // product += B_val

@mult_count
M=M-1

@LOOP_mult
0;JMP

(AFTER_mult)
// sum += product
@sum
D=M
@product
D=D+M
@sum
M=D

// k++
@k
M=M+1
@LOOP_k
0;JMP

(END_k)
// Store result: BASE_C + (i * N) + j
@i
D=M
@SIZE
D=D*M   // i * N
@j
D=D+M   // (i * N) + j
@BASE_C
D=D+M   // BASE_C + (i * N) + j
@addr_C
M=D

@sum
D=M
@addr_C
A=M
M=D     // Store C[i][j]

// j++
@j
M=M+1
@LOOP_j
0;JMP

(END_j)
// i++
@i
M=M+1
@LOOP_i
0;JMP

(END_ALL)
@HALT
0;JMP

(HALT)
@HALT
0;JMP
```

**Note**: The Hack assembly language doesn't have a built-in multiplication instruction. You need to implement multiplication using repeated addition (as shown in [MatMul.asm:102-123](MatMul.asm#L102-L123)).

### Step 3: Memory Allocation Guidelines

When creating larger matrices, ensure proper memory spacing:

| Matrix Size | Elements | Memory Required | Recommended Layout |
|------------|----------|-----------------|-------------------|
| 2×2 | 4 | 12 locations | A:[16-19], B:[20-23], C:[24-27] |
| 4×4 | 16 | 48 locations | A:[16-31], B:[32-47], C:[48-63] |
| 8×8 | 64 | 192 locations | A:[16-79], B:[80-143], C:[144-207] |
| 16×16 | 256 | 768 locations | A:[16-271], B:[272-527], C:[528-783] |

**Important**: Reserve RAM[65+] for loop variables and temporary storage.

---

## Running Benchmarks

### Method 1: Single Test

Run a specific .hack file:

```bash
python3 benchmark.py MatMul_Full.hack
```

### Method 2: Batch Testing

Run all .hack files in the current directory:

```bash
python3 benchmark.py
```

### Method 3: Custom Workflow

For a complete custom matrix size test:

```bash
# 1. Modify init_matmul.py for your matrix size
# 2. Generate initialization code
python3 init_matmul.py

# 3. Assemble to machine code
python3 assembler.py MatMul_Full.asm

# 4. Run benchmark
python3 benchmark.py MatMul_Full.hack
```

---

## Understanding Results

The benchmark output shows:

```
======================================================================
Benchmarking: MatMul_Full.hack
======================================================================

Running Standard Hack CPU:
----------------------------------------------------------------------
Cycles: 12543
Execution Time: 0.234s
Result Matrix C:
  RAM[48]: 1
  RAM[49]: 2
  ...

Running NMC-Augmented Hack CPU:
----------------------------------------------------------------------
Cycles: 3421
Execution Time: 0.089s
Result Matrix C:
  RAM[48]: 1
  RAM[49]: 2
  ...
```

### Key Metrics

- **Cycles**: Number of CPU cycles executed
- **Execution Time**: Wall-clock time in seconds
- **Speedup**: Calculate as `Standard Cycles / NMC Cycles`
- **Result Matrix**: Verify correctness by checking output values

### Expected Performance

Performance characteristics vary with matrix size:

| Matrix Size | Standard Cycles (approx) | Expected Speedup |
|------------|-------------------------|------------------|
| 2×2 | ~800 | 2-4× |
| 4×4 | ~12,000 | 3-8× |
| 8×8 | ~100,000 | 5-15× |
| 16×16 | ~1,600,000 | 10-30× |

---

## Troubleshooting

### Issue: "File not found"

**Solution**: Ensure you've run the assembler first:
```bash
python3 assembler.py MatMul_Full.asm
```

### Issue: Incorrect results

**Possible causes**:
1. Memory overlap - Check base addresses don't conflict
2. Matrix size mismatch - Verify loop bounds match initialization
3. Arithmetic overflow - Use smaller test values

**Solution**: Use identity matrix for Matrix A to easily verify results (C should equal B).

### Issue: Timeout errors

**Cause**: Large matrices may exceed the 30-second timeout.

**Solution**: Modify [benchmark.py:23](benchmark.py#L23) and [benchmark.py:44](benchmark.py#L44):
```python
timeout=300  # Increase to 5 minutes for large matrices
```

### Issue: Out of memory

**Cause**: Matrix size exceeds available RAM.

**Solution**: The Hack computer has 32K RAM locations (0-32767). For large matrices:
- Maximum practical size: ~90×90 (uses ~24,000 locations)
- Reserve addresses 24576+ for I/O (keyboard, screen)

### Issue: Assembly errors

**Common errors**:
- Undefined labels - Check loop label names match jumps
- Invalid mnemonics - Refer to Hack instruction set
- Symbol conflicts - Avoid reusing predefined symbols (R0-R15, SP, etc.)

**Solution**: Review [assembler.py:13-34](assembler.py#L13-L34) for valid instruction formats.

---

## Example: 2×2 Matrix Benchmark

Here's a complete example for benchmarking 2×2 matrices:

### Step 1: Create MatMul2x2.asm

```assembly
// 2×2 MATRIX MULTIPLICATION
// A: RAM[16..19]
// B: RAM[20..23]
// C: RAM[24..27]

// Initialize Matrix A (identity)
@1
D=A
@16
M=D  // A[0][0] = 1

@0
D=A
@17
M=D  // A[0][1] = 0

@0
D=A
@18
M=D  // A[1][0] = 0

@1
D=A
@19
M=D  // A[1][1] = 1

// Initialize Matrix B
@1
D=A
@20
M=D  // B[0][0] = 1

@2
D=A
@21
M=D  // B[0][1] = 2

@3
D=A
@22
M=D  // B[1][0] = 3

@4
D=A
@23
M=D  // B[1][1] = 4

// Matrix multiplication (i, j, k loops for N=2)
// C[i][j] = sum(A[i][k] * B[k][j]) for k=0..1

// [Add multiplication logic here following the N×N template above]

@HALT
0;JMP
(HALT)
@HALT
0;JMP
```

### Step 2: Assemble and Run

```bash
python3 assembler.py MatMul2x2.asm
python3 benchmark.py MatMul2x2.hack
```

### Expected Result

For identity matrix A and test matrix B:
```
C = A × B = B
C = [[1, 2],
     [3, 4]]
```

---

## Tips for Large Matrix Benchmarks

1. **Start Small**: Test with 2×2 or 4×4 first to verify correctness
2. **Use Identity Matrices**: Makes result verification trivial (C = B)
3. **Monitor Memory**: Track variable allocation to avoid conflicts
4. **Incremental Testing**: Test initialization and multiplication separately
5. **Performance Scaling**: Expect O(N³) complexity for N×N matrices

---

## Additional Resources

- Hack Assembly Language Specification
- NMC Architecture Documentation
- CPU Simulator Implementation Details

---

## Contributing

When creating benchmarks for new matrix sizes, please:
1. Document memory layout clearly
2. Verify results with known test cases
3. Report performance metrics
4. Share assembly optimizations

---

**Last Updated**: 2025-12-23
