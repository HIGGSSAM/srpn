"""
Saturated Reverse Polish Notation Calculator

Description
-----------
The script takes input from STDIN and displays results via STDOUT.

In reverse Polish notation, the operators follow their operands;
for instance, to add 3 and 4 together, one would write 3 4 +
rather than 3 + 4.

For background on RPN see:
https://en.wikipedia.org/wiki/Reverse_Polish_notation 

Functions
---------
append_stack(float(number))  
check_saturation(float(number))
process_octal_number(str(number_str))
process_number(str(number_str))
display_stack()
process_equals()
process_rand_number(str(rand_number_str))
process_arithmetic_operator(str(operator))
op_precedence_change(str(current_op), str(previous_op))
parse_comment(str(command), int(command_index), 
    boolean(comment_flag) str(comment_string)) 
parse_number(str(command), int(command_index))
parse_command_line(str(command))
process_command(str(command))

Misc Variables
--------------
stack = []
program_status = [int(random_index), 
    boolean(multiline_comment_flag), str(previous_comment_string)]
"""

#               Python v3.8

#               Pylint instructions
# Disable the pylint errors from Black reformatting style on block indents
# ppylint: disable=C0330

# used to indicate variables that shouldn't be re-assigned
# ref: https://docs.python.org/3.8/library/typing.html
from typing import Final

# stack limit constant
stack_limit: Final = 23

# saturation constants
min_nr: Final = -2147483648
max_nr: Final = 2147483647

# command parsing token values
comment_token: Final = "<#>"
number_token: Final = "<n>"
rand_number_token: Final = "<r>"
octal_number_token: Final = "<o>"
valid_number_digits: Final = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "r",
]

# error message literals
unrecognised_op_msg: Final = 'Unrecognised operator or operand "%".\n'
stack_overflow_msg: Final = "Stack overflow.\n"
stack_empty_msg: Final = "Stack empty.\n"
stack_underflow_msg: Final = "Stack underflow.\n"
zero_divide_msg: Final = "Divide by 0.\n"
negative_power_msg: Final = "Negative power.\n"

arithmetic_operators: Final = ["-", "+", "*", "/", "%", "^"]
equals_operator: Final = "="
rand_number_operator: Final = "r"
display_stack_operator: Final = "d"
comment_operator: Final = "#"

# psuedo random numbers returned in sequence with <r> operator
random_number: Final = [
    1804289383,
    846930886,
    1681692777,
    1714636915,
    1957747793,
    424238335,
    719885386,
    1649760492,
    596516649,
    1189641421,
    1025202362,
    1350490027,
    783368690,
    1102520059,
    2044897763,
    1967513926,
    1365180540,
    1540383426,
    304089172,
    1303455736,
    35005211,
    521595368,
    1804289383,
]

#               define global variables
# LIFO list containing valid integer (base 10) numbers in string format
stack = []

# contains program status settings:
program_status = [0, False, ""]

# constants to access each status setting
#   [0] is random number index value, default=0
random_index: Final = 0
#   [1] is multiline comment flag, default=False
multiline_comment_flag: Final = 1
#   [2] is multiline comment string, default =""
previous_comment_string: Final = 2


#                               SRPN def's
def append_stack(number):
    """
    <number> = float value

    Checks if stack will overflow otherwise appends <number> to stack
    as string value

    Returns: <string> empty or contains "Error message"
    """
    # check if adding number would overflow the stack
    if len(stack) + 1 > stack_limit:
        return stack_overflow_msg

    # stack.append(str(number))
    stack.append(number)
    return ""


def check_saturation(number):
    """
    <number> = <int or float value>

    Checks values fall in the range -2,147,483,648 <= x =<  2,147,483,647
    otherwise sets <number> to boundary value

    Returns: <number>
    """

    if number < 0:
        return max(number, min_nr)

    return min(number, max_nr)


