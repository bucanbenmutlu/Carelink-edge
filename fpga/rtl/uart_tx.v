module uart_tx (
    input wire clk,
    input wire reset,
    input wire start,
    input wire [7:0] data_in,
    output reg tx,
    output reg busy
);

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            tx <= 1'b1;
            busy <= 1'b0;
        end else begin
            if (start) begin
                busy <= 1'b1;
                tx <= data_in[0];
            end else begin
                busy <= 1'b0;
                tx <= 1'b1;
            end
        end
    end

endmodule
