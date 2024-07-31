# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Helper function to perform a test
    async def perform_test(a, b, opcode, expected_result, expected_carry, expected_overflow):
        dut.ui_in.value = (a << 4) | b
        dut.uio_in.value = opcode
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == expected_result, f"Expected result: {expected_result}, got: {dut.uo_out.value}"
        assert (dut.uio_out.value >> 7) & 1 == expected_overflow, f"Expected overflow: {expected_overflow}, got: {(dut.uio_out.value >> 7) & 1}"
        assert (dut.uio_out.value >> 6) & 1 == expected_carry, f"Expected carry: {expected_carry}, got: {(dut.uio_out.value >> 6) & 1}"

    # Testing ADD operation
    await perform_test(a=0b0011, b=0b0101, opcode=0b000, expected_result=0b00001000, expected_carry=0, expected_overflow=1)

    # Testing SUB operation
    await perform_test(a=0b0011, b=0b0101, opcode=0b001, expected_result=0b00001110, expected_carry=0, expected_overflow=0)

    # Testing MUL operation
    await perform_test(a=0b0011, b=0b0101, opcode=0b010, expected_result=0b00001111, expected_carry=0, expected_overflow=0)

    # Testing DIV operation (quotient 2, remainder 1)
    await perform_test(a=0b0011, b=0b0101, opcode=0b011, expected_result=0b00110000, expected_carry=0, expected_overflow=0)

    # Testing AND operation
    await perform_test(a=0b0011, b=0b0101, opcode=0b100, expected_result=0b00000001, expected_carry=0, expected_overflow=0)

    # Testing OR operation
    await perform_test(a=0b0011, b=0b0101, opcode=0b101, expected_result=0b00000111, expected_carry=0, expected_overflow=0)

    # Testing XOR operation
    await perform_test(a=0b0011, b=0b0101, opcode=0b110, expected_result=0b00000110, expected_carry=0, expected_overflow=0)

    # Testing NOT operation (unary operation, only uses 'a')
    await perform_test(a=0b0011, b=0b0101, opcode=0b111, expected_result=0b00001100, expected_carry=0, expected_overflow=0)

    dut._log.info("All tests passed")
