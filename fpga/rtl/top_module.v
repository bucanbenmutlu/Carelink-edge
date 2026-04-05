module top_module (
    input wire clk,
    input wire reset,
    input wire medication_btn,
    input wire emergency_btn,
    input wire [1:0] mood,
    output wire alert_led,
    output wire buzzer
);

    wire [1:0] current_state;

    alert_fsm fsm_inst (
        .clk(clk),
        .reset(reset),
        .medication_btn(medication_btn),
        .emergency_btn(emergency_btn),
        .mood(mood),
        .state(current_state),
        .alert_led(alert_led),
        .buzzer(buzzer)
    );

endmodule
