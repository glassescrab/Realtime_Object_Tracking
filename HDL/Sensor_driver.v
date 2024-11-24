`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/11/24 15:34:37
// Design Name: 
// Module Name: Sensor_driver
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module Sensor_driver(
    input clk,
    
    input wire[31:0] PC_command,
    
    output reg[31:0] PC_acl_x,
    output reg[31:0] PC_acl_y,
    output reg[31:0] PC_acl_z,
    
    output reg[31:0] PC_mag_x,
    output reg[31:0] PC_mag_y,
    output reg[31:0] PC_mag_z,
    
    output reg ADT7420_A0,
    output reg ADT7420_A1,
    
    output I2C_SCL,
    inout  I2C_SDA      
    );
    
    reg [31:0] PC_rx;
    reg [31:0] PC_tx;
    reg [31:0] PC_slave_addr;
    reg [31:0] PC_addr;
    reg [31:0] PC_val;
    
    wire SCL,SDA,ACK;
    wire [7:0] tx_byte, rx_byte;
    wire [1:0] next_step;
    wire ready;
    wire busy;
    
    localparam read_rx  = 31'd2;
    localparam write_rx = 31'd1;
    localparam idle_rx  = 31'd0;
    
    localparam ctrl_reg_1_addr  = 31'h20;
    localparam ctrl_reg_1_value = 31'h37;
    localparam mr_reg_m_addr  = 31'h02;
    localparam mr_reg_m_value = 31'h00;
    localparam accel_salve_addr = 31'h32;
    localparam magnet_slave_addr = 31'h3C;
    localparam x_a_reg_addr = 31'hA8;
    localparam y_a_reg_addr = 31'hAA;
    localparam z_a_reg_addr = 31'hAC;
    localparam x_m_reg_addr = 31'h03;
    localparam y_m_reg_addr = 31'h07;
    localparam z_m_reg_addr = 31'h05;
    
    
    I2C_driver I2C_SERDES ( 
        .busy(busy),
               
        .led(led),
        .clk(clk),
        .ADT7420_A0(ADT7420_A0),
        .ADT7420_A1(ADT7420_A1),
        .I2C_SCL_0(I2C_SCL_1),
        .I2C_SDA_0(I2C_SDA_1),             

        .ACK(ACK),
        .SCL(SCL),
        .SDA(SDA),
        .State(State),
        
        .tx_byte(tx_byte),
        .rx_byte(rx_byte),
        .next_step(next_step),
        .ready(ready)
        );
        
    I2C_controller I2C_controller(
        .clk(clk),
        .PC_rx(PC_rx),
        .PC_tx(PC_tx),
        .PC_slave_addr(PC_slave_addr),
        .PC_addr(PC_addr),
        .PC_val(PC_val),
        .next_step(next_step),
        .tx_byte(tx_byte),
        .rx_byte(rx_byte),
        .cur_state(cur_state),
        .PC_rx_reg1(PC_rx_reg1),
        .PC_rx_reg2(PC_rx_reg2),
        .ready(ready)
    );
    
    reg [4:0] steps;
    reg [14:0] HS_counter = 1;
    
    localparam idle   = 5'b00000;
    localparam init_1 = 5'b00001;
    localparam init_2 = 5'b00010;
    localparam read_1 = 5'b00100;
    localparam read_2 = 5'b01000;
    
    always @(posedge clk) begin
        case (cur_state) begin
            5'b00000 : begin
                
                    
     
    
    
    
    
endmodule
