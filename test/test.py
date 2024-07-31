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
        print(f"{op_name} - ui_in: {dut.ui_in.value}, uio_in: {dut.uio_in.value}, uo_out: {dut.uo_out.value}")

    # Helper function to check results
    async def check_result(op_name, expected_value):
        await Timer(10, units='ns')
        actual_value = dut.uo_out.value
        expected_bin = f"{expected_value:06b}"
        actual_bin = actual_value.binstr.zfill(6)
        print(f"{op_name} - Expected: {expected_bin}, Actual: {actual_bin}")
        if actual_bin != expected_bin:
            raise AssertionError(f"{op_name}: Expected result = {expected_bin}, but got {actual_bin}")

    # Test ADD operation
    dut.ui_in.value = 0b0011_0101  # a = 53, b = 2
    dut.uio_in.value = 0b000       # opcode = ADD
    await Timer(10, units='ns')
    display_result("ADD")
    await check_result("ADD", 0b0011_0110)  # Example expected value

    # Test SUB operation
    dut.ui_in.value = 0b0010_0001  # a = 2, b = 1
    dut.uio_in.value = 0b001       # opcode = SUB
    await Timer(10, units='ns')
    display_result("SUB")
    await check_result("SUB", 0b0000_0001)  # Example expected value

    # Test MUL operation
    dut.ui_in.value = 0b0010_0011  # a = 2, b = 3
    dut.uio_in.value = 0b010       # opcode = MUL
    await Timer(10, units='ns')
    display_result("MUL")
    await check_result("MUL", 0b0000_0110)  # Example expected value

    # Test DIV operation
    dut.ui_in.value = 0b0100_0010  # a = 4, b = 2
    dut.uio_in.value = 0b011       # opcode = DIV
    await Timer(10, units='ns')
    display_result("DIV")
    await check_result("DIV", 0b0000_0010)  # Example expected value

    # Test AND operation
    dut.ui_in.value = 0b1100_1010  # a = 12, b = 10
    dut.uio_in.value = 0b100       # opcode = AND
    await Timer(10, units='ns')
    display_result("AND")
    await check_result("AND", 0b0000_1000)  # Example expected value

    # Test OR operation
    dut.ui_in.value = 0b1100_1010  # a = 12, b = 10
    dut.uio_in.value = 0b101       # opcode = OR
    await Timer(10, units='ns')
    display_result("OR")
    await check_result("OR", 0b0000_1110)  # Example expected value

    # Test XOR operation
    dut.ui_in.value = 0b1100_1010  # a = 12, b = 10
    dut.uio_in.value = 0b110       # opcode = XOR
    await Timer(10, units='ns')
    display_result("XOR")
    await check_result("XOR", 0b0000_0110)  # Example expected value

    # Test NOT operation
    dut.ui_in.value = 0b1100_1010  # a = 12, b = ignored
    dut.uio_in.value = 0b111       # opcode = NOT
    await Timer(10, units='ns')
    display_result("NOT")
    await check_result("NOT", 0b0011_0101)  # Example expected value
