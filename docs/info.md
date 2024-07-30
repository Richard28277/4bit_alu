# Project Datasheet: 4-Bit ALU
## Overview
The `4-Bit ALU` module is a digital system that performs various arithmetic and logical operations based on the input provided. It operates on 4-bit binary numbers and supports operations such as addition, subtraction, multiplication, division, logical AND, OR, XOR, and NOT.
## How it works
The module takes in two 4-bit binary numbers, `a` and `b`, and an operation code (`opcode`) that determines the operation to be performed. The operation results are then output through the `uo_out` wire, while additional status information such as carry out and overflow is output through the `uio_out` wire. The `uio_oe` wire is used to enable or disable the input/output functionality of the `uio_in` and `uio_out` wires.

- **ADD**: Adds `a` and `b`, producing a 4-bit result and a carry out.
- **SUB**: Subtracts `b` from `a`, producing a 4-bit result and a borrow indication.
- **MUL**: Multiplies `a` and `b`, producing an 8-bit result.
- **DIV**: Divides `a` by `b`, producing a 4-bit quotient and remainder. Division by zero is handled by returning a zero result.
- **AND, OR, XOR, NOT**: Performs the respective logical operation on `a` and `b`.
The results and status bits are then output accordingly.
## How to test
To test the `4 bit ALU` module, follow these steps:
1. Connect the `ui_in` wire to the 4-bit inputs `a` and `b`.
2. Connect the `uio_in` wire to the 3-bit `opcode`.
3. Connect the `uo_out` wire to an 8-bit output display or register to observe the operation result.
4. Connect the `uio_out` wire to observe the carry out and overflow status.
5. Ensure the `ena` signal is active (high).
6. Provide a clock signal to the `clk` input.
7. Optionally, use the `rst_n` signal to reset the module by pulling it low.
8. Cycle through various `opcode` values and corresponding `a` and `b` inputs to verify the correct operation of the module.
## External hardware
No external hardware is required for the basic operation of the `4 bit ALU` module. However, for testing and observation purposes, you may need:
- An 8-bit display or register to observe the `uo_out` output.
- Logic analyzers or oscilloscopes to monitor the `clk`, `rst_n`, and status signals.
