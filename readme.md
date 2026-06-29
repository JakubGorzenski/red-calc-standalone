# Red Calculator
A standalone version of my [Factorio](https://factorio.com/) mod `red calculator`, implemented in Python using Tkinter.

## How to Run

**Windows:**
- Double-click `red_calculator.bat`

**Command Line:**
```bash
python calc.py
```

**Regression Tests:**
- Double-click `debug.bat`
```bash
python calc.py --test
```

---

## Key Differences from Typical Calculators

### 1. **Three Independent Memory Arrays**
  - Press `Ans`, `B`, or `C` buttons to access stored values
    - subsequent presses cycle through values
    - number buttons can be used to access specific (relative) addresses
  - Memory automatically captures results based on context:
    - **Ans:** Stores recent calculations
    - **B:** Stores results from closing a **B**rackets `(`
    - **C:** Stores any automatic **C**alculation results

### 2. **Native Fraction Support**
  - Input fractions directly: `3` `/` `1` `/` `2` → `3 1/2`
  - Decimal-to-fraction conversion:
    - Automatic: `3.1415` `/` → `333/106`
    - Manual:    `3.1415` `/` `123` → `387/123`

### 3. **Adjustable Precision & Fraction Display**
  - **Precision Slider:** Toggle between 2, 4, 6, or 8 decimal places
  - **Fraction Style Toggle:**
    - Mixed numbers (e.g., `1 1/2`)
    - Improper fractions (e.g., `3/2`)
<!-- re-word this -->
### 4. **Parenthesis Support**
  - Pressing `(` can be used to toggle a bracket
  - After that `=` button will work as a close bracket
> [!NOTE]
> This calculator ignores operator precedence  
> (e.g., `1` `+` `2` `*` `3` `=` → `9.0000`  
> `1` `+` `(` `2` `*` `3` `=` `=` → `7.0000`)  

### 5. **Supported Operations**
  - `+` Addition
  - `−` Subtractions, also works as a unary minus
  - `×` Multiplication, doublepress creates:
    - `^` Exponentiation
  - `÷` Division, when by 0:
    - `sign` return sign of a number (-1, 0 or 1)

### 6. **Error Indication**
  - Question mark (`?`) appears when an invalid operation is attempted
  - Prevents:
    - Invalid button presses
    - Invalid fraction syntax
    - Memory access out of range
    - Multiple decimal points

---

## Button Layout

```
[Sel] [ 7 ] [ 8 ] [ 9 ] [DEL] [CLR]
[ C ] [ 4 ] [ 5 ] [ 6 ] [ − ] [ × ]
[ B ] [ 1 ] [ 2 ] [ 3 ] [ + ] [ ÷ ]
[Ans] [ / ] [ 0 ] [ . ] [ ( ] [ = ]
```

---
<!--
## Example Operations


---
-->

## Features Summary

✅ Fraction arithmetic with automatic approximation  
✅ Mixed number display  
✅ Three automatic memory arrays  
✅ Adjustable decimal precision  
✅ Parenthesis support  
✅ Comprehensive test suite included  
