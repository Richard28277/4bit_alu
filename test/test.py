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
        assert dut.uio_out.value & 0x80 == (expected_overflow << 7), f"Expected overflow: {expected_overflow}, got: {dut.uio_out.value & 0x80}"
        assert dut.uio_out.value & 0x40 == (expected_carry << 6), f"Expected carry: {expected_carry}, got: {dut.uio_out.value & 0x40}"

    # Testing ADD operation
    await perform_test(a=5, b=10, opcode=0b000, expected_result=15, expected_carry=0, expected_overflow=0)

    # Testing SUB operation
    await perform_test(a=15, b=5, opcode=0b001, expected_result=10, expected_carry=1, expected_overflow=0)

    # Testing MUL operation
    await perform_test(a=2, b=3, opcode=0b010, expected_result=6, expected_carry=0, expected_overflow=0)

    # Testing DIV operation (quotient 2, remainder 1)
    await perform_test(a=9, b=4, opcode=0b011, expected_result=(1 << 4) | 2, expected_carry=0, expected_overflow=0)

    # Testing AND operation
    await perform_test(a=6, b=3, opcode=0b100, expected_result=0b00000010, expected_carry=0, expected_overflow=0)

    # Testing OR operation
    await perform_test(a=6, b=3, opcode=0b101, expected_result=0b00000111, expected_carry=0, expected_overflow=0)

    # Testing XOR operation
    await perform_test(a=6, b=3, opcode=0b110, expected_result=0b00000101, expected_carry=0, expected_overflow=0)

    # Testing NOT operation (unary operation, only uses 'a')
    await perform_test(a=6, b=0, opcode=0b111, expected_result=0b00001001, expected_carry=0, expected_overflow=0)

    dut._log.info("All tests passed")
