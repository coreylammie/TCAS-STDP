// TSTDP Module [Minimal Hippocampal]
// Model Parameters:
// ---------------------------------------------
// tauY = 2^(5)      = 32
// tauPlus 2^(4)     = 16
// tauMinus = 2^(7)  = 128
// A2Plus = 2^(-12)  = 0.00024414062
// A3Plus = 2^(-7)   = 0.0078125
// A3Minus = 2^(-10) = 0.0009765625
// ---------------------------------------------
module TSTDP(preSynapticSpike, postSynapticSpike, clk, ENABLE, LEDR, dataToSend);
	input preSynapticSpike; // Presynaptic spike input
	input postSynapticSpike; // Postsynaptic spike input
	input clk; // Clock input
	input ENABLE; // Enable signal to allow data transmission
	output dataToSend; // Output data to send over the UART interface
	output wire [9:0] LEDR; // LEDs used for debugging

	integer currentWeight = 0; // Current synaptic weight
	reg [27:0]  clkCount = 28'd0; // 28Bit counter to store the current clock count [0-268435456]
	reg TSTDP_CLK = 0; // TSTDP clock
	// Assign r1, r2, o1, and o2
	reg signed [17:0] r1 = 0;
	reg signed [17:0] r2 = 0;
	reg signed [17:0] o1 = 0;
	reg signed [17:0] o2 = 0;
	// Initialize registers to store previous values of r2, and o2
	reg signed [17:0] r2prev = 0;
	reg signed [17:0] o2prev = 0;
	// MOORE machine variables
	reg [2:0] statePre = 2'b0; // Set the initial (current) state to 0/A [Pre]
	reg [2:0] nextStatePre = 2'b0; // Next state [Pre]
	reg outPre = 0; // Output of the MOORE machine [Pre]
	reg [2:0] statePost = 2'b0; // Set the initial (current) state to 0/A [Post]
	reg [2:0] nextStatePost = 2'b0; // Next state [Post]
	reg outPost = 0; // Output of the MOORE machine [Post]
	localparam A=0, B=1, C=2; // Local parameters for MOORE machine states
	FourBitMuliplier o2prev_r1(product_o2prev_r1, o2prev, r1, clk, reset); // Approximate o2prev * r1

	always @(*)
		begin
			dataToSend.currentSynapticWeight = currentWeight;
		end

	// Generate TSTDP_CLK
	always @ (posedge clk) // On the rising edge of the clock
		begin
			// Generate the shift register clock
			clkCount <= clkCount + 1; // Increment clkCount
			if (clkCount == 28'd6250)
				begin
					clkCount <= 0; // Reset clkCount
					TSTDP_CLK <= ~TSTDP_CLK; // Invert the TSTDP clock signal
				end
		end

	// Iteratively update the synaptic weight and associated differential equations
	always @ (posedge TSTDP_CLK) // On the rising edge of TSTDP_CLK [1ms]
		begin
			if (ENABLE == 1) // If ENABLE is HIGH
				begin
					currentWeight = currentWeight + 1;
					if (outPre) // If a presynaptic spike is detected
						begin
							// Update r1, r2, o1 and o2
							r1 = 18'sd1;
							r2 = 18'sd1;
							o1 = o1 - (o1 >>> 7);
							o2 = o2 - (o2 >>> 5);
							// Update the synaptic weight
							currentWeight = currentWeight - ((o1 >>> 9) + ((r2prev*o1) >>> 10));
						end
					else if (outPost) // If a postsynaptic spike is detected
						begin
							// Update r1, r2, o1 and o2
							r1 = r1 - (r1 >>> 4);
							r2 = r2 - (r2 >>> 10);
							o1 = 18'sd1;
							o2 = 18'sd1;
							// Update the synaptic weight
							currentWeight = currentWeight + ((r1 >>> 12) + ((o2prev*r1) >>> 7));
						end
					else begin
						r1 = r1 - (r1 >>> 4);
						r2 = r2 - (r2 >>> 10);
						o1 = o1 - (o1 >>> 7);
						o2 = o2 - (o2 >>> 5);
					end
					r2prev = r2; // Store the current value of r2 in a buffer
					o2prev = o2; // Store the current value of o2 in a buffer
				end
		end

	// MOORE machine for the presypatic input signal [Every 1ms]
	always @ (posedge TSTDP_CLK) // On the rising edge of TSTDP_CLK
		begin
			statePre = nextStatePre; // Assign the current state from the next state
			case (statePre) // Determine the next state from the previous state
				A : if (preSynapticSpike) nextStatePre = C; // If the signal is initially HIGH goto state C
					else nextStatePre = B; // If the signal is initially LOW goto state B
				B : if (preSynapticSpike) begin // If the signal transitions from LOW to HIGH output HIGH and goto state C
						outPre = outPre | 1; // Output HIGH
						nextStatePre = C; // Goto state C
					end
				C : if (~preSynapticSpike) nextStatePre = B; // If the signal transitions from HIGH to LOW goto state B
				default : begin // Otherwize return do not care [X]
					nextStatePre = 3'bX;
				end
			endcase
			cycleCountPre = cycleCountPre + 1;
			if (cycleCountPre == 0)
				begin
					if (outPre == 1)
						begin
							LEDR[8] <= ~LEDR[8];
						end
					else begin
						LEDR[8] <= 0;
					end
					cycleCountPre <= 1;
					outPre <= 0; // Reset outPost to be zero
				end
		end

	// MOORE machine for the postsypatic input signal
	always @ (posedge TSTDP_CLK) // On the rising edge of TSTDP_CLK [Every 1ms]
		begin
			statePost = nextStatePost; // Assign the current state from the 'next' state
			case (statePost) // Determine the next state from the previous state
				A : if (postSynapticSpike) nextStatePost = C; // If the signal is initially HIGH goto state C
					else nextStatePost = B; // If the signal is initially LOW goto state B
				B : if (postSynapticSpike) begin // If the signal transitions from LOW to HIGH output HIGH and goto state C
						outPost = outPost | 1; // Output HIGH
						nextStatePost = C; // Goto state C
					end
				C : if (~postSynapticSpike) nextStatePost = B; // If the signal transitions from HIGH to LOW goto state B
				default : begin // Otherwize return do not care [X] to avoid instability
					//outPost = 1'bX;
					nextStatePost = 3'bX;
				end
			endcase
			cycleCountPost = cycleCountPost + 1;
			if (cycleCountPost == 0)
				begin
					if (outPost == 1)
						begin
							LEDR[9] <= ~LEDR[9];
						end
					else begin
						LEDR[9] <= 0;
					end
					cycleCountPost <= 1;
					outPost <= 0; // Reset outPost to be zero
				end
		end
endmodule

// FourBitMultiplier
// Multiplies two four bit unsigned numbers and returns the product
module FourBitMuliplier(product, a, b, clk, reset);
	input [3:0] a, b; // Inputs to multiply
	input clk, reset;
	output reg [7:0] product; // Product of the inputs
	reg [7:0] tmp0, tmp1, tmp2, tmp3; // Registers to hold temporary values
	wire [7:0] tmp; // Register to hold 4'b0000, b temporarily
	assign tmp = {4'b0000, b}; // Assign 4'b000, b to tmp

	always @ (posedge clk) // On the rising edge of the clock
 		begin
			if (reset) // If reset is HIGH
				begin
					// Reset the product register's state
					product = 8'bzzzz_zzzz;
				end
			else
				begin
					case (a[0]) // For the zeroith bit of a
						1'b0: tmp0 = 8'b0000_0000;
						1'b1: tmp0 = tmp;
					endcase
					case (a[1]) // For the first bit of a
						1'b0: tmp1 = 8'b0000_0000;
						1'b1: tmp1 = tmp<<1;
					endcase
					case (a[2]) // For the second bit of a
						1'b0: tmp2 = 8'b0000_0000;
						1'b1: tmp2 = tmp<<2;
					endcase
					case (a[3]) // For the third bit of a
						1'b0: tmp3 = 8'b0000_0000;
						1'b1: tmp3 = tmp<<3;
					endcase
							// Determine the product by summing tmp0, tmp1, tmp2 and tmp3
      				product = tmp0 + tmp1 + tmp2 + tmp3;
				end
		end
endmodule
