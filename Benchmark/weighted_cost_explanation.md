# Understanding Weighted Cost in NMC Architecture

## What is Weighted Cost?

**Weighted cost** is a model that assigns a **relative cycle cost** to each instruction type based on how much work the hardware actually does — specifically, how many times data crosses the CPU-Memory bus.

In the traditional architecture, every bus crossing adds latency and energy cost. Our model assigns:
- **1.0 cycle** = baseline (one full instruction with typical memory access)
- **< 1.0 cycle** = NMC optimization reduces the effective cost

---

## The Hack CPU Registers

Before understanding the instructions, you need to know the three key storage locations:

| Register | Name | Purpose |
|----------|------|---------|
| **D** | Data Register | General-purpose register inside the CPU for holding values during computation |
| **A** | Address Register | Holds either a memory address OR a constant value |
| **M** | Memory | The RAM location pointed to by A — so M means "the value stored at RAM[A]" |

**Example:** If A = 100, then M refers to RAM[100].

---

## Instruction Types and Their Costs

### Comparison Table

| Instruction Type | Example | Traditional CPU | NMC-Augmented CPU | Speedup |
|------------------|---------|-----------------|-------------------|---------|
| Register-only | D=D+A | 1.0 cycle | 1.0 cycle | 1.0x |
| Memory read | D=M | 1.0 cycle | 0.7 cycles | 1.43x |
| Memory write | M=D | 1.0 cycle | 0.7 cycles | 1.43x |
| Compute-and-store | M=D+M | 1.0 cycle | **0.5 cycles** | **2.0x** |

---

## Detailed Explanation of Each Instruction Type

### 1. Register-only (D=D+A) — Cost: 1.0 on both

**What it does:** Adds the value in register D to the value in register A, stores result in D.

**Why same cost?** Both D and A are inside the CPU. No memory access is needed, so no bus crossing occurs. NMC provides no advantage here.

```
┌─────────────────┐
│      CPU        │
│  D ──┬──► ALU   │
│  A ──┘    │     │
│           ▼     │
│      D (result) │
└─────────────────┘
No memory involved — identical on both architectures
```

---

### 2. Memory read (D=M) — Cost: 1.0 traditional, 0.7 NMC

**What it does:** Reads the value from memory location M (i.e., RAM[A]) and stores it in register D.

**Traditional CPU:**
```
┌─────────┐              ┌─────────┐
│   CPU   │◄─── BUS ────►│ MEMORY  │
│         │   (crossing) │         │
│    D ◄──┼──────────────┼── M     │
└─────────┘              └─────────┘
1 bus crossing = 1.0 cycle
```

**NMC-Augmented CPU:**
```
┌─────────────────────────────────┐
│      INTEGRATED CHIP            │
│  ┌─────────┐    ┌─────────┐    │
│  │   ALU   │◄───│   RAM   │    │
│  │    D ◄──┼────┼── M     │    │
│  └─────────┘    └─────────┘    │
└─────────────────────────────────┘
Short internal path = 0.7 cycles (30% faster)
```

---

### 3. Memory write (M=D) — Cost: 1.0 traditional, 0.7 NMC

**What it does:** Writes the value from register D to memory location M (i.e., RAM[A]).

**Traditional CPU:**
```
┌─────────┐              ┌─────────┐
│   CPU   │◄─── BUS ────►│ MEMORY  │
│         │   (crossing) │         │
│    D ──►┼──────────────┼──► M    │
└─────────┘              └─────────┘
1 bus crossing = 1.0 cycle
```

**NMC-Augmented CPU:**
```
┌─────────────────────────────────┐
│      INTEGRATED CHIP            │
│  ┌─────────┐    ┌─────────┐    │
│  │   ALU   │───►│   RAM   │    │
│  │    D ──►┼────┼──► M    │    │
│  └─────────┘    └─────────┘    │
└─────────────────────────────────┘
Short internal path = 0.7 cycles (30% faster)
```

---

### 4. Compute-and-store (M=D+M) — Cost: 1.0 traditional, 0.5 NMC ⭐

**What it does:** Reads M, adds D to it, writes the result back to M. This is the **key optimization**.

**Traditional CPU:**
```
┌─────────┐              ┌─────────┐
│   CPU   │              │ MEMORY  │
│         │              │         │
│ (1) ────┼──► address ──┼──►      │
│         │              │         │
│ (2) ◄───┼── read M ◄───┼───      │  } 2 bus crossings!
│         │              │         │
│ (3) ALU computes D+M   │         │
│         │              │         │
│ (4) ────┼── write ────►┼──► M    │
└─────────┘              └─────────┘
2 bus crossings = 1.0 cycle (expensive)
```

**NMC-Augmented CPU:**
```
┌─────────────────────────────────┐
│      INTEGRATED CHIP            │
│  ┌─────────┐    ┌─────────┐    │
│  │   ALU   │◄──►│   RAM   │    │
│  │         │    │         │    │
│  │ (1) Read M directly    │    │
│  │ (2) Compute D+M        │    │
│  │ (3) Write back to M    │    │
│  └─────────┘    └─────────┘    │
└─────────────────────────────────┘
0 bus crossings = 0.5 cycles (50% faster!)
```

**Why this matters:** Matrix multiplication uses many M=D+M style operations (accumulating products into a sum). Each one is **twice as fast** on NMC.

---

## Summary: Why NMC Wins

| Factor | Traditional | NMC | Improvement |
|--------|-------------|-----|-------------|
| Bus crossings for M=D+M | 2 | 0 | Eliminated |
| Energy per memory op | High | Low | ~30-50% reduction |
| Compute-and-store cost | 1.0 | 0.5 | **2x faster** |

The **1.46x speedup** in our matrix multiplication benchmark comes from the accumulation of these savings across thousands of memory-intensive instructions.

---

## Key Takeaway

> **Traditional architecture:** Data must travel between CPU and Memory for every memory operation.
>
> **NMC architecture:** ALU sits next to RAM, so read-compute-write happens locally without bus crossings.
>
> **Result:** Same instructions, same results, but fewer cycles and less energy.