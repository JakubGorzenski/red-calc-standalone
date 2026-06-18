import tkinter as tk
import copy as copy

# Global font configuration
DISPLAY_FONT = ("Courier New", 18)
BUTTON_FONT = ("Courier New", 18)

class OperationEntry:
    def __init__(self, number="", rq_op=" ", bracket=" ", calculated=False, stub=False):
        self.number = number
        self.rq_op = rq_op
        self.bracket = bracket
        self.calculated = calculated
        self.stub = stub
class Context:
    def __init__(self):
        self.operation_stack = []
        self.number_memory   = {"A": ["0.00000000"], "B": ["0.00000000"], "C": ["0.00000000"]} # starts with "" in lists so you can read [0]
        self.greyed_out      = False
        self.precision       = 2
        self.fraction_style  = 1
        self.question_mark   = " "


def main(run_tests=False):
    C = Context()

    window = tk.Tk()
    root = tk.Frame(window)
    root.pack(fill="both", expand=True, padx=5, pady=5)

    # Text display (output only) - 2 lines tall with monospace font
    display = tk.Text(root, font=DISPLAY_FONT, height=2, state="disabled", width=len("+(-12345 1234567890/1234567890 [A5]"))
    display.pack(padx=1, pady=1)
    display.tag_configure("greyed", foreground="gray")


    def at(array, index, default=None):
        """return array[index] or default"""
        if len(array) >= abs(index) and len(array) > index:
            return array[index]
        return default
    def current_operation(C):
        if len(C.operation_stack) == 0:
            C.operation_stack.append(OperationEntry())
        return C.operation_stack[-1]
    def previous_operation(C, go_further_back_by = 0):
        if len(C.operation_stack) > go_further_back_by + 1:
            return C.operation_stack[-2 - go_further_back_by]
        else:
            return OperationEntry(stub=True)
    def is_current_valid(C):
        curr = current_operation(C)
        prev = previous_operation(C)

        if prev.rq_op == "÷" and prev.bracket == " " and string_round(C, curr, to_float=True) == 0.0:
            return False
        if curr.number in {"", "-"} or curr.number[-1] == ".":
            return False
        elif curr.number[-1] == "/" and "." not in curr.number:
            return False
        return True

    def clr_if_blank(C):
        curr = current_operation(C)
        if curr.number == "":
            C.operation_stack.pop()
    def append_to_number(C, value):
        curr = current_operation(C)
        if curr.calculated and value != "/":
            curr.number = string_round(C, curr)
            curr.calculated = False

        p_char = at(curr.number, -1)

        if value == "/" and p_char == "/":
            curr.number = curr.number[:-1]
        elif at(curr.number, 0) in {"A", "B", "C"}:
            last_num_mem = len(C.number_memory[at(curr.number, 0)]) - 1
            if at(curr.number, 0) == value:
                next = at(curr.number, 1)
                if next == "/":
                    next = None
                next = int(next or -1) + 1
                if next >= last_num_mem:
                    C.question_mark = "?"
                    return
                curr.number = value + str(next)
            elif value in {"A", "B", "C"}:
                curr.number = value
            elif value in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                if int(value) >= last_num_mem:
                    C.question_mark = "?"
                    return
                curr.number = curr.number[0] + value

            elif value == "/":
                curr.number += "/"

        elif value in {".", "/"}:
            count = curr.number.count(".") + curr.number.count("/")
            if value == "." and count < 1:
                curr.number += "."
            elif value == "/" and count < 2 and p_char != ".":
                curr.number += "/"
            else:
                C.question_mark = "?"
        elif p_char == "/" and value == "0":
            C.question_mark = "?"
        elif curr.number == "" or value in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
            curr.number += value
        else:
            C.question_mark = "?"

    def to_fraction(decimal_part):
        def frc(f, i):
            if i == 0:
                return 1, int(1 / f)

            n, d = frc(1/f % 1, i - 1)
            n += int(1 / f) * d
            return d, n

        f = float("0." + decimal_part)
        p = len(decimal_part) + 2
        i = 0

        if f == 0.0:
            return 0, 1

        while True:
            n, d = frc(f, i)
            i += 1
            if f"{n/d:.9f}"[2:p] == decimal_part:
                return n, d
            if i > 15:
                return n, d
    def string_round(C, operation_entry, visual_modification=False, to_float=False, check_if_fraction=False):
        string = operation_entry.number
        calculated = operation_entry.calculated

        if at(string, 0) in {"A", "B", "C"}:
            calculated = True
            idx = at(string, 1, "")
            append = at(string, 2, "")
            if idx in {"", "/"}:
                append = idx
                idx = 0
            else:
                idx = 1 + int(idx)
            string = C.number_memory[string[0]][int(idx)] + append
            if string[-2:] == "//":
                string = string[:-2]

        if visual_modification:
            separator = " "
            ch_sign = " "
        else:
            separator = "/"
            ch_sign = ""
        
        if at(string, 0) == '-':
            string = string[1:]
            ch_sign = "-"
            sign = -1
        else:
            sign = 1

        fraction = string.split("/")
        
        if "." in fraction[0]:
            whole, decimal_part = fraction[0].split(".")
            if calculated:
                decimal_part = decimal_part[:C.precision]
            if len(fraction) == 1:
                ret_string = f"{whole}.{decimal_part}"
                ret_float  = float(ret_string + "0")
            elif len(fraction) == 2:
                if whole == "0":
                    whole = ""
                if fraction[1]:
                    ret_string = f"{whole and whole + separator}{round(int(fraction[1] or 0) * float("0." + decimal_part))}/{fraction[1]}"
                    ret_float  = int(whole or 0) +               round(int(fraction[1] or 0) * float("0." + decimal_part)) / int(fraction[1] or 1)
                else:
                    n, d = to_fraction(decimal_part)
                    if C.fraction_style == 2:
                        n += int(whole or 0) * d
                        whole = ""
                    if n == 0:
                        ret_string = f"{whole or "0"}"
                    else:
                        ret_string = f"{whole and whole + separator}{n}/{d}"
                    ret_float  = int(whole or 0) +               n / d

        elif len(fraction) == 1:
            ret_string = string
            ret_float  = int(fraction[0] or 0)
        elif len(fraction) == 2:
            ret_string = f"{fraction[0] or "1"}/{fraction[1]}"
            ret_float  = int(fraction[0] or 1) / int(fraction[1] or 1)
        elif len(fraction) == 3:
            ret_string = f"{fraction[0] or "1"}{separator}{fraction[1] or "1"}/{fraction[2]}"
            ret_float  = int(fraction[0] or 1) +       int(fraction[1] or 1) / int(fraction[2] or 1)
        
        if to_float:
            if check_if_fraction:
                                        # int + int => 2
                                        # frc + int => 3
                                        # frc + frc => 4
                return ret_float * sign, (len(fraction) > 1) * 2 or ret_float.is_integer()
            return ret_float * sign
        else:
            return ch_sign + ret_string
    def insert_number_memory(C, bracket, number):
        if C.number_memory["C"][0] != number:
            C.number_memory["C"].insert(0, number)
            C.number_memory["C"] = C.number_memory["C"][:11]

        if bracket == "(":
            if C.number_memory["B"][0] != number:
                C.number_memory["B"].insert(0, number)
                C.number_memory["B"] = C.number_memory["B"][:11]
        else:
            if C.number_memory["A"][0] != number:
                C.number_memory["A"].insert(0, number)
                C.number_memory["A"] = C.number_memory["A"][:11]


    def calculate(C, return_result=False, equals=False):
        curr = current_operation(C)
        prev = previous_operation(C)
        
        if prev.stub or prev.bracket == "(":
            if equals:
                if curr.rq_op != " ":
                    C.question_mark = "?"
                    return None
                curr.number, cn_frc = string_round(C, curr, to_float=True, check_if_fraction=True)
                curr.number = f"{curr.number:.9f}"
                curr.calculated = True
                insert_number_memory(C, prev.bracket, curr.number + "/" * (cn_frc >= 2))
                return curr
            return None

        a, a_frc = string_round(C, prev, to_float=True, check_if_fraction=True)
        op = prev.rq_op
        b, b_frc = string_round(C, curr, to_float=True, check_if_fraction=True)

        frc = "/" if a_frc + b_frc > 2 else ""
        result = 0.0

        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "×":
            result = a * b
        elif op == "^":
            result = a ** b
        elif op == "÷":
            assert b != 0.0, "Division by 0, shoud not be posibble to enter!"
            result = a / b

        if return_result:
            prev = OperationEntry()

        prev.number = f"{result:.9f}" + frc
        prev.calculated = True

        if not return_result:
            insert_number_memory(C, previous_operation(C, 1).bracket, prev.number)

        if not C.greyed_out:
            prev.rq_op = curr.rq_op
            prev.bracket = curr.bracket
            if not return_result:
                C.operation_stack.pop()

        return prev
    def update_display(C, is_test=False):
        prev2 = previous_operation(C, 1)
        prev = previous_operation(C)
        curr = current_operation(C)

        line_3 = f"{curr.rq_op}{curr.bracket}"

        if line_3 != "  ":
            calc = calculate(C, return_result=True)
            if calc:
                line_1 = f"{prev2.rq_op}{prev2.bracket}{string_round(C, calc, True):31}{C.question_mark}\n"
            else:
                line_1 = f"{prev.rq_op}{prev.bracket}{string_round(C, curr, True):31}{C.question_mark}\n"
            line_2 = line_3
        else:
            line_1 = f"{prev2.rq_op}{prev2.bracket}{string_round(C, prev, True):31}{C.question_mark}\n"
            line_2 = f"{prev.rq_op}{prev.bracket}{string_round(C, curr, True)}"

        if is_test:
            return line_1 + line_2

        display.config(state="normal")
        display.delete(1.0, tk.END)
        
        display.insert(1.0, line_1)
        display.insert(tk.END, line_2, "greyed" if C.greyed_out else None)
        
        display.config(state="disabled")


    def handle_equals_button(C):
        prev = previous_operation(C)

        if not is_current_valid(C):
            C.question_mark = "?"
            return

        if len(C.operation_stack) == 2 and prev.bracket == " ":
            C.greyed_out = True

        if calculate(C, equals=True):
            previous_operation(C).bracket = " "
    def handle_del_button(C):
        """Delete the last character from current number"""
        if C.greyed_out:
            C.greyed_out = False
            return

        curr = current_operation(C)

        if curr.bracket != " ":
            curr.bracket = " "
        elif curr.rq_op != " ":
            curr.rq_op = " "
        elif curr.number:
            if curr.calculated:
                curr.number = string_round(C, curr)
                curr.calculated = False
            curr.number = curr.number[:-1]

        clr_if_blank(C)
    def handle_clr_button(C):
        """Clear the newest line (current operation)"""
        C.operation_stack.pop()
    def handle_number_button(C, value):
        curr = current_operation(C)

        if C.greyed_out and value == "/":
            curr.rq_op = " "
        elif curr.rq_op != " ":
            calculate(C)
            C.operation_stack.append(OperationEntry())
            curr = current_operation(C)

        append_to_number(C, value)
    def handle_operation_button(C, op):
        curr = current_operation(C)
        prev = previous_operation(C)

        if (curr.rq_op == " " and is_current_valid(C)) or C.greyed_out:
            curr.rq_op = op
        elif curr.rq_op == "×" and op == "×":
            curr.rq_op = "^"
        elif op == "-":
            handle_number_button(C, "-")
        else:
            C.question_mark = "?"
    def handle_bracket_button(C):
        curr = current_operation(C)
        prev = previous_operation(C)
        
        C.greyed_out = False
        
        if curr.rq_op != " ":
            curr.bracket = "(" if curr.bracket == " " else " "
        else:
            if prev.stub:
                C.question_mark = "?"
            else:
                prev.bracket = "(" if prev.bracket == " " else " "

    def handle_button_press(C, text):
        C.question_mark = " "

        if text == "=":
            handle_equals_button(C)
        elif text == "DEL":
            handle_del_button(C)
        else:
            if C.greyed_out:
                handle_clr_button(C)
            
            if text == "CLR":
                handle_clr_button(C)
            elif text in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "/", ".", "Ans", "B", "C"}:
                handle_number_button(C, text[0])
            elif text in {"+", "-", "×", "÷"}:
                handle_operation_button(C, text)
            elif text == "(":
                handle_bracket_button(C)
            else:
                C.question_mark = "?"
                pass
            C.greyed_out = False

        update_display(C)
    def switch_precision(C, switch):
        C.precision = 2 * int(switch)
        update_display(C)
    def switch_fraction(C, switch):
        C.fraction_style = int(switch)
        update_display(C)



    if run_tests:
        test_result = "["
        def test(in_sequence, output):
            nonlocal test_result

            # Test Context
            TC = Context()

            try:
                for key in in_sequence:
                    if key in "!@#$":
                        switch_precision(TC, " !@#$".index(key))
                    elif key in "%^":
                        switch_fraction(TC, " %^".index(key))
                    elif key in "Sdc*A":
                        key = {"S":"Sel", "d":"DEL", "c":"CLR", "*":"×", "A":"Ans"}[key]
                        handle_button_press(TC, key)
                    else:
                        handle_button_press(TC, key)
                result = update_display(TC, True)
                if result == output:
                    test_result += "-"
                else:
                    test_result += "/"
                    print(f"Fail \"{in_sequence}\":")
                    print(result.replace(" ", "`"))
                    print("Expected:")
                    print(output.replace(" ", "`"))
                    print("")
            except:
                test_result += "!"
                print(f"Fail \"{in_sequence}\":")
                print("Expected:")
                print(output.replace(" ", "`"))
                print("")