def process_octal_number(number_str):
    """
    <number> = Str value

    Check <number> in non decimal base format and converts
    to decimal (base 10) value

    For an Octal format number, i.e. leading zero(s) and
    all digits less than 7. E.g. 01101 is 557 in decimal or
    -01101 which -557
    If its an illegal Octal value eg has 8 or 9 digits then
    return None

    """
    oCtal = ""

    # check for illegal digits for Octal number
    for x in ["8", "9"]:
        if number_str.count(x):
            return None

    # replace leading zero with 0o to signal
    # python this is Octal value
    if number_str.startswith("0"):
        oCtal = "0o" + number_str[1:]
    elif number_str.startswith("-0"):
        oCtal = "-0o" + number_str[2:]
    else:
        return None

    # return Octal value converted to decimal
    return append_stack(check_saturation(int(oCtal, base=8)))


def process_number(number_str):
    """
    <number> = string NUMBER value

    Pushes the number onto the stack, first checking for number saturation,
    and stack overflow situation

    Returns: <string> empty or contains "Error message"
    """

    try:
        # append value to stack retaining float accuracy
        return append_stack(check_saturation(float(number_str)))
    except:
        return ""


def display_stack():
    """
    Concatentates stack values with '\\n' delimiters
    trailing each item into a string value

    Returns: <string> or '-2147483648' if stack is empty
    """
    return_value = ""

    if len(stack) == 0:
        return_value = str(min_nr) + "\n"
    else:
        # insert newline control between stack entries
        # and convert to INT to format correctly on output
        for item in stack:
            return_value += str(int(float(item))) + "\n"

    return return_value


def process_equals():
    """
    Copies last stack value into string with trailing '\\n'

    Returns: <string> or error message if stack is empty
    """

    if len(stack) == 0:
        return stack_empty_msg

    # insert newline control between stack entries
    # and convert to INT to format correctly on output
    return str(int(float(stack[-1]))) + "\n"


def process_rand_number(rand_number_str):
    """
    Arg:
    <rand_number_str>  = string with rand nr command. Used to
    check for leading '-'

    Adds the next random number in sequence from a list of pseudo
    random numbers to the stack.

    Numbers wrap around after the stack limit is reach starting from the
    begining of the list again

    Returns: <string> empty or contains "Error message"
    """
    # identify index as global variable so can be updated
    index = program_status[random_index]

    return_value = ""
    # get index to next number
    rand_number = random_number[index]

    # check if need to negate number
    if rand_number_str.startswith("-"):
        rand_number *= -1

    return_value = str(append_stack(rand_number))

    # if apppend has been successful increment random number index
    if return_value == "":
        index += 1
        # reset to 0 if beyond stack limit
        if index > stack_limit:
            index = 0
        # save incremented index
        program_status[random_index] = index

    return return_value


def process_arithmetic_operator(operator):
    """
    <operator> = valid arithmetic operators: +, -, /, *, ^, %

    Pops the last two values off the stack[x, y] and
    pushes result of the corresponding operation onto the stack[]
    after checking for zero divide and saturation.   Maintains float
    values for calculation accuracy

    Returns: <string> empty or contains "Error message"
    """
    try:
        return_value = ""
        x = 0  # first operand
        y = 0  # second operand

        # exit with error message if less than 2
        # numbers on the stack
        if len(stack) < 2:
            return stack_underflow_msg
        # check for divide by zero error first
        if operator in ["/", "%"] and float(stack[-1]) == 0:
            return zero_divide_msg
        # only if y is positive do we perform calculation
        if operator == "^" and float(stack[-1]) < 1:
            return negative_power_msg

        # perform calculations on last two numbers on stack
        y = float(stack.pop())
        x = float(stack.pop())

        if operator == "+":
            append_stack(check_saturation(x + y))

        elif operator == "-":
            append_stack(check_saturation(x - y))

        elif operator == "*":
            append_stack(check_saturation(x * y))

        elif operator == "/":
            append_stack(check_saturation(x / y))

        elif operator == "^":
            append_stack(check_saturation(x ** y))

        elif operator == "%":
            append_stack(check_saturation(x % y))

        return return_value

    except ZeroDivisionError:
        return zero_divide_msg


