from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type.value == other.text_type.value and self.url == other.url

        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

# returns the correct Leaf Node based on the passed in text node
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Not a valid type {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            new_nodes.append(old)
            continue
        
        #text = old.text
        lst = old.text.split(delimiter)
        to_add = []

        # a delimeter always adds 3 values to the lst ' ' whats inside the delimeter and ' '
        # therefore lst must be odd since odd + num always odd
        if len(lst) % 2 == 0:
            raise Exception("no closing delimiter")
        i = 0
        
        for new in lst:
            if new == '':
                i += 1
                continue
            # same idea odd i values will always be within the delimiter
            elif i % 2 == 0:
                to_add.append(TextNode(new, TextType.TEXT))
            else:
                to_add.append(TextNode(new, text_type))
            
            i += 1
        
        for x in to_add:
            new_nodes.append(x)

    return new_nodes
