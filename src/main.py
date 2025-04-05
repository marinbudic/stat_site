from textnode import TextNode, TextType, split_nodes_delimiter

def main():
    test = TextNode("This is some 'anchor' text", TextType.TEXT)
    print(split_nodes_delimiter([test], "'", TextType.CODE))

main()
