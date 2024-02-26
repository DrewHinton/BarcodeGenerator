# BarcodeGenerator
a simple python script that generates a series of barcodes given a list of items, a title, and an items code.


Steps to generate barcodes:
1. Add data to list.txt or whichever file _exampleRun.cmd is pointing to.
2. Ensure the names of the items are [word] [#]x format such as: hats 43x
3. click on _exampleRun.cmd to run the program. 
If it doesn't run, the number at the end is possibly incorrect format.


Generate barcodes using the command:
  python barcode_gen.py <input filepath> title=<title name> itemscode=<number 0-9>

example:
  python barcode_gen.py "items list (repo-ignored)/test.txt" title="random list" itemscode=7

