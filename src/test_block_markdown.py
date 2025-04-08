import unittest

from block_markdown import markdown_to_blocks, BlockType, block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_block_to_block_types(self):
        
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "# h"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "###### heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "####### heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "1. list"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "Flowers are the colorful and fragrant reproductive parts of many plants. They come in various shapes, sizes, and colors."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. list\n2. items\n3. asdsa\n4. dasfdadg\n5. asfdas\n6. hjfg\n7. sdvf\n8. ff\n9. gg\n10. hahaha\n11. wut"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)


if __name__ == "__main__":
    unittest.main()