def op_precedence_change(current_op, previous_op):
    """
    Arg:
    <current_op> str = current arithmetic operator
    <previous_op> str = previous arithmetic operator

    Checks order of operations:
    1. exponentiation and root extraction   --> highest
    2. multiplication and division
    3. addition and subtraction             --> lowest

    and if changes down a level ie from 1 (^) to 2 (*) or 3 (+) returns
    <level_change> as True, otherwise False

    """
    level_change = False

    #
    if previous_op == current_op:
        return level_change

    level_1 = ["^"]
    level_2 = ["*", "/", "%"]
    # level_3=["-","+"]

    current_op_level = 0
    previous_op_level = 0

    if current_op in level_1:
        current_op_level = 1
    elif current_op in level_2:
        current_op_level = 2
    else:
        current_op_level = 3

    if previous_op in level_1:
        previous_op_level = 1
    elif previous_op in level_2:
        previous_op_level = 2
    else:
        previous_op_level = 3

    if previous_op_level < current_op_level:
        level_change = True

    return level_change


def parse_comment(command, command_index, comment_flag, comment_string):
    """
    Args:
    <command> (str) = input line being parsed,
    <command_index> (int) = current character position,
    <comment_flag> (bool) = True indicating aready inside a comment string,
    <comment_string> (str) = unclosed comment substring

    Checks at current character position for valid comment delimiter " # ",
    or "# " / " #" if at the start or end of the command input.

    If <comment_flag>=True appends all characters up to and including any
    valid # found or the rest of the input line to <command_string>. Sets
    <command_index> to the next following character position to continue
    general parsing from.

    If <comment_flag>=True and closing comment delimter found resets
    <comment_flag>=False to indicate now outside of the comment.

    <comment_index> is set to -1 if no comment found

    Returns:
        <comment_flag> (bool),
        <command_index> (int)   = position of last character parsed,
        <comment_string> (str),

    """
    # test if comments potentially present in command
    if (
        comment_flag is False
        and command[command_index : command_index + len(comment_operator)]
        != comment_operator
    ):
        command_index = -1
        return comment_flag, command_index, comment_string

    # Test if already parsing inside a comment still open from a previous
    # <command> input
    # -------------------------------------------------------------------

    if comment_flag is True:
        # locate end comment delimiter and return all characters
        # upto and including "#" & appended to <comment_string>. If no #
        # found appends the remainder of <command> string from
        # current <command_index> position

        # check when at of start of <command> for comment delimiter
        if command_index == 0 and (
            command == comment_operator
            or command.startswith(comment_operator + " ")
        ):
            # found so indicate now at end of comment and
            # move parser to last charactero f "# "
            command_index = len(comment_operator)
            comment_flag = False

        # check mid line comment delimter (i contains start position if found)
        elif command.find(" " + comment_operator + " ", command_index) > 0:
            # found so add substring from current <comment_index>
            # up to and including ' #' move parser index to last
            # character of " # ". i = char position at start of search pattern
            i = command.find(" " + comment_operator + " ", command_index)
            # ensures trailing delimiter included
            comment_string += command[
                command_index : i + len(comment_operator) + 1
            ]
            command_index = i + len(comment_operator)
            comment_flag = False

        # check for end of line #
        elif command.endswith(" " + comment_operator) is True:
            # found so add substring from current <comment_index>
            # up to and including '#' move parser index to end of
            # <command> string
            comment_string += command[command_index:]
            command_index = len(command)
            comment_flag = False
        else:
            # if no # found then append remainder of <command> to comment_string
            # NB remainder of <command> used since there may have been more
            # than 1 comment on the same line,
            # e.g. '... # comment # ... # comment #'
            comment_string += command[command_index:]
            command_index = len(command)
            comment_flag = True

        # return with updated values
        return comment_flag, command_index, comment_string

    # test for the start of a new comment at <command_index>
    # ------------------------------------------------------

    # check when at the of start of <command> for comment delimiter
    if command_index == 0 and (
        command == comment_operator
        or command.startswith(comment_operator + " ")
    ):
        # found so indicate now at start of comment and
        # move parser to last character of "# "
        command_index = len(comment_operator)
        comment_flag = True

    # check for mid line comment delimiter
    elif (
        command[command_index - 1 : command_index + 2]
        == " " + comment_operator + " "
    ):
        # found so indicate now at start of comment and
        # move parser to last character of " # "
        command_index = command_index + len(comment_operator)  # - 1
        comment_flag = True

    # check for end of line #
    elif (
        command_index == len(command)
        and command.endswith(" " + comment_operator) is True
    ):
        # found so add substring from current <comment_index>
        # up to and including '#' move parser index to end of
        # <command> string
        command_index = command_index + len(comment_operator)  # - 1
        comment_flag = True

    if comment_flag is True:
        comment_string = comment_token + comment_operator + " "
    else:
        # arriving here means no comment found so set index to -1
        command_index = -1

    return comment_flag, command_index, comment_string


