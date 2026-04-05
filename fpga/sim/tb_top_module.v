`timescale 1ns / 1ps

module tb_top_module;

    reg clk = 0;
    reg reset = 0;
    reg medication_btn = 0;
    reg emergency_btn = 0;
    reg [1:0] mood = 2'b00;

    wire alert_led;
    wire buzzer;

    top_module uut (
        .clk(clk),
        .reset(reset),
        .medication_btn(medication_btn),
        .emergency_btn(emergency_btn),
        .mood(mood),
        .alert_led(alert_led),
        .buzzer(buzzer)
    );

    always #5 clk = ~clk;

    initial begin
        reset = 1;
        #10 reset = 0;

        mood = 2'b10;
        #20;

        emergency_btn = 1;
        #10 emergency_btn = 0;
        #20;

        medication_btn = 1;
        #10 medication_btn = 0;
        #20;

        $finish;
    end

endmodule
