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
        await RisingEdge(dut.clk)
        actual_value = dut.uo_out.value
        # Convert expected_value and actual_value to binary strings for comparison
        expected_bin = f"{expected_value:04b}"
        actual_bin = actual_value.binstr.zfill(4)  # Ensure 4-bit width
        print(f"{op_name} - Expected: {expected_bin}, Actual: {actual_bin}")
        if actual_bin != expected_bin:
            raise AssertionError(f"{op_name}: Expected result = {expected_bin}, but got {actual_bin}")

    # Test ADD operation
    dut.ui_in.value = 0b0011_0101  # a = 53, b = 2
    dut.uio_in.value = 0b000       # opcode = ADD
    print(f"ADD - ui_in: {dut.ui_in.value}, uio_in: {dut.uio_in.value}, uo_out: {dut.uo_out.value}")
    await check_result("ADD", 0b0011_0110)  # 53 + 2 = 55 (binary 0011 0110)
    

    # Test SUB operation
    dut.ui_in.value = 0b0010_0001  # a = 33, b = 1
    dut.uio_in.value = 0b001       # opcode = SUB
    await check_result("SUB", 0b0010_0000)  # 33 - 1 = 32 (binary 0010 0000)

    # Test MUL operation
    dut.ui_in.value = 0b0010_0011  # a = 35, b = 3
    dut.uio_in.value = 0b010       # opcode = MUL
    await check_result("MUL", 0b0101_1011)  # 35 * 3 = 105 (binary 0101 1011)

    # Test DIV operation
    dut.ui_in.value = 0b0100_0010  # a = 66, b = 2
    dut.uio_in.value = 0b011       # opcode = DIV
    await check_result("DIV", 0b0010_0010)  # 66 // 2 = 33 (binary 0010 0010)

    # Test AND operation
    dut.ui_in.value = 0b1100_1010  # a = 202, b = 10
    dut.uio_in.value = 0b100       # opcode = AND
    await check_result("AND", 0b1100_0010)  # 202 & 10 = 2 (binary 1100 0010)

    # Test OR operation
    dut.ui_in.value = 0b1100_1010  # a = 202, b = 10
    dut.uio_in.value = 0b101       # opcode = OR
    await check_result("OR", 0b1100_1110)  # 202 | 10 = 206 (binary 1100 1110)

    # Test XOR operation
    dut.ui_in.value = 0b1100_1010  # a = 202, b = 10
    dut.uio_in.value = 0b110       # opcode = XOR
    await check_result("XOR", 0b1100_1110)  # 202 ^ 10 = 206 (binary 1100 1110)

    # Test NOT operation
    dut.ui_in.value = 0b1100_1010  # a = 202, b = ignored
    dut.uio_in.value = 0b111       # opcode = NOT
    await check_result("NOT", 0b0011_0101)  # ~202 = 53 (binary 0011 0101)