def parse_number(command, command_index):
    """
    Args:
    <command> (str) = input line being parsed,
    <command_index> (int) = current character position,

    Checks at current character position for valid number with
    or without leading '-' sign and returns values in <number_string>.

    character 'r' is treated as special case representing psuedo random number
    which can also have a leading '-' sign

    NOTE: this only handles digit strings not floats, hex, binary
    or Octal syntax (apart from older style Octal form i.e. 011)

    <comment_index> is set to -1 if no comment found

    Returns:
        <command_index> (int)  = position of last character parsed,
        <number_string> (str)

    """
    increment = 0
    number_string = ""
    isRandNum = False

    # if - sign but no following digit or prev char is digit then return
    # if (
    #    command[command_index : command_index + 1] == "-"
    #    and (
    #        command[command_index + 1 : command_index + 2]
    #        not in valid_number_digits
    #    )
    #    or (command[command_index - 1 : command_index] in valid_number_digits)
    #:

    #   return -1, ""

    # check first for leading minus sign which true if
    # next character after is a <valid_number_digit> and
    # previous character isn't in <valid_number_digit>
    if (
        command[command_index : command_index + 1] == "-"
        and (
            command[command_index + 1 : command_index + 2]
            in valid_number_digits
        )
        and (
            command[command_index - 1 : command_index]
            not in valid_number_digits
        )
    ):
        # add the leading minus sign
        number_string = "-"
        # position to next digit
        increment += 1

    if (
        # next character is digit or 'r' (increment=1 if a leading - sign)
        (
            command[command_index + increment : command_index + increment + 1]
            in valid_number_digits
        )
        # and previous character was NOT a digit
        and command[command_index - 1 : command_index]
        not in valid_number_digits
    ):
        # get rest of digits
        i = command_index + increment

        if (
            command[command_index + increment : command_index + increment + 1]
            == rand_number_operator
        ):
            number_string += rand_number_operator
            isRandNum = True
            # position at next char after r
            increment += 1
        else:
            # loop until end of digits
            while i != -1:
                if command[i : i + 1].isdigit() is True:
                    number_string += command[i : i + 1]
                    increment += 1
                    i += 1
                else:
                    i = -1

    if number_string == "":
        # arriving here means no number found so set index to -1
        command_index = -1
    else:
        # test for Octal format number with more than one digit
        # and leading 0 or -0.
        # Validation of octal held until later in the process
        if (number_string.startswith("0") and len(number_string) > 1) or (
            number_string.startswith("-0") and len(number_string) > 2
        ):
            number_string = octal_number_token + number_string
        elif isRandNum:
            number_string = rand_number_token + number_string
        else:
            number_string = number_token + number_string
        # return position of last character parsed
        command_index += increment - 1

    return command_index, number_string


