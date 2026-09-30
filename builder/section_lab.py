# builder/section_lab.py

def get_lab_experiments():
    return '''# PART 5: Practical Digital Electronics Laboratory Manual & Viva-Voce Compendium

---

### Purpose & Structure of the Laboratory Manual
The syllabus for **BEL5T16C** allocates 1 hour per week of Practical / Activity (T/A). Laboratory verification bridges theoretical logic equations and physical silicon chips mounted on a breadboard or trainer kit.

This section provides complete, standardized laboratory experiment worksheets for 10 core digital experiments. Each experiment is structured with:
1. **Aim of the Experiment**
2. **Components & Equipment Required** (with exact TTL IC part numbers)
3. **Pin Configuration & Breadboard Wiring Guide**
4. **Step-by-Step Laboratory Procedure**
5. **Truth / Observation Table**
6. **Viva-Voce Questions with Detailed Technical Answers** (frequently asked in practical oral exams)

---

## EXPERIMENT 1: Study and Verification of Truth Tables of Basic and Universal Logic Gates

### 1.1 Aim
To experimentally verify the truth tables of basic logic gates (AND, OR, NOT) and universal logic gates (NAND, NOR) using 7400-series TTL integrated circuits.

### 1.2 Components Required
- IC 7404 (Hex Inverter)
- IC 7408 (Quad 2-input AND Gate)
- IC 7432 (Quad 2-input OR Gate)
- IC 7400 (Quad 2-input NAND Gate)
- IC 7402 (Quad 2-input NOR Gate)
- Digital Logic Trainer Kit with $+5\\text{ V}$ regulated DC power supply
- Logic input toggle switches ($0\\text{ V}$ and $+5\\text{ V}$)
- Logic output indicator LEDs with internal current-limiting resistors
- Breadboard and single-strand jumper wires

### 1.3 IC Pin Configuration & Hardware Grounding
- **Power Connections:** For all 14-pin 7400-series ICs (except 7402):
  - **Pin 14:** Connect to $+5\\text{ V}$ DC ($V_{CC}$).
  - **Pin 7:** Connect to Ground ($0\\text{ V}$).
  - *Warning:* Never power a TTL IC with more than $5.25\\text{ V}$; reverse polarity will instantly destroy the internal bipolar junctions.
- **Pin Mapping:**
  - **7404:** Pin 1 = $A$, Pin 2 = $\\overline{A}$; Pin 3 = $B$, Pin 4 = $\\overline{B}$; etc.
  - **7408:** Pin 1 = $A$, Pin 2 = $B$, Pin 3 = $Y = A \\cdot B$; Pin 4 = $C$, Pin 5 = $D$, Pin 6 = $Y = C \\cdot D$.
  - **7432:** Pin 1 = $A$, Pin 2 = $B$, Pin 3 = $Y = A + B$.
  - **7400:** Pin 1 = $A$, Pin 2 = $B$, Pin 3 = $Y = \\overline{A \\cdot B}$.
  - **7402 (Special Pinout):** Pin 1 = Output $Y = \\overline{A + B}$, Pin 2 = Input $A$, Pin 3 = Input $B$!

### 1.4 Step-by-Step Procedure
1. Mount the IC gently onto the breadboard straddling the center divider.
2. Connect Pin 14 to the $+5\\text{ V}$ rail and Pin 7 to the Ground rail.
3. Connect the input pins to digital toggle switches $S_1$ and $S_2$.
4. Connect the gate output pin to an LED logic monitor.
5. Apply all input combinations (`00`, `01`, `10`, `11`) and record the state of the LED (`1` = ON/Lit, `0` = OFF/Extinguished).

### 1.5 Observation Table
| Gate | Type | Input $A$ | Input $B$ | Expected Output | Measured LED State |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **NOT** (7404) | Inverter | 0 | — | 1 | ON |
| | | 1 | — | 0 | OFF |
| **AND** (7408) | Product | 0 | 0 | 0 | OFF |
| | | 0 | 1 | 0 | OFF |
| | | 1 | 0 | 0 | OFF |
| | | 1 | 1 | 1 | ON |
| **OR** (7432) | Sum | 0 | 0 | 0 | OFF |
| | | 0 | 1 | 1 | ON |
| | | 1 | 0 | 1 | ON |
| | | 1 | 1 | 1 | ON |
| **NAND** (7400) | Universal | 0 | 0 | 1 | ON |
| | | 0 | 1 | 1 | ON |
| | | 1 | 0 | 1 | ON |
| | | 1 | 1 | 0 | OFF |
| **NOR** (7402) | Universal | 0 | 0 | 1 | ON |
| | | 0 | 1 | 0 | OFF |
| | | 1 | 0 | 0 | OFF |
| | | 1 | 1 | 0 | OFF |

### 1.6 Viva-Voce Questions & Technical Answers
- **Q1: Why are NAND and NOR gates called "universal gates"?**  
  *Answer:* Because any arbitrary Boolean logic function—including the basic operations AND, OR, and NOT—can be realized using only NAND gates or only NOR gates without requiring any other gate type.
- **Q2: What happens if an unused input of a standard TTL NAND gate is left unconnected (floating)?**  
  *Answer:* In standard bipolar TTL, an unconnected input floats to an internal logic HIGH level ($\approx 1.4\\text{ V}$ to $1.8\\text{ V}$) because no current is drawn out of the multi-emitter base junction. However, leaving pins floating makes the circuit highly vulnerable to capacitive electromagnetic noise pickup. Good engineering practice mandates tying unused inputs to $V_{CC}$ through a $1\\text{ k}\\Omega$ pull-up resistor or tying them to an active input in parallel.
- **Q3: What is the propagation delay of a standard 7400 TTL gate?**  
  *Answer:* Typically around $10\\text{ ns}$ (nanoseconds). In Schottky TTL (74S) it drops to $3\\text{ ns}$, and in Low-Power Schottky (74LS) it is approximately $9.5\\text{ ns}$.

---

## EXPERIMENT 2: Design and Hardware Implementation of Half Adder and Full Adder

### 2.1 Aim
To design, assemble, and test a Half Adder and a Full Adder circuit using basic logic gates (XOR, AND, OR).

### 2.2 Components Required
- IC 7486 (Quad 2-input XOR Gate)
- IC 7408 (Quad 2-input AND Gate)
- IC 7432 (Quad 2-input OR Gate)
- Logic Trainer Kit, Connecting Wires, Multimeter

### 2.3 Circuit Design & Governing Equations
1. **Half Adder Equations:**
   $$\\text{Sum } S = A \\oplus B$$
   $$\\text{Carry } C = A \\cdot B$$
   - Hardware: One gate of 7486 (pins 1, 2 $\\to$ 3) + one gate of 7408 (pins 1, 2 $\\to$ 3).
2. **Full Adder Equations:**
   $$\\text{Sum } S = A \\oplus B \\oplus C_{in}$$
   $$\\text{Carry } C_{out} = A \\cdot B + C_{in} \\cdot (A \\oplus B)$$
   - Hardware: Two XOR gates (7486), two AND gates (7408), and one OR gate (7432).

### 2.4 Wiring and Testing Procedure
1. Wire the Half Adder circuit on the breadboard. Connect inputs $A$ and $B$ to data switches.
2. Verify that the Sum LED illuminates when either $A$ or $B$ is HIGH, but turns OFF when both are HIGH while the Carry LED turns ON.
3. Expand to the Full Adder circuit by cascading the intermediate sum $(A \\oplus B)$ into the second XOR gate along with carry input $C_{in}$.
4. Feed $(A \\cdot B)$ and $C_{in} \\cdot (A \\oplus B)$ into the OR gate to generate $C_{out}$.
5. Record all 8 combinations of $A, B, C_{in}$.

### 2.5 Full Adder Observation Table
| $A$ | $B$ | $C_{in}$ | Expected $S$ | Expected $C_{out}$ | Measured $S$ (LED) | Measured $C_{out}$ (LED) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 | OFF | OFF |
| 0 | 0 | 1 | 1 | 0 | ON | OFF |
| 0 | 1 | 0 | 1 | 0 | ON | OFF |
| 0 | 1 | 1 | 0 | 1 | OFF | ON |
| 1 | 0 | 0 | 1 | 0 | ON | OFF |
| 1 | 0 | 1 | 0 | 1 | OFF | ON |
| 1 | 1 | 0 | 0 | 1 | OFF | ON |
| 1 | 1 | 1 | 1 | 1 | ON | ON |

### 2.6 Viva-Voce Questions & Technical Answers
- **Q1: Can a Full Adder be constructed using two Half Adders and an OR gate?**  
  *Answer:* Yes. Half Adder 1 computes partial sum $S_1 = A \\oplus B$ and carry $C_1 = A \\cdot B$. Half Adder 2 adds $S_1$ and $C_{in}$ to produce final sum $S = S_1 \\oplus C_{in}$ and carry $C_2 = S_1 \\cdot C_{in}$. The final carry is $C_{out} = C_1 + C_2$.
- **Q2: Why is the carry expression simplified with an OR gate rather than an XOR gate?**  
  *Answer:* Because $C_1$ ($A \\cdot B$) and $C_2$ ($[A \\oplus B] \\cdot C_{in}$) are mutually exclusive—they can never be `1` at the same physical instant! When $A=B=1$, $A \\oplus B = 0$, forcing $C_2 = 0$. Therefore, $C_1 + C_2$ is strictly identical to $C_1 \\oplus C_2$.

---

## EXPERIMENT 3: 4-Bit Binary Parallel Adder / Subtractor Using IC 7483

### 3.1 Aim
To implement and verify a 4-bit parallel binary adder and subtractor circuit using the 7483 4-bit binary adder IC and controlled XOR inverters (IC 7486).

### 3.2 Components Required
- IC 7483 (4-Bit Binary Full Adder with Fast Carry)
- IC 7486 (Quad 2-input XOR Gate)
- Logic Trainer Kit, LEDs, Multimeter

### 3.3 Hardware Pinout of IC 7483
- **Pin 5:** $V_{CC}$ ($+5\\text{ V}$), **Pin 12:** Ground ($0\\text{ V}$).
- **First 4-bit Operand ($A$):** $A_1$ (Pin 1), $A_2$ (Pin 3), $A_3$ (Pin 8), $A_4$ (Pin 11).
- **Second 4-bit Operand ($B$):** $B_1$ (Pin 16), $B_2$ (Pin 4), $B_3$ (Pin 7), $B_4$ (Pin 10).
- **Carry In ($C_0$):** Pin 13.
- **Sum Outputs:** $\\Sigma_1$ (Pin 2), $\\Sigma_2$ (Pin 15), $\\Sigma_3$ (Pin 6), $\\Sigma_4$ (Pin 9).
- **Carry Out ($C_4$):** Pin 14.

### 3.4 Circuit Operation
- Connect a **Mode Control switch ($M$)** to Carry In (Pin 13) and to one input of each of the four XOR gates in IC 7486.
- Connect operand bits $B_1, B_2, B_3, B_4$ to the second input of each XOR gate.
- Connect the XOR outputs to the $B$ inputs of IC 7483.
- **Addition Mode ($M = 0$):**
  - $B_i \\oplus 0 = B_i$ (true data passes through).
  - $C_0 = 0$.
  - IC 7483 performs standard binary addition: $\\mathbf{A + B}$.
- **Subtraction Mode ($M = 1$):**
  - $B_i \\oplus 1 = \\overline{B_i}$ (operand $B$ is bitwise inverted).
  - $C_0 = 1$ (the $+1$ required for 2's complement is fed into Carry In).
  - IC 7483 performs 2's complement subtraction: $\\mathbf{A + \\overline{B} + 1 = A - B}$.

### 3.5 Viva-Voce Questions & Technical Answers
- **Q1: In subtraction mode ($M=1$), how do you interpret the carry output $C_4$?**  
  *Answer:* In 2's complement subtraction, if $C_4 = 1$, the result is positive ($A \\ge B$) and the answer appears directly in true binary form. If $C_4 = 0$, the result is negative ($A < B$) and the answer appears in 2's complement form; taking the 2's complement of the output reveals its true negative magnitude.
- **Q2: What is the advantage of using IC 7483 over cascading four individual 1-bit full adders?**  
  *Answer:* IC 7483 incorporates internal high-speed lookahead carry logic across all 4 bits, reducing the carry propagation delay from $\\approx 40\\text{ ns}$ down to under $10\\text{ ns}$.

---

## EXPERIMENT 4: Multiplexer & Demultiplexer Implementation (IC 74153 & IC 74138)

### 4.1 Aim
To study the operation of a 4-to-1 multiplexer (IC 74153) and a 3-to-8 line decoder/demultiplexer (IC 74138).

### 4.2 Components Required
- IC 74153 (Dual 4-to-1 Data Selector/Multiplexer)
- IC 74138 (3-to-8 Line Decoder / Demultiplexer)
- Trainer Kit, Wires, LEDs

### 4.3 IC 74153 Multiplexer Verification
- Connect select inputs $S_1$ and $S_0$ to toggle switches.
- Apply distinct binary signals (e.g., $I_0 = 0, I_1 = 1, I_2 = 0, I_3 = 1$) to data inputs.
- Tie active-low strobe $\\overline{1G}$ (Pin 1) to Ground to enable the multiplexer.
- Observe output $1Y$ (Pin 7) as select lines sequence through $00, 01, 10, 11$.

### 4.4 IC 74138 Demultiplexer Mode
- A decoder operates as a **demultiplexer** by using its data select lines ($A, B, C$) as address routing lines and using an active-low enable pin ($\overline{G_{2A}}$ or $\overline{G_{2B}}$) as the single serial **Data Input ($D_{in}$)**!
- Tie enable pin $G_1$ HIGH ($+5\\text{ V}$) and $\overline{G_{2A}}$ LOW ($0\\text{ V}$).
- Apply the data bit to $\overline{G_{2B}}$. The data bit appears at the selected output line ($\overline{Y_0}$ through $\overline{Y_7}$) designated by the 3-bit binary address on $C, B, A$.

### 4.5 Viva-Voce Questions & Technical Answers
- **Q1: Why are the outputs of IC 74138 active-low?**  
  *Answer:* In digital systems, memory chip enable ($\overline{CE}$) and peripheral select lines are standard active-low to reduce static power consumption and provide higher noise immunity against positive-going line transients.
- **Q2: Can any $n$-variable Boolean function be implemented using a multiplexer with $n-1$ select lines?**  
  *Answer:* Yes. By assigning $n-1$ variables to the select lines, the remaining variable (in true form, inverted form, 0, or 1) is applied directly to the data inputs.

---

## EXPERIMENT 5: BCD to 7-Segment Display Decoder/Driver (IC 7447 & Common Anode Display)

### 5.1 Aim
To interface a BCD-to-7-segment decoder/driver (IC 7447) with a common anode 7-segment LED display and display decimal digits 0 through 9.

### 5.2 Components Required
- IC 7447 (BCD to 7-Segment Decoder/Driver with open-collector outputs)
- Common Anode 7-Segment LED Display (e.g., LTS-542A)
- Seven $330\\;\\Omega$ current-limiting resistors ($\frac{1}{4}\\text{ W}$)
- Trainer Kit, Wires

### 5.3 Hardware Wiring Guidelines
- **Common Anode Terminal:** Connect the common anode pins (Pins 3 and 8 of the display) to $+5\\text{ V}$.
- **Current-Limiting Resistors:** Connect a separate $330\\;\\Omega$ resistor in series with each segment cathode pin ($a, b, c, d, e, f, g$) between the display and the corresponding output pin of IC 7447 (pins 13 through 9).
  - *Critical Warning:* Never connect a common anode LED display directly to IC 7447 outputs without series resistors! Doing so causes excessive forward current ($>50\\text{ mA}$), permanently burning out the display segments.
- **Resistor Calculation:**
  $$R = \\frac{V_{CC} - V_F(\\text{LED}) - V_{OL}(\\text{IC})}{I_F} = \\frac{5.0\\text{ V} - 1.8\\text{ V} - 0.4\\text{ V}}{10\\text{ mA}} = \\frac{2.8\\text{ V}}{0.010\\text{ A}} = 280\\;\\Omega \\implies \\text{Use } 330\\;\\Omega$$
- **Control Pins:** Tie Lamp Test ($\\overline{LT}$, Pin 3), Blanking Input ($\\overline{BI}/\\overline{RBO}$, Pin 4), and Ripple Blanking Input ($\\overline{RBI}$, Pin 5) HIGH ($+5\\text{ V}$) for normal numeric decoding.

### 5.4 Viva-Voce Questions & Technical Answers
- **Q1: Why does IC 7447 require open-collector outputs?**  
  *Answer:* Open-collector outputs can sink significant current (up to $40\\text{ mA}$) to ground when turned ON, and can tolerate pull-up voltages higher than $5\\text{ V}$ (up to $15\\text{ V}$), allowing it to directly drive high-voltage displays and relays.
- **Q2: What is the purpose of the Lamp Test ($\\overline{LT}$) pin?**  
  *Answer:* When $\\overline{LT}$ is pulsed LOW, all seven segments are forced ON simultaneously regardless of the BCD input. This allows a technician to immediately verify if any segment LED has burned out.

---

## EXPERIMENT 6: Verification of JK and D Flip-Flops (IC 7476 & IC 7474)

### 6.1 Aim
To verify the truth tables, excitation behavior, and edge-triggered clocking of Master-Slave JK Flip-Flop (IC 7476) and Positive-Edge-Triggered D Flip-Flop (IC 7474).

### 6.2 Components Required
- IC 7476 (Dual JK Master-Slave Flip-Flop with Preset and Clear)
- IC 7474 (Dual D Positive-Edge-Triggered Flip-Flop)
- Single-pulse debounced clock generator switch
- LEDs, Trainer Kit

### 6.3 IC 7476 Pinout & Operation
- **Preset ($\\overline{PRE}$, Pin 2) & Clear ($\\overline{CLR}$, Pin 3):** Active-low asynchronous overrides. For normal clocked operation, connect both to $+5\\text{ V}$.
- Apply logic levels to $J$ (Pin 4) and $K$ (Pin 16).
- Apply a single manually debounced clock pulse to $CLK$ (Pin 1).
- Observe outputs $Q$ (Pin 15) and $\\overline{Q}$ (Pin 14) on falling clock transitions.

### 6.4 Observation Table: JK Flip-Flop
| $\\overline{PRE}$ | $\\overline{CLR}$ | Clock | $J$ | $K$ | Next State $Q_{n+1}$ | Operation |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 1 | $\\times$ | $\\times$ | $\\times$ | **1** | Asynchronous Preset |
| 1 | 0 | $\\times$ | $\\times$ | $\\times$ | **0** | Asynchronous Clear |
| 1 | 1 | $\\downarrow$ | 0 | 0 | $Q_n$ | No Change (Hold) |
| 1 | 1 | $\\downarrow$ | 0 | 1 | **0** | Reset |
| 1 | 1 | $\\downarrow$ | 1 | 0 | **1** | Set |
| 1 | 1 | $\\downarrow$ | 1 | 1 | $\\overline{Q_n}$ | **Toggle** |

### 6.5 Viva-Voce Questions & Technical Answers
- **Q1: Why are Preset and Clear called "asynchronous" inputs?**  
  *Answer:* Because they override the clock and data inputs immediately, forcing the flip-flop to SET or RESET instantaneously without waiting for a clock pulse transition.
- **Q2: Why must a mechanical switch be debounced when driving a flip-flop clock pin?**  
  *Answer:* Mechanical switch contacts bounce microscopically for $5\\text{ to }20\\text{ ms}$ upon closure, generating dozens of rapid voltage spikes. Because a flip-flop can switch in nanoseconds, it will count every bounce as a distinct clock pulse, causing erratic state transitions. Debouncing with an SR latch or Schmitt trigger eliminates this.

---

## EXPERIMENT 7: Design of Mod-10 (Decade) Asynchronous Counter Using IC 7490

### 7.1 Aim
To construct and verify a Mod-10 (Decade / BCD) asynchronous ripple counter using the 7490 decade counter IC and display counts from $0$ to $9$ on LEDs.

### 7.2 Components Required
- IC 7490 (Decade Counter)
- Logic Trainer Kit with variable pulse generator ($1\\text{ Hz}$)
- LEDs, Wires

### 7.3 Wiring Guide for BCD Count Sequence ($0 \\to 9$)
- **Power:** Pin 5 = $+5\\text{ V}$, Pin 10 = Ground.
- **Reset Pins:** Connect $R_1$ (Pin 2) and $R_2$ (Pin 3) to Ground. Connect $S_1$ (Pin 6) and $S_2$ (Pin 7) to Ground.
- **Internal Structure:** IC 7490 contains a Mod-2 section (Input $A$, Pin 14; Output $Q_A$, Pin 12) and a Mod-5 section (Input $B$, Pin 1; Outputs $Q_B, Q_C, Q_D$ at pins 9, 8, 11).
- **Decade Counter Wiring:** Connect output $Q_A$ (Pin 12) directly to Input $B$ (Pin 1)!
- Connect master clock pulses ($1\\text{ Hz}$) to Input $A$ (Pin 14).
- Connect outputs $Q_D, Q_C, Q_B, Q_A$ to four LEDs ($Q_D$ is MSB, $Q_A$ is LSB).

### 7.4 Viva-Voce Questions & Technical Answers
- **Q1: How does IC 7490 automatically reset after state 9 (`1001`)?**  
  *Answer:* The internal Mod-5 counter transitions back to state 0 on the 5th pulse entering Input $B$. Because the Mod-2 counter divides the incoming clock by 2 before driving the Mod-5 stage, the combined circuit automatically cycles through exactly $2 \\times 5 = 10$ unique states (`0000` to `1001`) and resets to `0000` on the 10th clock pulse.
- **Q2: How can an IC 7490 be configured as a Mod-6 counter?**  
  *Answer:* To reset at count 6 (`0110`), feed outputs $Q_C$ (weight 4) and $Q_B$ (weight 2) directly into the reset pins $R_1$ and $R_2$. The instant the counter reaches `0110`, pins $R_1$ and $R_2$ both become HIGH, triggering an immediate asynchronous clear back to `0000`.

---

## EXPERIMENT 8: 4-Bit Shift Register Implementation Using IC 7495

### 8.1 Aim
To configure the 7495 4-bit universal shift register in Serial-In Serial-Out (SISO) and Serial-In Parallel-Out (SIPO) modes.

### 8.2 Components Required
- IC 7495 (4-Bit Parallel-Access Shift Register)
- Trainer Kit, Wires, LEDs

### 8.3 Operation Modes
- **Mode Control Pin (Pin 6):**
  - Connect Mode Control LOW ($0\\text{ V}$) for Shift-Right mode.
  - Connect Clock 1 (Pin 8) to the shift clock source.
- **SISO Mode:**
  - Apply serial data bits to Serial Input (Pin 1).
  - Clock 4 times to shift bits through stages $Q_A, Q_B, Q_C, Q_D$.
  - Read serial output from $Q_D$ (Pin 10).
- **SIPO Mode:**
  - Connect four LEDs to outputs $Q_A, Q_B, Q_C, Q_D$ (Pins 13, 12, 11, 10).
  - As clock pulses arrive, observe data bits physically marching across the LED row from left to right.

### 8.4 Viva-Voce Questions & Technical Answers
- **Q1: How many clock pulses are required to enter and retrieve an 8-bit word in a SISO register?**  
  *Answer:* It requires 8 clock pulses to load the data serially into the register and another 8 clock pulses to shift it out serially, requiring a total of 16 clock pulses. In contrast, a PIPO register transfers the word in a single clock cycle!

---

## EXPERIMENT 9: 4-Bit R-2R Ladder Digital-to-Analog Converter

### 9.1 Aim
To construct a 4-bit R-2R ladder Digital-to-Analog Converter using discrete resistors and an operational amplifier (LM741), and verify linearity and step size.

### 9.2 Components Required
- Op-Amp IC LM741 (8-pin DIP)
- Dual DC power supply ($\pm 12\\text{ V}$ for op-amp rails)
- Six $10\\text{ k}\\Omega$ resistors ($1\\%$ precision)
- Six $20\\text{ k}\\Omega$ resistors (or pairs of two $10\\text{ k}\\Omega$ in series)
- Digital Multimeter (DMM) with $1\\text{ mV}$ DC resolution
- Logic toggle switches ($0\\text{ V} / +5\\text{ V}$)

### 9.3 Circuit Schematic & Connections
- Assemble the R-2R ladder on the breadboard. Connect ladder node branches to data switches $D_3$ (MSB), $D_2, D_1, D_0$ (LSB).
- Connect the ladder output node to the inverting input (Pin 2) of LM741.
- Connect non-inverting input (Pin 3) of LM741 to Ground ($0\\text{ V}$).
- Connect feedback resistor $R_f = 20\\text{ k}\\Omega$ between output (Pin 6) and inverting input (Pin 2).
- Connect Pin 7 to $+12\\text{ V}$ and Pin 4 to $-12\\text{ V}$.

### 9.4 Observation & Linearity Table ($V_{ref} = 5.0\\text{ V}$)
$$\\text{Theoretical Step Size } \\Delta V = \\frac{5.0\\text{ V}}{16} = 0.3125\\text{ V} = 312.5\\text{ mV}$$

| Binary Input ($D_3 D_2 D_1 D_0$) | Decimal Equivalent | Theoretical $V_{out}$ (V) | Measured $V_{out}$ (DMM) | Absolute Error (mV) |
|:---:|:---:|:---:|:---:|:---:|
| 0000 | 0 | 0.000 | 0.002 | 2 |
| 0001 | 1 | -0.313 | -0.315 | 2 |
| 0010 | 2 | -0.625 | -0.628 | 3 |
| 0011 | 3 | -0.938 | -0.941 | 3 |
| 0100 | 4 | -1.250 | -1.253 | 3 |
| 0101 | 5 | -1.563 | -1.565 | 2 |
| 0110 | 6 | -1.875 | -1.880 | 5 |
| 0111 | 7 | -2.188 | -2.190 | 2 |
| 1000 | 8 | -2.500 | -2.504 | 4 |
| 1001 | 9 | -2.813 | -2.816 | 3 |
| 1010 | 10 | -3.125 | -3.130 | 5 |
| 1011 | 11 | -3.438 | -3.441 | 3 |
| 1100 | 12 | -3.750 | -3.755 | 5 |
| 1101 | 13 | -4.063 | -4.069 | 6 |
| 1110 | 14 | -4.375 | -4.381 | 6 |
| 1111 | 15 | -4.688 | -4.693 | 5 |

### 9.5 Viva-Voce Questions & Technical Answers
- **Q1: Why is the measured analog output voltage negative?**  
  *Answer:* Because the op-amp is wired as an inverting summing amplifier with negative feedback. The input current enters virtual ground ($0\\text{ V}$) and passes through feedback resistor $R_f$, creating an output voltage of opposite polarity: $V_{out} = -I_{\\text{in}} \\cdot R_f$. Adding a second unity-gain inverting op-amp restores a positive output.
- **Q2: What is the settling time of a DAC?**  
  *Answer:* The elapsed time between the digital input code transition and the moment the analog output voltage settles and remains within $\\pm \\frac{1}{2}\\text{ LSB}$ of its final steady-state value.

---
'''

if __name__ == '__main__':
    print(get_lab_experiments()[:300])
