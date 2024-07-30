`default_nettype none

module tt_um_Richard28277 (
    input  wire [7:0] ui_in,    // Dedicated inputs (a and b)
    output wire [7:0] uo_out,   // Dedicated outputs (result)
    input  wire [7:0] uio_in,   // IOs: Input path (opcode)
    output wire [7:0] uio_out,  // IOs: Output path (carry_out, overflow)
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Operation encoding
    parameter ADD = 3'b000;
    parameter SUB = 3'b001;
    parameter MUL = 3'b010;
    parameter DIV = 3'b011;
    parameter AND = 3'b100; // Logical AND
    parameter OR  = 3'b101; // Logical OR
    parameter XOR = 3'b110; // Logical XOR
    parameter NOT = 3'b111; // Logical NOT (Unary operation)

    // Internal signals
    wire [3:0] a = ui_in[7:4];         // Input a (high 4 bits of ui_in)
    wire [3:0] b = ui_in[3:0];         // Input b (low 4 bits of ui_in)
    wire [2:0] opcode = uio_in[2:0];   // Opcode (lower 3 bits of uio_in)
    wire [4:0] add_result;             // 5 bits to capture carry/overflow
    wire [4:0] sub_result;             // 5 bits to capture borrow
    wire [7:0] mul_result;             // 8 bits for multiplication
    wire [3:0] div_quotient;
    wire [3:0] div_remainder;
    wire [3:0] and_result = a & b;
    wire [3:0] or_result  = a | b;
    wire [3:0] xor_result = a ^ b;
    wire [3:0] not_result = ~a;
    reg [7:0] result;
    reg carry_out;
    reg overflow;

    // Addition
    assign add_result = a + b;

    // Subtraction
    assign sub_result = a - b;

    // Multiplication
    assign mul_result = a * b;

    // Division (handle division by zero)
    assign div_quotient = (b != 0) ? a / b : 4'b0000;
    assign div_remainder = (b != 0) ? a % b : 4'b0000;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            result <= 8'b00000000;
            carry_out <= 0;
            overflow <= 0;
        end else begin
            case (opcode)
                ADD: begin
                    result <= {4'b0000, add_result[3:0]}; // 4-bit result with upper 4 bits set to 0
                    carry_out <= add_result[4]; // Carry out
                    // Overflow detection
                    overflow <= (a[3] & b[3] & ~add_result[3]) | (~a[3] & ~b[3] & add_result[3]);
                end
                SUB: begin
                    result <= {4'b0000, sub_result[3:0]}; // 4-bit result with upper 4 bits set to 0
                    carry_out <= ~sub_result[4]; // Borrow detection
                    // Overflow detection
                    overflow <= (a[3] & ~b[3] & ~sub_result[3]) | (~a[3] & b[3] & sub_result[3]);
                end
                MUL: begin
                    result <= mul_result; // 8-bit result
                end
                DIV: begin
                    result <= {div_remainder, div_quotient}; // 8-bit result (remainder: lower 4 bits, quotient: upper 4 bits)
                end
                AND: begin
                    result <= {4'b0000, and_result}; // 4-bit result with upper 4 bits set to 0
                end
                OR: begin
                    result <= {4'b0000, or_result}; // 4-bit result with upper 4 bits set to 0
                end
                XOR: begin
                    result <= {4'b0000, xor_result}; // 4-bit result with upper 4 bits set to 0
                end
                NOT: begin
                    result <= {4'b0000, not_result}; // 4-bit result with upper 4 bits set to 0
                end
                default: begin
                    result <= 8'b00000000;
                    carry_out <= 0;
                    overflow <= 0;
                end
            endcase
        end
    end

    // Assign outputs
    assign uo_out  = result;
    assign uio_out[7] = overflow;   // Assign overflow to the most significant bit
    assign uio_out[6] = carry_out;  // Assign carry_out to the next bit
    assign uio_out[5] = 1'b0;       // Drive unused bits to 0
    assign uio_out[4] = 1'b0;       // Drive unused bits to 0
    assign uio_out[3] = 1'b0;       // Drive unused bits to 0
    assign uio_out[2] = 1'b0;       // Drive unused bits to 0
    assign uio_out[1] = 1'b0;       // Drive unused bits to 0
    assign uio_out[0] = 1'b0;       // Drive unused bits to 0

    // IO Enable Path
    assign uio_oe[7] = 1'b1; // Enable output for bit 7
    assign uio_oe[6] = 1'b1; // Enable output for bit 6
    assign uio_oe[5] = 1'b0; // Keep input for bit 5
    assign uio_oe[4] = 1'b0; // Keep input for bit 4
    assign uio_oe[3] = 1'b0; // Keep input for bit 3
    assign uio_oe[2] = 1'b0; // Keep input for bit 2
    assign uio_oe[1] = 1'b0; // Keep input for bit 1
    assign uio_oe[0] = 1'b0; // Keep input for bit 0

    // List all unused inputs to prevent warnings
    wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