#   2 <!@#$> 8  1/2<%^>3/2
#   [S] [7] [8] [9] [d] [c]
#   [C] [4] [5] [6] [-] [*]
#   [B] [1] [2] [3] [+] [÷]
#   [A] [/] [0] [.] [(] [=]

        test("",            "                                  \n   ")
        test("$/6=",        "                                  \n   0.16666666")
        test("$/6=/",       "                                  \n   1/6")
        test("$1÷6=/",      "                                  \n   1/6")
        test("%/3=/",       "                                  \n   1/3")
        test("/2+0=",       "   1/2                            \n+  0")
        test("/2+0=cA/",    "                                  \n   0.50")
        test("A5",          "                                 ?\n   0.00")
        test("/2=cA",       "                                  \n   1/2")
        test(".6900/",      "                                  \n   69/100")
        test("$.00000001/=","                                  \n   0.00000001")
        test("1+(2*",       "+( 2                              \n× ")
        test("1÷0+",        "   1                             ?\n÷  0")
        test("%2=/",        "                                  \n   2")
        test("@1.33//",     "                                  \n   1.33")
        test("@1/3=//",     "                                  \n   0.3333")
        test("0=/",         "                                  \n   0")

        print(test_result + "]")



    switch_row = tk.Frame(root)
    switch_row.pack(side="top", anchor="w")

    def create_switch(C, left_label, right_label, steps, command, default_value = 1):
        switch = tk.Frame(switch_row)
        label = tk.Label(switch, text=left_label, font=BUTTON_FONT)
        label.pack(side="left")
        label_width = label.winfo_reqwidth()
        scale = tk.Scale(
            switch,
            from_        = 1,
            to           = steps,
            orient       = "horizontal",
            length       = 20 * steps,
            width        = 20,
            sliderlength = 20,
            showvalue    = False,
            command      = lambda sw: command(C, sw)
        )
        scale.pack(side="left", padx=2, pady=1)
        scale.set(default_value)
        tk.Label(switch, text=right_label, font=BUTTON_FONT).pack(side="left")
        switch.pack(anchor="w", padx=50 - label_width, side="left")
    

    # Button layout: 4 rows of 6 buttons
    buttons = [
        ["Sel", "7" , "8" , "9" ,"DEL","CLR"],
        [ "C" , "4" , "5" , "6" , "-" , "×" ],
        [ "B" , "1" , "2" , "3" , "+" , "÷" ],
        ["Ans", "/" , "0" , "." , "(" , "=" ]
    ]

    # Button colors (same layout as buttons)
    button_colors = [
        ["blue", "gray", "gray", "gray",  "red" ,  "red" ],
        ["blue", "gray", "gray", "gray", "green", "green"],
        ["blue", "gray", "gray", "gray", "green", "green"],
        ["blue", "gray", "gray", "gray", "green", "green"]
    ]
    
    # Text color mapping (white for colored buttons, black for gray)
    text_color_map = {
        "red": "white",
        "green": "white",
        "blue": "white",
        "gray": "black"
    }
    
    # Pressed button colors (darker versions)
    pressed_color_map = {
        "red": "#cc0000",
        "green": "#cc9900",
        "blue": "#0066cc",
        "gray": "#b0b0b0"
    }

    create_switch(C, "2",   "8",   4, switch_precision, 2)
    create_switch(C, "1/2", "3/2", 2, switch_fraction, 1)
    for row_idx, row in enumerate(buttons):
        frame = tk.Frame(root)
        frame.pack(fill="both", expand=True, padx=1, pady=1)
        for col_idx, btn_text in enumerate(row):
            color_name = button_colors[row_idx][col_idx]
            btn = tk.Button(
                frame, text=btn_text, font=BUTTON_FONT, width=5, height=1,
                bg=color_name, fg=text_color_map[color_name],
                activebackground=pressed_color_map[color_name], activeforeground=text_color_map[color_name],
                command=lambda text=btn_text: handle_button_press(C, text)
            )
            btn.pack(side="left", padx=2, pady=1)

    update_display(C)

    window.title("Calculator")
    # Auto-size window to fit contents
    window.update_idletasks()
    window.geometry("")
    window.resizable(width=False, height=False)

    window.mainloop()

if __name__ == "__main__":
    main(True)