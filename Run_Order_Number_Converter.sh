source /home/ben/minionvenv/bin/activate

#InputDirectory="/home/ben/Github/order-number-converter/sample_data/input"
#OutputDirectory="/home/ben/Github/order-number-converter/sample_data/output"
#PreviousOrderNumber="19000308_1900030701"
#InputOrderNumber="19000308-1900030701newID"
#NewOrderNumber="19000308_1900030701newID"

# This utility searches for (.txt) files in the InputDirectory.
# I will open each (.txt) file in the InputDirectory, and search for OldOrderNumber
# Every time OldOrderNumber is found, it is replaced by NewOrderNumber
# the new, changed files are written to OutputDirectory.

#python Order_Number_Converter_Main.py \
# --inputdir=InputDirectory \
# --outputdir=OutputDirectory \
# --previousordernumber=PreviousOrderNumber \
# --newordernumber=$NewOrderNumber

python Order_Number_Converter_Main.py


