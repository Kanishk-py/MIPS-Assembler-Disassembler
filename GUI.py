from pickle import FRAME
from tkinter import *
import os
import disassembler
import assembler

root = Tk()

# Defining Title and size of window
root.title('COMPARC')
root.geometry("1100x650")
root['bg'] = "gray"

# Function to open "Filename" in "txtbox"
def open_txt(txt_box, filename):
	clear(txt_box)
	file = filename

	file = open(file, 'r')
	data = file.read()

	txt_box.insert(END, data)
	file.close()

# Here two functions are defined to read the data in Text Box,
# write them in their respective file and call the function from other module to convert the code.

def convertMIPS(txt_box):
	text_file = 'MIPS.txt'
	text_file = open(text_file, 'w')
	text_file.write(txt_box.get(1.0, END))
	text_file.close()
	assembler.assemble(isbin.get())
	open_txt(text2,'machine.txt')


def convertMachine(txt_box):
	text_file = 'machine.txt'
	text_file = open(text_file, 'w')
	text_file.write(txt_box.get(1.0, END))
	text_file.close()
	disassembler.disassemble(isbin.get())
	open_txt(text1,'MIPS.txt')

# Function to clear the text box
def clear(txt_box):
	txt_box.delete("1.0", END)

my_frame = Frame(root)
radio = Frame(root)
top = Frame(root)
topleft = Frame(top)
topright = Frame(top)


w = Label(topleft, text="MIPS CODE", anchor=CENTER)
w.pack(padx=5, pady=20, anchor=CENTER)
w = Label(topright, text="MACHINE CODE", anchor="center")
w.pack(padx=5, pady=20)

radio.pack(pady=10, side="top")
top.pack( side="top")
topleft.pack(side="left")
topright.pack(side="right")
my_frame.pack(pady=10)


isbin = IntVar()
R1 = Radiobutton(radio, text="Read/Write from binary", variable=isbin, value=1)
R1.pack()
R1 = Radiobutton(radio, text="Read/Write from hexadecimal", variable=isbin, value=0)
R1.pack()


# Create scrollbar
scroll1 = Scrollbar(topleft)
scroll1.pack(side=RIGHT, fill=Y)

scroll2 = Scrollbar(topright)
scroll2.pack(side=RIGHT, fill=Y)


text1 = Text(topleft, width=40, height=10, font=("Times New Roman", 16), selectbackground="yellow",
				selectforeground="black", yscrollcommand=scroll1.set, undo=True)
text1.pack(pady=20)
scroll1.config(command=text1.yview)

text2 = Text(topright, width=40, height=10, font=("Times New Roman", 16), selectbackground="yellow",
				selectforeground="black", yscrollcommand=scroll2.set, undo=True)
text2.pack(pady=20)
scroll2.config(command=text2.yview)

#########################################################################################################################
openButton1 = Button(topleft, text="Read MIPS code from File", command=lambda: open_txt(text1, 'MIPS.txt'))
openButton1.pack(pady=20)

saveButton1 = Button(topleft, text="Convert MIPS to Machine Code", command=lambda: convertMIPS(text1))
saveButton1.pack(pady=20)

clear1 = Button(topleft, text="Clear MIPS Textbox", command=lambda: clear(text1))
clear1.pack(pady=20)
#########################################################################################################################
openButton2 = Button(topright, text="Read Machine code from File", command=lambda: open_txt(text2, 'machine.txt'))
openButton2.pack(pady=20)

saveButton2 = Button(topright, text="Convert Machine Code to MIPS", command=lambda: convertMachine(text2))
saveButton2.pack(pady=20)

clear2 = Button(topright, text="Clear Machine Code Textbox", command=lambda: clear(text2))
clear2.pack(pady=20)
#########################################################################################################################

root.mainloop()
