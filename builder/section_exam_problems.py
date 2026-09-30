# builder/section_exam_problems.py

def get_exam_problems():
    return '''# PART 4: Master University Examination & Numerical Problem Compendium

---

### Purpose and Pedagogy of this Problem Compendium
In Rashtrasant Tukadoji Maharaj Nagpur University (RTMNU) and affiliated engineering university examinations for **Digital Electronics Circuits (BEL5T16C)**, the 70-mark university paper rigorously balances theoretical derivations with numerical circuit synthesis. 

This section presents step-by-step, fully worked solutions to the most challenging, frequently recurring examination problems across all 5 units. Every problem is solved following the engineering standard:
1. **Given Data & Parameter Identification**
2. **First-Principles Governing Formula / Truth Table**
3. **Step-by-Step Algebraic / Circuit Derivation**
4. **Physical Sanity Check & Verification**

---

## UNIT I: Solved Numerical & Design Problems

### Problem 1.1: Signed 2's Complement Arithmetic & Hardware Overflow Detection
**Question:** Perform the following arithmetic operations using 8-bit 2's complement representation. In each case, determine whether an arithmetic overflow has occurred and explain the physical hardware condition used by the ALU to detect it:
1. $(+75)_{10} + (+68)_{10}$
2. $(-42)_{10} + (-95)_{10}$
3. $(+95)_{10} - (+42)_{10}$

#### Solution:
##### Step 1: Bit Budget and Representation
An 8-bit signed register stores numbers in the range:
$$\\text{Range} = \\left[-2^7, \\; +2^7 - 1\\right] = [-128, \\; +127]$$

- Convert absolute magnitudes to 8-bit binary:
  - $75_{10} = 64 + 8 + 2 + 1 = 01001011_2$
  - $68_{10} = 64 + 4 = 01000100_2$
  - $42_{10} = 32 + 8 + 2 = 00101010_2$
  - $95_{10} = 64 + 16 + 8 + 4 + 2 + 1 = 01011111_2$

- Form negative numbers using 2's complement (invert all bits and add 1):
  - $(-42)_{10}$: Invert $00101010 \\to 11010101$, add $1 \\to \\mathbf{11010110_2}$
  - $(-95)_{10}$: Invert $01011111 \\to 10100000$, add $1 \\to \\mathbf{10100001_2}$

---

##### Part 1: $(+75)_{10} + (+68)_{10}$
```
   Carry in:      1 0 0 0 0 0 0 0
   (+75):         0 1 0 0 1 0 1 1
   (+68):       + 0 1 0 0 0 1 0 0
   ---------------------------------
   Sum:           1 0 0 0 1 1 1 1   (Bit 7 = 1, meaning NEGATIVE!)
```
- **Overflow Analysis:**
  - Expected decimal sum: $+75 + 68 = +143_{10}$.
  - But the maximum positive value an 8-bit register can hold is $+127_{10}$!
  - We added two positive operands (Sign bits both $0$) and received a negative result (Sign bit $1$).
  - **Hardware Rule Check:** In the ALU, carry into the sign bit ($C_7 = 1$) is XORed with carry out of the sign bit ($C_8 = 0$):
    $$V = C_7 \\oplus C_8 = 1 \\oplus 0 = \\mathbf{1} \\implies \\text{OVERFLOW DETECTED!}$$
  - The bit pattern `10001111` in 2's complement evaluates to $-(01110000 + 1) = -113_{10}$, which is mathematically erroneous due to register overflow.

---

##### Part 2: $(-42)_{10} + (-95)_{10}$
```
   Carry in:    1 0 0 0 0 0 0 0 0
   (-42):         1 1 0 1 0 1 1 0
   (-95):       + 1 0 1 0 0 0 0 1
   ---------------------------------
   Sum:         1 0 1 1 1 0 1 1 1   (Carry out C8 = 1 is discarded in 2's comp)
```
- **Overflow Analysis:**
  - Expected decimal sum: $-42 + (-95) = -137_{10}$.
  - The minimum negative value an 8-bit register can hold is $-128_{10}$!
  - We added two negative numbers (Sign bits both $1$) and produced a positive result ($01110111_2 = +119_{10}$)!
  - **Hardware Rule Check:** Carry into sign bit $C_7 = 0$, carry out $C_8 = 1$:
    $$V = C_7 \\oplus C_8 = 0 \\oplus 1 = \\mathbf{1} \\implies \\text{OVERFLOW DETECTED!}$$

---

##### Part 3: $(+95)_{10} - (+42)_{10} = (+95)_{10} + (-42)_{10}$
```
   Carry in:    1 1 1 0 1 1 0 0 0
   (+95):         0 1 0 1 1 1 1 1
   (-42):       + 1 1 0 1 0 1 1 0
   ---------------------------------
   Sum:         1 0 0 1 1 0 1 0 1   (Carry out C8 = 1 discarded)
```
- Discard end carry $C_8 = 1$. The 8-bit result is `00110101`.
- Convert to decimal: $32 + 16 + 4 + 1 = +53_{10}$.
- Expected: $95 - 42 = +53_{10}$.
- **Hardware Rule Check:** $C_7 = 1, C_8 = 1 \\implies V = 1 \\oplus 1 = \\mathbf{0}$ (No overflow). Result is exact.

---

### Problem 1.2: DC Noise Margin and Interfacing Pull-Up Resistor Calculation
**Question:** A standard TTL gate (7400 series) with parameters:
$$V_{OH(\\min)} = 2.4\\text{ V}, \\quad V_{OL(\\max)} = 0.4\\text{ V}, \\quad V_{IH(\\min)} = 2.0\\text{ V}, \\quad V_{IL(\\max)} = 0.8\\text{ V}$$
$$I_{OH(\\max)} = -400\\;\\mu\\text{A}, \\quad I_{OL(\\max)} = 16\\text{ mA}, \\quad I_{IH(\\max)} = 40\\;\\mu\\text{A}, \\quad I_{IL(\\max)} = -1.6\\text{ mA}$$
is used to drive a high-speed CMOS gate ($74\\text{HC}$ series powered at $V_{DD} = 5.0\\text{ V}$) having:
$$V_{IH(\\min)} = 3.5\\text{ V}, \\quad V_{IL(\\max)} = 1.0\\text{ V}, \\quad I_{in} \\approx \\pm 1\\;\\mu\\text{A}$$
1. Show why direct interfacing fails in the HIGH state.
2. Calculate the allowable range ($R_{p(\\min)}$ to $R_{p(\\max)}$) for an external pull-up resistor connected from the TTL output to $+5\\text{ V}$.

#### Solution:
##### Step 1: Why Direct Connection Fails
- Look at the LOW state:
  $$V_{OL(\\max)} = 0.4\\text{ V} < V_{IL(\\max,\\text{ CMOS})} = 1.0\\text{ V}$$
  $NM_L = 1.0\\text{ V} - 0.4\\text{ V} = +0.6\\text{ V}$. The LOW state communicates safely.
- Look at the HIGH state:
  $$V_{OH(\\min,\\text{ TTL})} = 2.4\\text{ V} < V_{IH(\\min,\\text{ CMOS})} = 3.5\\text{ V}$$
  $$NM_H = 2.4\\text{ V} - 3.5\\text{ V} = -1.1\\text{ V} \\quad (\\mathbf{\\text{NEGATIVE NOISE MARGIN!}})$$
  The CMOS gate will see $2.4\\text{ V}$ as an indeterminate voltage in the forbidden threshold region, causing severe oscillations or intermediate conduction where both PMOS and NMOS conduct simultaneously, overheating the chip! Direct connection is impossible.

---

##### Step 2: Calculation of Maximum Pull-Up Resistance ($R_{p(\\max)}$)
When the TTL output is in the HIGH state, the pull-up resistor must supply the leakage currents while maintaining the node voltage above $V_{IH(\\min,\\text{ CMOS})} = 3.5\\text{ V}$:
$$V_{CC} - I_{\\text{total leakage}} \\cdot R_p \\ge V_{IH(\\min)}$$
The leakage current is the sum of TTL reverse leakage ($I_{OH} \\approx 100\\;\\mu\\text{A}$) and CMOS input leakage ($1\\;\\mu\\text{A}$):
$$I_{\\text{leakage}} \\approx 100\\;\\mu\\text{A} + 1\\;\\mu\\text{A} = 101\\;\\mu\\text{A}$$
$$R_{p(\\max)} = \\frac{V_{CC} - V_{IH(\\min)}}{I_{\\text{leakage}}} = \\frac{5.0\\text{ V} - 3.5\\text{ V}}{101 \\times 10^{-6}\\text{ A}} = \\frac{1.5\\text{ V}}{101\\;\\mu\\text{A}} \\approx \\mathbf{14.85\\text{ k}\\Omega}$$

---

##### Step 3: Calculation of Minimum Pull-Up Resistance ($R_{p(\\min)}$)
When the TTL output transitions to the LOW state, its lower pull-down transistor ($Q_1$) turns ON and sinks current from the pull-up resistor to ground. To prevent the LOW voltage from rising above $V_{OL(\\max)} = 0.4\\text{ V}$, the current sinking capacity ($I_{OL(\\max)} = 16\\text{ mA}$) must not be exceeded:
$$I_{\\text{sink}} = \\frac{V_{CC} - V_{OL(\\max)}}{R_p} + N \\cdot |I_{IL}| \\le I_{OL(\\max)}$$
For a single CMOS load, $|I_{IL}| \\approx 0$:
$$R_{p(\\min)} = \\frac{V_{CC} - V_{OL(\\max)}}{I_{OL(\\max)}} = \\frac{5.0\\text{ V} - 0.4\\text{ V}}{16\\text{ mA}} = \\frac{4.6\\text{ V}}{0.016\\text{ A}} = \\mathbf{287.5\\;\\Omega}$$

##### Engineering Conclusion:
Any standard resistor between **$1\\text{ k}\\Omega$ and $10\\text{ k}\\Omega$** (typically **$2.2\\text{ k}\\Omega$ or $3.3\\text{ k}\\Omega$**) guarantees safe, fast, and robust TTL-to-CMOS interfacing.

---

## UNIT II: Solved Boolean Minimization & K-Map Problems

### Problem 2.1: 4-Variable K-Map Minimization with Don't Cares
**Question:** Minimize the following 4-variable Boolean logic function in both Sum-of-Products (SOP) and Product-of-Sums (POS) standard forms. Explicitly identify all Prime Implicants (PI) and Essential Prime Implicants (EPI):
$$f(A, B, C, D) = \\sum m(1, 3, 7, 11, 15) + \\sum d(0, 2, 5)$$

#### Solution:
##### Step 1: Populate the 4-Variable Karnaugh Map
The map coordinates follow Gray code sequence ($00, 01, 11, 10$):

```
       CD
AB     00   01   11   10
00   ┌────┬────┬────┬────┐
     │ X0 │ 11 │ 13 │ X2 │
     ├────┼────┼────┼────┤
01   │  4 │ X5 │ 17 │  6 │
     ├────┼────┼────┼────┤
11   │ 12 │ 13 │ 115│ 14 │
     ├────┼────┼────┼────┤
10   │  8 │  9 │ 111│ 10 │
     └────┴────┴────┴────┘
```
- Cell 1, 3, 7, 11, 15 contain `1`.
- Cell 0, 2, 5 contain `X` (Don't Care).
- All remaining cells (4, 6, 8, 9, 10, 12, 13, 14) contain `0`.

---

##### Step 2: Form Optimal SOP Groupings (Powers of 2: 8, 4, 2)
1. **Octet Exploration:** Look at the four corners and edges. Can we form an 8-group? No.
2. **Quad 1 (The Entire Column $CD = 11$):**  
   Cells $(3, 7, 15, 11)$ all contain `1`!  
   This vertical column spans all four rows ($AB = 00, 01, 11, 10$).  
   Variables $A$ and $B$ eliminate completely.  
   **Term 1 = $C D$**
3. **Quad 2 (Row 00):**  
   Look at row $AB = 00$: cells are $(0, 1, 3, 2)$ having values $(X, 1, 1, X)$.  
   By treating the don't cares at cells $0$ and $2$ as `1`s, we form a 4-cell group!  
   In this row, $A=0$ and $B=0$. Variables $C$ and $D$ span all combinations and eliminate.  
   **Term 2 = $\\overline{A} \\, \\overline{B}$**
4. **Coverage Check:**  
   - Cell 1 is covered by Quad 2.
   - Cell 3 is covered by both Quad 1 and Quad 2.
   - Cells 7, 11, 15 are covered by Quad 1.
   - All specified minterms (`1, 3, 7, 11, 15`) are 100% covered!
   - What about cell 5 ($X$)? We leave it as `0` because grouping it would require an extra redundant gate.

##### Prime Implicant Inventory:
- **Prime Implicants (PI):** $C D$, $\\overline{A} \\, \\overline{B}$, $\\overline{A} D$ (cells $1, 3, 5, 7$).
- **Essential Prime Implicants (EPI):**
  - $C D$ is essential because minterms $7, 11, 15$ are covered by no other prime implicant.
  - $\\overline{A} \\, \\overline{B}$ is essential because minterm $1$ is covered only by it (if we choose the minimal 2-term cover).
- **Minimal SOP Equation:**
  $$\\mathbf{f(A, B, C, D) = \\overline{A} \\, \\overline{B} + C D}$$

---

##### Step 3: Minimal POS Minimization (Grouping the `0`s)
The `0` cells are: $4, 6, 8, 9, 10, 12, 13, 14$.
We group the zeros together with don't cares ($X$):
1. **Quad of 0s at left column ($CD = 00$):** Cells $(4, 12)$ with $(0, X)$? No, cell 0 is X.  
   Let's group cells $(4, 6, 12, 14)$: In these cells, $B=1$ and $D=0$.  
   Complement: $(B + \\overline{D})$.
2. **Quad of 0s at row 10 and 11 ($AB = 10, 11 \\implies A=1$):**  
   Cells $(8, 9, 12, 13)$: $A=1$ and $C=0$.  
   Complement: $(\\overline{A} + C)$.
3. **Minimal POS Equation:**
   $$\\mathbf{f(A, B, C, D) = (\\overline{A} + C)(B + \\overline{D})}$$
   *(Both forms require only two 2-input gates plus an output gate, representing an 85% hardware reduction from the unsimplified 5-AND SOP expression!)*

---

## UNIT III: Solved Combinational Logic Synthesis Problems

### Problem 3.1: Full Adder Implementation Using Only 4-to-1 Multiplexers
**Question:** Design and realize a Full Adder (Outputs: Sum $S$ and Carry $C_{out}$) using **only two 4-to-1 Multiplexers** (such as the dual 74153 IC) and no external logic gates. Inputs are $A, B, C_{in}$.

#### Solution:
##### Step 1: Full Adder Truth Table
| $A$ | $B$ | $C_{in}$ | Sum ($S$) | $C_{out}$ |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

---

##### Step 2: Multiplexer Input Assignment
A 4-to-1 MUX has two select inputs ($S_1, S_0$) and four data inputs ($I_0, I_1, I_2, I_3$).
- We assign variables $A$ and $B$ to the select lines:
  $$S_1 = A, \\quad S_0 = B$$
- The remaining input variable $C_{in}$ (and its complement $\\overline{C_{in}}$, 0, or 1) will be connected directly to the data inputs $I_0, I_1, I_2, I_3$.

---

##### Step 3: Deriving Data Inputs for MUX 1 (Sum $S$)
- When $A B = 00$:
  - If $C_{in} = 0 \\implies S = 0$
  - If $C_{in} = 1 \\implies S = 1$
  - Therefore: $\\mathbf{I_0 = C_{in}}$
- When $A B = 01$:
  - If $C_{in} = 0 \\implies S = 1$
  - If $C_{in} = 1 \\implies S = 0$
  - Therefore: $\\mathbf{I_1 = \\overline{C_{in}}}$
- When $A B = 10$:
  - If $C_{in} = 0 \\implies S = 1$
  - If $C_{in} = 1 \\implies S = 0$
  - Therefore: $\\mathbf{I_2 = \\overline{C_{in}}}$
- When $A B = 11$:
  - If $C_{in} = 0 \\implies S = 0$
  - If $C_{in} = 1 \\implies S = 1$
  - Therefore: $\\mathbf{I_3 = C_{in}}$

---

##### Step 4: Deriving Data Inputs for MUX 2 (Carry $C_{out}$)
- When $A B = 00$:
  - For both $C_{in} = 0$ and $C_{in} = 1$, $C_{out} = 0$.
  - Therefore: $\\mathbf{I_0 = 0}$ (tied to Ground)
- When $A B = 01$:
  - If $C_{in} = 0 \\implies C_{out} = 0$
  - If $C_{in} = 1 \\implies C_{out} = 1$
  - Therefore: $\\mathbf{I_1 = C_{in}}$
- When $A B = 10$:
  - If $C_{in} = 0 \\implies C_{out} = 0$
  - If $C_{in} = 1 \\implies C_{out} = 1$
  - Therefore: $\\mathbf{I_2 = C_{in}}$
- When $A B = 11$:
  - For both $C_{in} = 0$ and $C_{in} = 1$, $C_{out} = 1$.
  - Therefore: $\\mathbf{I_3 = 1}$ (tied to $V_{CC}$)

##### Synthesis Summary:
Both functions are realized using a single dual 4-to-1 MUX IC (74153) with zero external gates:
- **MUX 1 (Sum):** $S_1 = A, S_0 = B$, Inputs: $(I_0 = C_{in}, I_1 = \\overline{C_{in}}, I_2 = \\overline{C_{in}}, I_3 = C_{in})$.
- **MUX 2 (Carry):** $S_1 = A, S_0 = B$, Inputs: $(I_0 = 0, I_1 = C_{in}, I_2 = C_{in}, I_3 = 1)$.

---

## UNIT IV: Solved Sequential Circuit Conversion & Counter Design Problems

### Problem 4.1: Systematic Conversion of an SR Flip-Flop to a JK Flip-Flop
**Question:** Design the combinational conversion logic required to convert an available **SR Flip-Flop** into a functional **JK Flip-Flop**.

#### Solution:
##### Step 1: Master Conversion Table
We list the desired inputs ($J, K$), present state ($Q_n$), next state ($Q_{n+1}$), and the required SR excitation values from the SR excitation table:

| $J$ | $K$ | $Q_n$ | Desired $Q_{n+1}$ | Required $S$ | Required $R$ |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | **0** | **$\\times$** |
| 0 | 0 | 1 | 1 | **$\\times$** | **0** |
| 0 | 1 | 0 | 0 | **0** | **$\\times$** |
| 0 | 1 | 1 | 0 | **0** | **1** |
| 1 | 0 | 0 | 1 | **1** | **0** |
| 1 | 0 | 1 | 1 | **$\\times$** | **0** |
| 1 | 1 | 0 | 1 | **1** | **0** |
| 1 | 1 | 1 | 0 | **0** | **1** |

---

##### Step 2: K-Map Minimization for $S$ Input
Inputs to K-map are $J, K, Q_n$:

```
      KQn
J     00   01   11   10
0   ┌────┬────┬────┬────┐
    │  0 │  X │  0 │  0 │
    ├────┼────┼────┼────┤
1   │  1 │  X │  0 │  1 │
    └────┴────┴────┴────┘
```
- Grouping cells $(4, 6)$ [where $J=1$ and $Q_n=0$]:
  $$\\mathbf{S = J \\, \\overline{Q_n}}$$

---

##### Step 3: K-Map Minimization for $R$ Input

```
      KQn
J     00   01   11   10
0   ┌────┬────┬────┬────┐
    │  X │  0 │  1 │  X │
    ├────┼────┼────┼────┤
1   │  0 │  0 │  1 │  0 │
    └────┴────┴────┴────┘
```
- Grouping cells $(3, 7)$ [where $K=1$ and $Q_n=1$]:
  $$\\mathbf{R = K \\, Q_n}$$

##### Hardware Reality Check:
Feed input $J$ into a 2-input AND gate with the complement output $\\overline{Q}$, and connect its output to pin $S$. Feed input $K$ into a 2-input AND gate with output $Q$, and connect its output to pin $R$.  
*Notice what this did physically:* When $J=K=1$ and $Q=1$, $R$ receives $1$ and $S$ receives $0$, forcing the flip-flop to RESET to $0$ on the clock edge. When $Q=0$, $S$ receives $1$ and $R$ receives $0$, forcing it to SET to $1$. The forbidden condition ($S=R=1$) is physically impossible because $Q$ and $\\overline{Q}$ can never be $1$ simultaneously!

---

## UNIT V: Solved Converter & Memory Architecture Problems

### Problem 5.1: 8-Bit R-2R Ladder DAC Performance & Resolution
**Question:** An 8-bit R-2R ladder Digital-to-Analog Converter is powered with an analog reference voltage $V_{ref} = +10.0\\text{ V}$.
1. Calculate the resolution (step size $\\Delta V$) in millivolts.
2. Determine the analog output voltage for a digital input code of $10100110_2$.
3. Calculate the full-scale output voltage ($V_{FS}$).

#### Solution:
##### Step 1: Resolution (Step Size)
An 8-bit DAC has $n=8$ bits, giving $2^8 - 1 = 255$ discrete conversion intervals:
$$\\Delta V = \\frac{V_{ref}}{2^n - 1} = \\frac{10.0\\text{ V}}{255} = 0.039215\\text{ V} = \\mathbf{39.22\\text{ mV per step}}$$
*(Note: In binary weighted converters referenced to an unscaled op-amp buffer, step size is often formulated as $V_{ref}/2^n = 10.0/256 = 39.06\\text{ mV}$. Both conventions are accepted in university evaluation when explicitly stated).*

---

##### Step 2: Output Voltage for Digital Code `10100110`
Convert binary code to decimal:
$$D = (1 \\times 128) + (0 \\times 64) + (1 \\times 32) + (0 \\times 16) + (0 \\times 8) + (1 \\times 4) + (1 \\times 2) + (0 \\times 1)$$
$$D = 128 + 32 + 4 + 2 = 166_{10}$$
The analog output voltage is:
$$V_{out} = D \\times \\Delta V = 166 \\times 39.215\\text{ mV} = \\mathbf{6.510\\text{ V}}$$

Alternatively, evaluate via node current summation:
$$V_{out} = V_{ref} \\left(\\frac{1}{2} + \\frac{0}{4} + \\frac{1}{8} + \\frac{0}{16} + \\frac{0}{32} + \\frac{1}{64} + \\frac{1}{128} + \\frac{0}{256}\\right)$$
$$V_{out} = 10.0 \\left(0.5 + 0.125 + 0.015625 + 0.0078125\\right) = 10.0 \\times 0.6484375 = \\mathbf{6.484\\text{ V}}$$

---

##### Step 3: Full-Scale Output Voltage ($V_{FS}$)
When all input bits are $1$ (`11111111` $= 255_{10}$):
$$V_{FS} = \\frac{255}{256} \\times 10.0\\text{ V} = \\mathbf{9.961\\text{ V}}$$
Notice that the full-scale analog output never reaches $10.0\\text{ V}$ exactly—it is always exactly **$1\\text{ LSB}$ less than $V_{ref}$**!

---

### Problem 5.2: Memory System Expansion ($4\\text{K} \\times 8$ using $1\\text{K} \\times 4$ Chips)
**Question:** Design a complete memory module with a capacity of **$4\\text{K} \\times 8$ bits** using individual **$1\\text{K} \\times 4$ static RAM chips**. Show the address decoding circuit using a 2-to-4 line active-low decoder.

#### Solution:
##### Step 1: Calculate Required Chips
- Total memory capacity needed: $4\\text{K} \\times 8 = 4096 \\times 8 = 32,768\\text{ bits}$.
- Capacity per chip: $1\\text{K} \\times 4 = 1024 \\times 4 = 4,096\\text{ bits}$.
$$\\text{Total Chips Required} = \\frac{4\\text{K} \\times 8}{1\\text{K} \\times 4} = 4 \\times 2 = \\mathbf{8\\text{ chips}}$$

---

##### Step 2: Address and Data Bus Architecture
- **Total Address Lines Needed:**
  $$4\\text{K} = 4096 = 2^{12} \\implies \\mathbf{12\\text{ Address Lines } (A_{11} \\text{ to } A_0)}$$
- **Total Data Lines Needed:**
  $$8\\text{ bits} \\implies \\mathbf{8\\text{ Data Lines } (D_7 \\text{ to } D_0)}$$
- **Address Lines for Individual Chips:**
  $$1\\text{K} = 1024 = 2^{10} \\implies \\mathbf{10\\text{ Address Lines } (A_9 \\text{ to } A_0)}$$
  The lower 10 address lines ($A_0$ through $A_9$) connect directly to all 8 memory chips in parallel.
- **Address Lines for Chip Selection:**
  The upper 2 address lines ($A_{11}, A_{10}$) determine which pair of chips is activated:
  $$2^2 = 4\\text{ banks of memory}$$

---

##### Step 3: Chip Bank Arrangement
We arrange the 8 chips into **4 banks**, with each bank containing **2 chips** wired in parallel to provide the full 8-bit word width:
- **Bank 0 (Addresses 000H to 3FFH):**
  - Chip 1 provides Data bits $D_0 - D_3$.
  - Chip 2 provides Data bits $D_4 - D_7$.
  - Enabled by Decoder Output $\\overline{Y_0}$ ($A_{11}A_{10} = 00$).
- **Bank 1 (Addresses 400H to 7FFH):**
  - Chip 3 provides Data bits $D_0 - D_3$.
  - Chip 4 provides Data bits $D_4 - D_7$.
  - Enabled by Decoder Output $\\overline{Y_1}$ ($A_{11}A_{10} = 01$).
- **Bank 2 (Addresses 800H to BFFH):**
  - Chip 5 provides Data bits $D_0 - D_3$.
  - Chip 6 provides Data bits $D_4 - D_7$.
  - Enabled by Decoder Output $\\overline{Y_2}$ ($A_{11}A_{10} = 10$).
- **Bank 3 (Addresses C00H to FFFH):**
  - Chip 7 provides Data bits $D_0 - D_3$.
  - Chip 8 provides Data bits $D_4 - D_7$.
  - Enabled by Decoder Output $\\overline{Y_3}$ ($A_{11}A_{10} = 11$).

---

##### Step 4: Address Decoder Connection
A 2-to-4 line active-low decoder (such as half of a 74LS139) is connected as follows:
- Decoder Select Input $A = A_{10}$
- Decoder Select Input $B = A_{11}$
- Decoder Enable $\\overline{G}$ tied to Ground (permanently enabled).
- Decoder output $\\overline{Y_0}$ connects to Chip Select $\\overline{CS}$ of Chips 1 and 2.
- Decoder output $\\overline{Y_1}$ connects to Chip Select $\\overline{CS}$ of Chips 3 and 4.
- Decoder output $\\overline{Y_2}$ connects to Chip Select $\\overline{CS}$ of Chips 5 and 6.
- Decoder output $\\overline{Y_3}$ connects to Chip Select $\\overline{CS}$ of Chips 7 and 8.
- The master Write Enable line ($\\overline{WE}$) connects to pin $\\overline{WE}$ of all 8 chips simultaneously.

*This concludes the complete hardware architecture for the $4\\text{K} \\times 8$ memory system.*

---
'''

if __name__ == '__main__':
    print(get_exam_problems()[:300])
