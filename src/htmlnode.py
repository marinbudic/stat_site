class HTMLNode:
    # tag - A string representing the HTML tag name 
    # value - A string representing the value of the HTML tag
    # children - A list of HTMLNode objects representing the children of this node
    # props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html not implemented")

    # if no props return empty string
    # else loop through each key value pair 
    # for each, convert to html and add to string

    def props_to_html(self):
        if self.props is None:
            return ""

        node = ""

        for key in self.props:
            node += " " + key + "=" + '"' + self.props[key] + '"' 

        return node

    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"

class LeafNode(HTMLNode):

    # tag - A string representing the HTML tag name 
    # value - A string representing the value of the HTML tag
    # children - Always none
    # props - A dictionary of key-value pairs representing the attributes of the HTML tag.

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    # check if value exists in leafnode
    # if no tag just return value
    # if no properties return the html
    # otherwise return the html with the properties

    def to_html(self):
        if self.value == None:
            raise ValueError("invalid HTML: Value cannot be None")
        if self.tag == None:
            return self.value
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    # check each text type case and return the proper leaf node

    def text_node_to_html_node(self, text_node):
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

    def __repr__(self):
        return f"LeafNode(Tag: {self.tag}, Value: {self.value}, Props: {self.props}"

class ParentNode(HTMLNode):

    # tag - A string representing the HTML tag name 
    # value - Always None
    # children - A list of HTMLNode objects representing the children of this node
    # props - A dictionary of key-value pairs representing the attributes of the HTML tag.

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    # check if node has tag and children
    # for each child of parent call its to_html function and add to string
    # after all recursive calls return the parent tag and props with the string

    def to_html(self):
        if self.tag == None:
            raise ValueError("parent node must have tag")
        if self.children == None:
            raise ValueError("parent node must have children")
        
        tmp = ""

        for c in self.children:
            tmp += c.to_html()

        return f"<{self.tag}{self.props_to_html()}>{tmp}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
