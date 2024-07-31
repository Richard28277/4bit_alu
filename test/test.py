import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

@cocotb.test()
async def test_tt_um_Richard28277(dut):
    # Clock generation
    cocotb.start_soon(Clock(dut.clk, 10, units='ns').start())

    # Initialize Inputs
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.ena.value = 1
    dut.rst_n.value = 0

    # Wait for global reset
    await Timer(10, units='ns')
    dut.rst_n.value = 1

    # Helper function to check results
    async def check_result(op_name, expected_value):
        await Timer(10, units='ns')
        actual_value = dut.uo_out.value
        if actual_value != expected_value:
            raise AssertionError(f"{op_name}: Expected result = {expected_value}, but got {actual_value}")

    # Test ADD operation
    dut.ui_in.value = 0b0011_0101  # a = 1, b = 2
    dut.uio_in.value = 0b000       # opcode = ADD
    await check_result("ADD", 00001000)  # Adjust expected value based on ADD operation

    # Test SUB operation
    dut.ui_in.value = 0b0010_0001  # a = 2, b = 1
    dut.uio_in.value = 0b001       # opcode = SUB
    await check_result("SUB", 00000001)  # Adjust expected value based on SUB operation

    # Test MUL operation
    dut.ui_in.value = 0b0010_0011  # a = 2, b = 3
    dut.uio_in.value = 0b010       # opcode = MUL
    await check_result("MUL", 00000110)  # Adjust expected value based on MUL operation

    # Test DIV operation
    dut.ui_in.value = 0b0100_0010  # a = 4, b = 2
    dut.uio_in.value = 0b011       # opcode = DIV
    await check_result("DIV", 00000010)  # Adjust expected value based on DIV operation

    # Test AND operation
    dut.ui_in.value = 0b1100_1010  # a = 12, b = 10
    dut.uio_in.value = 0b100       # opcode = AND
    await check_result("AND", 00001000)  # Adjust expected value based on AND operation

    # Test OR operation
    dut.ui_in.value = 0b1100_1010  # a = 12, b = 10
    dut.uio_in.value = 0b101       # opcode = OR
    await check_result("OR",00001110)  # Adjust expected value based on OR operation

    # Test XOR operation
    dut.ui_in.value = 0b1100_1010  # a = 12, b = 10
    dut.uio_in.value = 0b110       # opcode = XOR
    await check_result("XOR", 00000110)  # Adjust expected value based on XOR operation

    # Test NOT operation
    dut.ui_in.value = 0b1100_1010  # a = 12, b = ignored
    dut.uio_in.value = 0b111       # opcode = NOT
    await check_result("NOT", 00000011)  # Adjust expected value based on NOT operation
