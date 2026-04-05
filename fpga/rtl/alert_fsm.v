module alert_fsm (
    input wire clk,
    input wire reset,
    input wire medication_btn,
    input wire emergency_btn,
    input wire [1:0] mood,
    output reg [1:0] state,
    output reg alert_led,
    output reg buzzer
);

    localparam NORMAL    = 2'b00;
    localparam WARNING   = 2'b01;
    localparam CRITICAL  = 2'b10;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            state <= NORMAL;
            alert_led <= 0;
            buzzer <= 0;
        end else begin
            case (state)
                NORMAL: begin
                    alert_led <= 0;
                    buzzer <= 0;
                    if (emergency_btn)
                        state <= CRITICAL;
                    else if (mood == 2'b10)
                        state <= WARNING;
                    else
                        state <= NORMAL;
                end

                WARNING: begin
                    alert_led <= 1;
                    buzzer <= 0;
                    if (emergency_btn)
                        state <= CRITICAL;
                    else if (mood == 2'b00)
                        state <= NORMAL;
                    else
                        state <= WARNING;
                end

                CRITICAL: begin
                    alert_led <= 1;
                    buzzer <= 1;
                    if (medication_btn)
                        state <= NORMAL;
                    else
                        state <= CRITICAL;
                end

                default: begin
                    state <= NORMAL;
                    alert_led <= 0;
                    buzzer <= 0;
                end
            endcase
        end
    end

endmodule