def parse_command_line(command):
    """
    <command> = STR value containing input command(s)

    Performs lexical analysis of <command> string returning list of operators
    and operands.  Operators are defined as any single character, with no
    validity checking performed. Operands are integer numbers.

    Returns: sequenced Tuple List[] containing parsed operands and operators
    as Str values.  Comment delimiters are returned as token "<#>"

    Special treatment to mimic the existing sprn program:
    -----------------------------------------------------

    Numbers input in a compact algebraic notation e.g. "2+2", "2/2^2" will
    be converted into the rpn notation equivalent with in immediate evaluation
    after each change of operand e.g. 2 2 + = ,  2 2 / = 2 ^ =
    *** CHECK += -+ SYNTAX

    """
    # set comment status from preceding input. <comment_flag> = True
    # indicates parsing an unclosed commment string
    comment_flag = program_status[multiline_comment_flag]
    comment_string = program_status[previous_comment_string]

    # define local variables
    command_tokens = []
    arithmetic_op_buffer = []
    increment = 0

    try:
        # if <comment_string> not empty then add \\n character to
        # display comment over multiple lines
        if comment_string:
            comment_string += "\\n"

        # loop through each character in command string
        # and build rpn tokens.Starting -1 allows end of command
        # string to be actioned before exiting while loop
        i = -1
        while i <= len(command) - 1:
            # move to and extract into s the next character
            i += 1
            s = command[i : i + 1]

            #       Parse Comment delimiter
            #       -----------------------
            #   *** THIS TEST MUST GO FIRST in parsing sequence to
            #       avoid operators and operands inside comment strings
            #       spanning multiple command lines being parsed !

            # test to see if comment or possible comment when s is not empty
            # but always parse text if already inside a delimited comment
            # or outside and s is the comment operator

            if s and (
                comment_flag is True
                or (
                    comment_flag is False
                    and command[i : i + len(comment_operator)]
                    == comment_operator
                )
            ):

                # check for comment strings delimited by " # " - with no
                # leading/trailing space if this occurs at the start/end
                # of the <command>
                comment_flag, increment, comment_string = parse_comment(
                    command, i, comment_flag, comment_string
                )
                # check if comment found ie <increment> > 0
                # and move current command character index forward by
                # increment
                if increment > 0:
                    i = increment
                    # check if end of comment found and append to rpn tokens
                    if comment_flag is False:
                        command_tokens.append(comment_string)
                        # reinitialise comment_string variable
                        comment_string = ""
                else:
                    # arrive here then comment token not passing delimiter
                    # tests so add to <rpn_tokens>
                    command_tokens += arithmetic_op_buffer[::-1]
                    arithmetic_op_buffer = []
                    command_tokens.append(s)

            #       Flush arithmetic_op_buffer when space or end of line
            #       or preceeding op of higher and this one was lower
            #       ----------------------------------------------------
            elif s.isspace() is True or not s:
                # if <arithmetic_op_buffer> not empty then appended to
                # rpn token list in reversed in order
                if arithmetic_op_buffer:
                    command_tokens += arithmetic_op_buffer[::-1]
                arithmetic_op_buffer = []

                # ignore the space character and skip to next in command
                # continue

            #       Parse number strings
            #       --------------------

            # test to see if number when s is not empty or a space character
            # and is a digit or possible digit then get number string
            elif (s or s.isspace()) and (
                (s in valid_number_digits)
                or (
                    s == "-"
                    and (
                        (command[i + 1 : i + 2] in valid_number_digits)
                        or (command[i - 1 : i] not in valid_number_digits)
                    )
                )
            ):
                increment, number_string = parse_number(command, i)

                # if number found ie <increment> => 0 (nb 0 is the first
                # char position) then move current command character index
                # forward by increment
                if increment >= 0:
                    i = increment
                    # append number to rpn to token
                    command_tokens.append(number_string)
                    # continue
                else:
                    # not a number so add char to token list
                    arithmetic_op_buffer.append(s)

            #       Parse 'compact' arithmetic expressions
            #       --------------------------------------
            # where no spaces between operators and operands,
            # e.g. sequences like: 1+1=+2, or ++1-2= or 1+=

            elif s in arithmetic_operators:
                # get the previous operator or use lowest arithmetic
                # operator as default
                last_op = ""
                if len(arithmetic_op_buffer) == 0:
                    last_op = "+"
                else:
                    last_op = arithmetic_op_buffer[-1]

                # test for next char being space or end of line or
                # an op with lower arithmetic procedence
                if (
                    command[i + 1 : i + 2].isspace()
                    or len(command[i + 1 : i + 2]) == 0
                    or op_precedence_change(s, last_op)
                ):
                    # if any above true then flush the buffer
                    command_tokens += arithmetic_op_buffer[::-1]
                    arithmetic_op_buffer = []
                    arithmetic_op_buffer.append(s)
                else:
                    # append current op to buffer
                    arithmetic_op_buffer.append(s)

                # continue

            #       Non space character (not in above tests)
            #       ----------------------------------------
            elif s.isspace() is not True:
                # append non space character in s to rpn_tokens list
                command_tokens.append(s)

        # after parsing command elements pass back
        # to caller tokenized input command string and update
        # program status settings
        program_status[multiline_comment_flag] = comment_flag
        program_status[previous_comment_string] = comment_string
        return command_tokens

    except:
        return ""


