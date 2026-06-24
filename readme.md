# Red Calc - Advanced Calculator

A feature-rich Python calculator built with Tkinter that goes beyond traditional calculator functionality.

## How to Run

**Windows:**
- Double-click `run.bat` or `calc.bat`

**Command Line:**
```bash
python calc.py
```

**Run Tests:**
```bash
python calc.py --test
```

---

## Key Differences from Traditional Calculators

### 1. **Three Independent Memory Slots**
- **Traditional:** Single memory (M+, M-, MR, MC)
- **This Calculator:** Three separate memory locations (A, B, C)
  - Press `A`, `B`, or `C` buttons to access stored values
  - Memory automatically captures results based on context:
    - **A:** Stores recent calculations
    - **B:** Stores results from operations with brackets `(`
    - **C:** Stores non-equals results

### 2. **Native Fraction Support**
- **Traditional:** Displays decimals only
- **This Calculator:** Full fractional arithmetic
  - Input fractions directly: `1 / 2` (one-half)
  - Mixed numbers: `1 1/2` (one and a half) displayed as `1 1/2`
  - Automatic fraction simplification: `2 / 4` → `1/2`
  - Decimal-to-fraction conversion (e.g., `0.33` → `1/3`)

### 3. **Adjustable Precision & Fraction Display**
- **Precision Slider:** Toggle between 2, 4, 6, or 8 decimal places
- **Fraction Style Toggle:**
  - Style 1: Mixed numbers (e.g., `1 1/2`)
  - Style 2: Improper fractions (e.g., `3/2`)

### 4. **Real-time Operation Display**
- **Traditional:** Shows one number at a time
- **This Calculator:** Two-line display showing:
  - **Line 1:** Previous operation with its result
  - **Line 2:** Current operation being entered
  - Visual indicators for operations (`+`, `−`, `×`, `÷`, `^`) and brackets

### 5. **Bracket/Parenthesis Support**
- Press `(` button to toggle bracket mode
- Brackets affect memory location where result is stored
- Bracket status displayed in real-time

### 6. **Exponentiation Operator**
- **Traditional:** Not typically included
- **This Calculator:** Power operation (`^`)
  - `2 × ×` = `2^2` (press multiplication twice)
  - Supports fractional exponents

### 7. **Advanced Operation Chaining**
- Intermediate results are preserved and displayed
- See the full calculation chain before pressing equals
- If you start a new operation, the previous one auto-calculates

### 8. **Error Indication**
- Question mark (`?`) appears when an invalid operation is attempted
- Prevents entry of:
  - Division by zero (returns sign of numerator)
  - Invalid fraction syntax
  - Memory access out of range
  - Multiple decimal points

### 9. **Intelligent Button Behavior**
- **DEL:** Deletes last character, then last operator, then bracket
- **CLR:** Clears current operation only (keeps history for display)
- **Ans:** Accesses most recent answer from memory
- **−:** Can be used for negative numbers after operations

---

## Button Layout

```
[Sel]  [7]  [8]  [9]  [DEL] [CLR]
[ C ]  [4]  [5]  [6]  [ − ] [ × ]
[ B ]  [1]  [2]  [3]  [ + ] [ ÷ ]
[Ans]  [/]  [0]  [.]  [ ( ] [ = ]
```

**Legend:**
- Blue: Memory/Answer access
- Gray: Numbers and operators
- Green: Operation & equals
- Red: Delete/Clear

---

## Example Operations

| Operation | Traditional Result | This Calculator |
|-----------|-------------------|-----------------|
| `1 ÷ 2 =` | `0.5` | `1/2` (or `0.50` if decimal mode) |
| `1 + 1/2 =` | `1.5` | `1 1/2` |
| `0.333... ≈` | `0.33` | `1/3` (exact) |
| `2 ^ 3 =` | ❌ N/A | `8` |
| Memory | 1 slot | 3 slots (A, B, C) |
| Precision | Fixed | Adjustable (2-8 decimals) |

---

## Features Summary

✅ Fraction arithmetic with automatic simplification  
✅ Mixed number display  
✅ Three independent memory slots  
✅ Adjustable decimal precision  
✅ Bracket/parenthesis support  
✅ Power operations  
✅ Real-time dual-line display  
✅ Error detection with visual feedback  
✅ Comprehensive test suite included  

