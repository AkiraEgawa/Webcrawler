# This will take a file as instructions and return them as an array of information

# File structure wanted
"""
First line: Starting URL
Second line: Depth
Third Line: URL Output file
Fourth Line: Tag/text Output file
Fifth Line onwards: Desired tags to extract
"""

def fileParser(file):
    with open(file) as f:
        lines = [line.strip() for line in f]
        if (len(lines) < 4):
            print("Instruction file too short, missing critical info")
            return -1
        if (len(lines) < 5):
            print("Missing tags (if don't want tags just put in a)")
            return -1
        
        # return instructions as dictionary
        instructions = {
            "start_url": lines[0],
            "depth": int(lines[1]),
            "url_output": lines[2],
            "tag_output": lines[3],
            "tags": lines[4:]
        }
    
    return instructions