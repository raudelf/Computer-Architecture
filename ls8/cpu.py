"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        program = []

        with open(filename) as f:
            for line in f:
                line_split = line.split("#")
                binary_num = line_split[0]

                try:
                    num = int(binary_num, 2)
                    program.append(num)

                except:
                    continue

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
        return f'{value} was added to the ram'

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == MUL:
            return self.reg[reg_a] * self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            cur_ram = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if cur_ram is LDI:

                self.reg[operand_a] = operand_b

                self.pc += 3

            if cur_ram is PRN:
                print(self.reg[operand_a])
                self.pc += 2

            if cur_ram is MUL:
                self.reg[operand_a] = self.alu(cur_ram, operand_a, operand_b)
                print(self.reg[operand_a])
                self.pc += 2

            if cur_ram is HLT:
                running = False
                self.pc += 1
                print('CPU has stopped running')
