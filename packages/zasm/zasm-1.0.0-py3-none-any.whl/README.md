Assembler for z80 CPU

This is a simple assembler for the z80 architecture.  
It parses .asm files are creates a binary file to be 
loaded into z80 memory, as well as a LST file for reference.

Usage

zasm filename.asm offset fill_size

The offset should be 0 if this is supposed to be loaded at the start of 
memory.  If, on the other hand, this is a program to be loaded at some other location in memory,
specify the offset of this start.   Code will be generated from address 0,
but only code starting at offset will be written to the binary output.

fill_size is used to specify the image file size.  If the memory size is
64k, using fill_size of 65536 will create exactly 64k image.



