import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_eq(self):
        node = ' href="https://www.google.com" target="_blank"'
        node2 = HTMLNode("p", "This is a test", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node, node2.props_to_html())

    def test_props_to_html_not_eq(self):
        node = ' href="https://www.boot.dev" target="_blank"'
        node2 = HTMLNode("p", "This is a test", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node, node2.props_to_html())

    def test_repr(self):
        node = HTMLNode("p", "This is a test", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(repr(node), "Tag: p, Value: This is a test, Children: None, Props: {'href': 'https://www.google.com', 'target': '_blank'}")
    
    def test_values(self):
        node = HTMLNode("div", "test")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "test")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertNotEqual(node.to_html(), node1.to_html())
        self.assertNotEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual('<a href="https://www.google.com">Click me!</a>', node1.to_html())
    
    def test_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), "LeafNode(Tag: p, Value: Hello, world!, Props: None")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a BOLD node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a BOLD node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {"src": "https://google.com", "alt": "This is an image node"})

if __name__ == "__main__()":
    unittest.main()
