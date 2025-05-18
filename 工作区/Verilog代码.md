
```

module top_module(
    input [31:0] a,
    input [31:0] b,
    output [31:0] sum
);
    wire[15:0] w1;
    wire[15:0] w2;
    wire choose;
    add16 ins1(.cin(0), .cout(choose), .sum(sum[15:0]), .a(a[15:0]), .b(b[15:0]));
    add16 ins2(.cin(0), .cout(), .sum(w1), .a(a[31:16]), .b(b[31:16]));
    add16 ins3(.cin(1), .cout(), .sum(w2), .a(a[31:16]), .b(b[31:16]));
    selector(.out(sum[31:16]), .in1(w1), .in2(w2), .choose(choose));
               
endmodule
               
module selector(
    input[15:0] in1,
    input[15:0] in2,
    input choose,
    output[15:0] out
);
    always @(*) begin
    	case(choose)
        	1'b0 : out = in1;
        	1'b1 : out = in2;
    	endcase
    end
endmodule
        

```