def process_command(command):
    """
     Saturated Reverse Polish Notation Calculator (RPNC)
     Implements a simple integer arithmetic calculator.

     RPNC operators and operands maybe passed either singlely or
     in any multiple instructions in the input command

     Saturated means no integer wrap around based on C style signed
     integers ie MAX 2,147,483,647 and MIN -2,147,483,648.

     Arithmetic operators supported:
       '+' addition,
       '-' subtraction,
       '*' multiplication,
       '/' integer division,
       '^' raise to power,
       '%' modulus
       '=' outputs result of last operator

    Special operators:
        'd' displays values on the stack,
        'r' inserts a random value based on C rand(),
        comments '# this is a comment #' are ignored including over
        multiple lines

    Number stack arbitarily limited to 23.  A stack underflow causes
    implicit evaluate command ie =

    Numbers input in Octal (leading zero, and no digits > 7 ), e.g.
    0123 converts to 85 decimal (base 10) but from Python v3 must first be
    reformated as 0o123 to avoid syntax error

    Returns: <string> containing concatented list of display outputs
    """

    # define local def variables
    rpn_elements = []
    temp_element = []
    # buffer to hold all outputs generated from input command in
    # the FIFO sequence they are generated
    output_buffer = ""

    try:

        # parse the command line into operator and operands stream
        temp_element = parse_command_line(command)
        if len(temp_element) > 0:
            rpn_elements += temp_element

        # action operator and operands

        for s in rpn_elements:

            #       Comment handling
            #       ----------------
            # ignore comment tokens
            if s.startswith(comment_token) is True:
                continue

            #       Process Arithmetic operators
            #       ----------------------------
            if s in arithmetic_operators:  # ["+", "-", "*", "/", "^", "%"]:
                output_buffer += process_arithmetic_operator(s)
                continue

            #       Process numbers
            #       ---------------
            # if number formats like 0o11, 0b0101 or 0xAA were permitted
            # the is_int_str def would need modifying to recognise these
            if s.startswith(number_token) is True:
                output_buffer += process_number(s[len(number_token) :])
                continue

            #       Process random number
            #       ---------------------
            # deals with random number
            if s.startswith(rand_number_token) is True:
                output_buffer += process_rand_number(
                    s[len(rand_number_token) :]
                )
                continue

            #       Process Octal numbers
            #       ---------------------

            if s.startswith(octal_number_token) is True:
                output_buffer += process_octal_number(
                    s[len(octal_number_token) :]
                )
                continue

            #       Process Equals show last result operator
            #       ----------------------------------------
            # perform = which displays last number appended to the stack ****
            if s == "=":
                output_buffer += process_equals()
                continue

            #       Process "r" generate psuedo rand number operator
            #       ------------------------------------------------
            # perform = which displays last number appended to the stack
            if s.startswith(rand_number_token) is True:

                output_buffer += process_rand_number(s[len(number_token) :])
                continue

            #       Process "d" display stack operator
            #       ----------------------------------
            # special instruction d (must be lower case) = display stack
            if s == "d":
                output_buffer += display_stack()
                continue

            # if you reach here then it must be an illegal operator
            output_buffer += unrecognised_op_msg.replace("%", s)

        # return outputs as concatented string, stripping last trailing \n
        return output_buffer[:-1]

    except:
        # return outputs as concatented string, stripping last trailing \n
        return output_buffer[:-1]


# Disable the pylint errors from this code below
# pylint: disable=bare-except
# pylint: disable=consider-using-sys-exit

# This is the entry point for the program.
# Do not edit the below
if __name__ == "__main__":
    while True:
        try:
            cmd = input()
            pc = process_command(cmd)
            # if pc != None:
            if pc != "":
                print(str(pc))
        # except:
        #    exit()
        except EOFError:
            exit()
        except KeyboardInterrupt:
            print("signal: interrupt")
            exit()
