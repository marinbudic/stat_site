from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from extract import text_to_textnodes

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

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []

    for node in nodes:
        html = text_node_to_html_node(node)
        children.append(html)
    
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.PARAGRAPH:
            lines = block.split("\n")
            joined = " ".join(lines)
            child = text_to_children(joined)
            children.append(ParentNode("p", child))
        elif btype == BlockType.HEADING:
            num = 0
            for i in range(len(block)):
                if block[i] == "#":
                    num += 1
                else:
                    break
            content = block[num + 1:]
            child = text_to_children(content)
            children.append(ParentNode(f"h{num}", child))
        elif btype == BlockType.CODE:
            if len(block) < 6 or block[0:3] != "```" or block [-3:] != "```":
                raise ValueError("not a code block")
            
            child = text_node_to_html_node(TextNode(block[4:-3], TextType.TEXT))
            text = ParentNode("code", [child])
            children.append(ParentNode("pre", [text]))
        elif btype == BlockType.QUOTE:
            lines = block.split("\n")
            raw_text = []
            
            for line in lines:
                if line[0] != ">":
                    raise ValueError("not a quote block")
                indent_removed = line.lstrip(">")
                raw_text.append(indent_removed.strip())
            text = " ".join(raw_text)
            child = text_to_children(text)
            children.append(ParentNode("blockquote", child))
        elif btype == BlockType.OLIST:
            lines = block.split("\n")
            list_lines = []

            for line in lines:
                lcontent = line[3:]
                child = text_to_children(lcontent)
                list_lines.append(ParentNode("li", child))
            
            children.append(ParentNode("ol", list_lines))
        elif btype == BlockType.ULIST:
            lines = block.split("\n")
            list_lines = []

            for line in lines:
                lcontent = line[2:]
                child = text_to_children(lcontent)
                list_lines.append(ParentNode("li", child))
            
            children.append(ParentNode("ul", list_lines))
        else:
            raise ValueError("not a block type")


    parent = ParentNode("div", children, None)

    return parent

print(markdown_to_html_node("```code```"))