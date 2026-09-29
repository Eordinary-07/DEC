# builder/section_appendix.py

def get_appendix():
    return '''# APPENDIX & MASTER REFERENCE COMPENDIUM

---

## A. Master Mathematical & Operational Cheat Sheet

### 1. Number Systems & Binary Arithmetic (Unit I)
- **Radix Polynomial Expansion:**
  $$N_r = \\sum_{i=0}^{n-1} d_i \\cdot r^i + \\sum_{j=1}^{m} d_{-j} \\cdot r^{-j}$$
- **Radix-minus-one Complement ($r-1$'s complement):**
  $$(r-1)'s = (r^n - 1) - N$$
  For binary: invert every bit ($0 \\leftrightarrow 1$).
- **Radix Complement ($r$'s complement):**
  $$r's = r^n - N = \\left[(r-1)'s\\right] + 1$$
  For binary: take 1's complement and add 1.
- **Signed Range for $n$-bit integers:**
  $$\\text{Range}_{\\text{2's comp}} = \\left[-2^{n-1}, \\; +2^{n-1}-1\\right]$$
  For $n=8$: $[-128, \\; +127]$.

### 2. Logic Families & DC Noise Margins (Unit I)
- **High-state Noise Margin:**
  $$NM_H = V_{OH(\\min)} - V_{IH(\\min)}$$
- **Low-state Noise Margin:**
  $$NM_L = V_{IL(\\max)} - V_{OL(\\max)}$$
- **Fan-out:**
  $$\\text{Fan-out} = \\min\\left(\\frac{I_{OH(\\max)}}{I_{IH(\\max)}}, \\; \\frac{I_{OL(\\max)}}{I_{IL(\\max)}}\\right)$$
- **Dynamic Power Dissipation in CMOS:**
  $$P_{\\text{dynamic}} = C_L \\cdot V_{DD}^2 \\cdot f$$

### 3. Boolean Algebra & Minimization (Unit II)
- **De Morgan's Theorems:**
  $$\\overline{A + B} = \\overline{A} \\cdot \\overline{B}$$
  $$\\overline{A \\cdot B} = \\overline{A} + \\overline{B}$$
- **Absorption Laws:**
  $$A + A \\cdot B = A$$
  $$A \\cdot (A + B) = A$$
  $$A + \\overline{A} \\cdot B = A + B$$
- **Consensus Theorem:**
  $$A B + \\overline{A} C + B C = A B + \\overline{A} C$$

### 4. Arithmetic & Combinational Circuits (Unit III)
- **Half Adder:**
  $$S = A \\oplus B, \\quad C = A \\cdot B$$
- **Full Adder:**
  $$S = A \\oplus B \\oplus C_{in}, \\quad C_{out} = A B + B C_{in} + A C_{in}$$
- **Carry Lookahead Generator:**
  $$G_i = A_i B_i, \\quad P_i = A_i \\oplus B_i$$
  $$C_{i+1} = G_i + P_i C_i$$
  $$C_1 = G_0 + P_0 C_0$$
  $$C_2 = G_1 + P_1 G_0 + P_1 P_0 C_0$$
  $$C_3 = G_2 + P_2 G_1 + P_2 P_1 G_0 + P_2 P_1 P_0 C_0$$
  $$C_4 = G_3 + P_3 G_2 + P_3 P_2 G_1 + P_3 P_2 P_1 G_0 + P_3 P_2 P_1 P_0 C_0$$
- **Multiplexer Output Expansion:**
  $$Y = \\sum_{k=0}^{2^n-1} m_k \\cdot I_k$$

### 5. Sequential Logic & Flip-Flop Characteristic Equations (Unit IV)
- **SR Flip-Flop:**
  $$Q_{next} = S + \\overline{R} Q, \\quad \\text{with condition } S \\cdot R = 0$$
- **JK Flip-Flop:**
  $$Q_{next} = J \\overline{Q} + \\overline{K} Q$$
- **D Flip-Flop:**
  $$Q_{next} = D$$
- **T Flip-Flop:**
  $$Q_{next} = T \\oplus Q = T \\overline{Q} + \\overline{T} Q$$
- **Master Excitation Summary:**

| $Q_n \\to Q_{n+1}$ | $S$ | $R$ | $J$ | $K$ | $D$ | $T$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $0 \\to 0$ | $0$ | $\\times$ | $0$ | $\\times$ | $0$ | $0$ |
| $0 \\to 1$ | $1$ | $0$ | $1$ | $\\times$ | $1$ | $1$ |
| $1 \\to 0$ | $0$ | $1$ | $\\times$ | $1$ | $0$ | $1$ |
| $1 \\to 1$ | $\\times$ | $0$ | $\\times$ | $0$ | $1$ | $0$ |

- **Maximum Ripple Counter Frequency:**
  $$f_{\\max} = \\frac{1}{n \\cdot t_{pd}}$$

### 6. Converters & Semiconductor Memories (Unit V)
- **DAC Resolution (Step Size):**
  $$\\Delta V = \\frac{V_{FS}}{2^n - 1}$$
- **Binary Weighted DAC Output:**
  $$V_{out} = -V_{ref} \\frac{R_f}{R} \\sum_{i=0}^{n-1} D_i 2^{-(n-1-i)}$$
- **R-2R Ladder DAC Output:**
  $$V_{out} = V_{ref} \\sum_{i=1}^{n} D_{n-i} 2^{-i}$$
- **ADC Quantization Error:**
  $$Q_e = \\pm \\frac{1}{2} \\text{ LSB}$$
- **SAR ADC Conversion Time:**
  $$t_{\\text{conversion}} = n \\times T_{\\text{clock}}$$
- **Dual-Slope ADC Transfer Equation:**
  $$V_{in} = V_{ref} \\left(\\frac{T_2}{T_1}\\right)$$
- **Memory Capacity:**
  $$\\text{Capacity} = 2^k \\times m \\text{ (where } k = \\text{address lines}, m = \\text{data lines)}$$

---

## B. Complete Master Textbook Figure Citation Directory

| Figure ID | Topic Description | Source Textbook | Chapter & Figure | Page (PDF / Printed) |
|---|---|---|---|---|
| `fig_u1_ttl_totem_pole.png` | Standard TTL NAND Gate with Totem-Pole Output | Anand Kumar | Ch. 4, Fig. 4.2 | p. 165 / p. 133 |
| `fig_u1_cmos_nand.png` | 2-Input CMOS NAND Gate Circuit | Anand Kumar | Ch. 4, Fig. 4.31 | p. 195 / p. 163 |
| `fig_u1_ttl_cmos_interfacing.png` | Interfacing TTL driving CMOS (Pull-Up Resistor) | Anand Kumar | Ch. 4, Fig. 4.36 | p. 201 / p. 169 |
| `fig_u2_kmap_grouping_rules.png` | Standard K-Map Formats (2, 3, 4 Variables) | Anand Kumar | Ch. 5, Fig. 5.1 | p. 238 / p. 206 |
| `fig_u3_full_adder_logic.png` | Full Adder Logic Diagram & Truth Table | Anand Kumar | Ch. 6, Fig. 6.2 | p. 320 / p. 288 |
| `fig_u3_parallel_adder_subtractor.png` | 4-Bit Parallel Binary Adder/Subtractor with XOR | Anand Kumar | Ch. 6, Fig. 6.8 | p. 327 / p. 295 |
| `fig_u3_carry_lookahead_adder.png` | 4-Bit Carry Lookahead Adder (CLA) Generator | Anand Kumar | Ch. 6, Fig. 6.10 | p. 329 / p. 297 |
| `fig_u3_multiplexer_trees.png` | 4-to-1 Multiplexer Internal Logic Gates | Anand Kumar | Ch. 7, Fig. 7.1 | p. 396 / p. 364 |
| `fig_u3_decoder_74138.png` | 3-to-8 Line Decoder (74LS138) Internal Logic | Anand Kumar | Ch. 7, Fig. 7.37 | p. 433 / p. 401 |
| `fig_u3_priority_encoder_74148.png` | 8-to-3 Octal Priority Encoder Logic Diagram | Anand Kumar | Ch. 7, Fig. 7.50 | p. 450 / p. 418 |
| `fig_u4_sr_latch_nor.png` | Basic SR Latch using Cross-Coupled NOR Gates | Anand Kumar | Ch. 10, Fig. 10.1 | p. 556 / p. 524 |
| `fig_u4_clocked_sr_flip_flop.png` | Clocked SR Flip-Flop with NAND Gates | Anand Kumar | Ch. 10, Fig. 10.5 | p. 559 / p. 527 |
| `fig_u4_master_slave_jk.png` | Master-Slave JK Flip-Flop Logic Circuit | Anand Kumar | Ch. 10, Fig. 10.12 | p. 565 / p. 533 |
| `fig_u4_siso_shift_register.png` | 4-Bit Serial-In Serial-Out (SISO) Shift Register | Anand Kumar | Ch. 11, Fig. 11.1 | p. 624 / p. 592 |
| `fig_u4_ripple_counter_4bit.png` | 4-Bit Asynchronous Binary Ripple Counter | Anand Kumar | Ch. 12, Fig. 12.1 | p. 678 / p. 646 |
| `fig_u4_mod10_counter.png` | Mod-10 (Decade) Ripple Counter with Reset | Anand Kumar | Ch. 12, Fig. 12.7 | p. 687 / p. 655 |
| `fig_u4_synchronous_counter_4bit.png` | 4-Bit Synchronous Binary Up-Counter | Anand Kumar | Ch. 12, Fig. 12.11 | p. 696 / p. 664 |
| `fig_u5_weighted_resistor_dac.png` | Binary Weighted-Resistor Summing Op-Amp DAC | Anand Kumar | Ch. 17, Fig. 17.10 | p. 951 / p. 919 |
| `fig_u5_r2r_ladder_dac.png` | R-2R Ladder Type Digital-to-Analog Converter | Anand Kumar | Ch. 17, Fig. 17.5 | p. 947 / p. 915 |
| `fig_u5_counter_type_adc.png` | Logic Diagram of Counter-Type (Ramp) ADC | Anand Kumar | Ch. 17, Fig. 17.15 | p. 958 / p. 926 |
| `fig_u5_dual_slope_adc.png` | Dual-Slope Integrating ADC Architecture | Anand Kumar | Ch. 17, Fig. 17.23 | p. 964 / p. 932 |
| `fig_u5_sar_adc.png` | Successive Approximation Register (SAR) ADC | Anand Kumar | Ch. 17, Fig. 17.24 | p. 965 / p. 933 |
| `fig_u5_adc0801_pinout.png` | Functional Pin Diagram of ADC0801 8-Bit Converter | Anand Kumar | Ch. 17, Fig. 17.25 | p. 967 / p. 935 |
| `fig_u5_memory_organization.png` | 32 × 4 Semiconductor Memory Array & Address Decode | Anand Kumar | Ch. 18, Fig. 18.1 | p. 976 / p. 944 |
| `fig_u5_sram_dram_cells.png` | Static RAM (SRAM) Transistor Storage Cells | Anand Kumar | Ch. 18, Fig. 18.5 | p. 982 / p. 950 |
| `fig_u5_memory_word_length_expansion.png` | Memory Expansion: Word Length ($16\\times 4$ to $16\\times 8$) | Anand Kumar | Ch. 18, Fig. 18.7 | p. 985 / p. 953 |
| `fig_u5_memory_word_capacity_expansion.png` | Memory Expansion: Word Capacity ($16\\times 4$ to $32\\times 4$) | Anand Kumar | Ch. 18, Fig. 18.9 | p. 988 / p. 956 |
| `fig_u5_pld_configurations.png` | Architectural Configurations: PROM, PAL, PLA | Anand Kumar | Ch. 8, Fig. 8.7 | p. 499 / p. 467 |
| `fig_u5_pal_structure.png` | Programmable Array Logic (PAL) Internal Matrix | Anand Kumar | Ch. 8, Fig. 8.8 | p. 500 / p. 468 |
| `fig_u5_pla_structure.png` | Programmable Logic Array (PLA) Internal Matrix | Anand Kumar | Ch. 8, Fig. 8.15 | p. 508 / p. 476 |

---
'''

if __name__ == '__main__':
    print(get_appendix()[:300])
