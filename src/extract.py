import re
from textnode import TextNode, TextType, split_nodes_delimiter

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text) 
    return matches

def split_nodes_image(lst):
    new_nodes = []

    for node in lst:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        markdown = extract_markdown_images(node.text)

        if not markdown:
            new_nodes.append(node)
            continue

        image_alt, image_url = markdown[0]
        sections = node.text.split(f"![{image_alt}]({image_url})", 1)
        
        if len(sections) != 2:
            raise ValueError("invalid markdown image section not closed")

        if len(sections[0]) != 0:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        
        new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))


        if len(sections) > 1 and sections[1]:
            remaining = split_nodes_image([TextNode(sections[1], TextType.TEXT)])
            new_nodes.extend(remaining)

    return new_nodes

def split_nodes_link(lst):
    new_nodes = []

    for node in lst:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        markdown = extract_markdown_links(node.text)

        if not markdown:
            new_nodes.append(node)
            continue

        link_alt, link_url = markdown[0]
        sections = node.text.split(f"[{link_alt}]({link_url})", 1)

        if len(sections) != 2:
            raise ValueError("invalid markdown link section not closed")

        if len(sections[0]) != 0:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        
        new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))


        if len(sections) > 1 and sections[1]:
            remaining = split_nodes_link([TextNode(sections[1], TextType.TEXT)])
            new_nodes.extend(remaining)

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    
    raise Exception("No level one heading in markdown")