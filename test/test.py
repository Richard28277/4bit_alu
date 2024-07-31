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

    test_cases = [
        {'ui_in': 0b00110101, 'uio_in': 0b00000000, 'expected_uo_out': 0b00001000, 'expected_overflow': 1, 'expected_carry_out': 0}, # ADD
        {'ui_in': 0b00110101, 'uio_in': 0b00000001, 'expected_uo_out': 0b00001110, 'expected_overflow': 0, 'expected_carry_out': 0}, # SUB
        {'ui_in': 0b00110101, 'uio_in': 0b00000010, 'expected_uo_out': 0b00001111, 'expected_overflow': 0, 'expected_carry_out': 0}, # MUL
        {'ui_in': 0b00110101, 'uio_in': 0b00000011, 'expected_uo_out': 0b00110000, 'expected_overflow': 0, 'expected_carry_out': 0}, # DIV
        {'ui_in': 0b00110101, 'uio_in': 0b00000100, 'expected_uo_out': 0b00000001, 'expected_overflow': 0, 'expected_carry_out': 0}, # AND
        {'ui_in': 0b00110101, 'uio_in': 0b00000101, 'expected_uo_out': 0b00000111, 'expected_overflow': 0, 'expected_carry_out': 0}, # OR
        {'ui_in': 0b00110101, 'uio_in': 0b00000110, 'expected_uo_out': 0b00000110, 'expected_overflow': 0, 'expected_carry_out': 0}, # XOR
        {'ui_in': 0b00110101, 'uio_in': 0b00000111, 'expected_uo_out': 0b00001100, 'expected_overflow': 0, 'expected_carry_out': 0}  # NOT
    ]

    for case in test_cases:
        dut.ui_in.value = case['ui_in']
        dut.uio_in.value = case['uio_in']

        # Wait for one clock cycle to see the output values
        await ClockCycles(dut.clk, 1)

        # Check the output values
        assert dut.uo_out.value == case['expected_uo_out'], f"Test failed for uio_in={case['uio_in']}: expected {case['expected_uo_out']} but got {dut.uo_out.value}"
        assert dut.uio_out[7].value == case['expected_overflow'], f"Test failed for uio_in={case['uio_in']}: expected overflow {case['expected_overflow']} but got {dut.uio_out[7].value}"
        assert dut.uio_out[6].value == case['expected_carry_out'], f"Test failed for uio_in={case['uio_in']}: expected carry_out {case['expected_carry_out']} but got {dut.uio_out[6].value}"

    dut._log.info("All tests passed")
