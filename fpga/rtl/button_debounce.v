module button_debounce (
    input wire clk,
    input wire btn_in,
    output reg btn_out
);

    reg [15:0] counter = 0;
    reg stable_state = 0;

    always @(posedge clk) begin
        if (btn_in == stable_state) begin
            counter <= 0;
        end else begin
            counter <= counter + 1;
            if (counter == 16'hFFFF) begin
                stable_state <= btn_in;
                btn_out <= btn_in;
                counter <= 0;
            end
        end
    end

endmodule
