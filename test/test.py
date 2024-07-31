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

    # Helper function to display results
    def display_result(op_name):
        print(f"{op_name}: result = {dut.uo_out.value},  {dut.uio_out.value}")

    # Test ADD operation
    dut.ui_in.value = 0b0011_0101  # a = 1, b = 2
    dut.uio_in.value = 0b000       # opcode = ADD
    await Timer(10, units='ns')
    display_result("ADD")
    assert dut.uo_out.value == 0b00001000

    # Test SUB operation
    dut.ui_in.value = 0b0010_0001  # a = 2, b = 1
    dut.uio_in.value = 0b001       # opcode = SUB
    await Timer(10, units='ns')
    display_result("SUB")
    assert dut.uo_out.value == 0b00000001

    # Test MUL operation
    dut.ui_in.value = 0b0010_0011  # a = 2, b = 3
    dut.uio_in.value = 0b010       # opcode = MUL
    await Timer(10, units='ns')
    print(f"MUL: result = {dut.uo_out.value}")
    assert dut.uo_out.value == 0b00000110

    # Test DIV operation
    dut.ui_in.value = 0b0100_0010  # a = 4, b = 2
    dut.uio_in.value = 0b011       # opcode = DIV
    await Timer(10, units='ns')
    print(f"DIV: result = {dut.uo_out.value}")
    assert dut.uo_out.value == 0b00100000

    # Test AND operation
    dut.ui_in.value = 0b1100_1010  # a = 12, b = 10
    dut.uio_in.value = 0b100       # opcode = AND
    await Timer(10, units='ns')
    print(f"AND: result = {dut.uo_out.value}")
    assert dut.uo_out.value == 0b00001000

    # Test OR operation
    dut.ui_in.value = 0b1100_1010  # a = 12, b = 10
    dut.uio_in.value = 0b101       # opcode = OR
    await Timer(10, units='ns')
    print(f"OR: result = {dut.uo_out.value}")
    assert dut.uo_out.value == 0b00001110

    # Test XOR operation
    dut.ui_in.value = 0b1100_1010  # a = 12, b = 10
    dut.uio_in.value = 0b110       # opcode = XOR
    await Timer(10, units='ns')
    print(f"XOR: result = {dut.uo_out.value}")
    assert dut.uo_out.value == 0b00000110

    # Test NOT operation
    dut.ui_in.value = 0b1100_1010  # a = 12, b = ignored
    dut.uio_in.value = 0b111       # opcode = NOT
    await Timer(10, units='ns')
    print(f"NOT: result = {dut.uo_out.value}")
    assert dut.uo_out.value == 0b00000011
