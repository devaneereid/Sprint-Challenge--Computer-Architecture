"""CPU Functionality"""

import sys

class CPU:
    """Main CPU Class"""

    def __init__(self):
        self.reg = [0] * 8 
        self.ram = [0] * 256
        self.pc = 0
        self.SP = 7
        self.FL = 1

    def load(self, filename):
        """Load a program into memory."""

        # filename = sys.argv[1]
        try: 
            address = 0
            # count = 0

            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue 
                    
                    val = int(n, 2)

                    self.ram[address] = val
                    # count = count + 1

                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

        self.reg = [0] * 8

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101 
        POP = 0b01000110
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        running = True
        instruction = 0
        # SP = self.SP
        # op_size = 1
    
        while running:
            instruction = self.ram[self.pc]
            # print(instruction)

            if instruction == LDI:
                # print(LDI)
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                print(reg_b)
                self.reg[reg_a] = reg_b
                
                self.pc += 3

            elif instruction == PRN:
                # print(PRN)
                reg_a = self.ram_read(self.pc + 1)
                print(reg_a)

                reg_b = self.reg[reg_a]
                print(reg_b)

                self.pc += 2

            elif instruction == HLT:
                # print(HLT)
                running = False

            elif instruction == MUL:
                # print(MUL)
                reg_a = self.ram_read(self.pc + 1)
                # print(reg_a)
                reg_b = self.ram_read(self.pc + 2)
                # print(reg_b)

                self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
                # print(self.reg[reg_a])
                self.pc += 3

            elif instruction == PUSH:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(reg_a)

                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = reg_b

                self.pc += 2

            elif instruction == POP:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram[self.reg[self.SP]]

                self.reg[reg_a] = reg_b
                self.reg[self.SP] += 1

                self.pc += 2

            # CMP register
            elif instruction == CMP:
                # CMP registerA registerB
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                # Compare the values in two registers
                if self.reg[reg_a] == self.reg[reg_b]:
                    # If they are equal, set the Equal E flag to 1, otherwise set it to 0
                    self.FL = 1
                else:
                    self.FL = 0

                self.pc += 3

            # JMP register
            elif instruction == JMP:
                # Jump to the address stored in the given register
                reg_a = self.ram[self.pc + 1]

                # Set the PC to the address stored in the given register
                self.pc = self.reg[reg_a]

            # JEQ register
            elif instruction == JEQ:
                # If equal flag is set (true, 1), jump to the address stored in the given register
                if self.FL == 1:
                    reg_a = self.ram[self.pc + 1]
                    self.pc = self.reg[reg_a]
                else:
                    self.pc += 2

            # JNE Register
            elif instruction == JNE:
                # If E flag is clear (false, 0), jump to the address stored in the given register
                if self.FL == 0:
                    reg_a = self.ram[self.pc + 1]
                    self.pc = self.reg[reg_a]
                else: 
                    self.pc += 2

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
 
