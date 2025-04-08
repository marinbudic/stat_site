from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    to_ret = []

    for b in blocks:
        if b == "":
            continue
        
        b = b.strip()
        to_ret.append(b)

    return to_ret

def block_to_block_type(line):
    lines = line.split("\n")

    if line[0:3] ==  "```" and line[-3:] == "```":
        return BlockType.CODE
    
    if line.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if line.startswith(">"):
        for l in lines:
            if not l.startswith(">"):
                return BlockType.PARAGRAPH
        
        return BlockType.QUOTE

    if line.startswith("- "):
        for l in lines:
            if not l.startswith("- "):
                return BlockType.PARAGRAPH
        
        return BlockType.ULIST

    if line.startswith("1. "):
        i = 1
        for l in lines:
            if not l.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1

        return BlockType.OLIST

    return BlockType.PARAGRAPH