import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.LINK, url="https://www.boot.dev")

        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK, url="https://www.boot.dev")
        self.assertEqual('TextNode(This is a text node, link, https://www.boot.dev)', repr(node))

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, url="https://www.boot.dev")

        self.assertEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, url="https://www.boot.dev")

        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
