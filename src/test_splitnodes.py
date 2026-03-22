import unittest

from textnode import TextNode, TextType
from splitnodes import split_nodes_image, split_nodes_link


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode("![img](https://example.com/pic.png) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "https://example.com/pic.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode("text before ![img](https://example.com/pic.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("text before ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://example.com/pic.png"),
            ],
            new_nodes,
        )

    def test_split_image_only(self):
        node = TextNode("![img](https://example.com/pic.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("img", TextType.IMAGE, "https://example.com/pic.png")],
            new_nodes,
        )

    def test_split_image_no_images(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("just plain text", TextType.TEXT)],
            new_nodes,
        )

    def test_split_image_non_text_passthrough(self):
        node = TextNode("bold stuff", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("bold stuff", TextType.BOLD)], new_nodes)

    def test_split_image_mixed_nodes(self):
        nodes = [
            TextNode("before ![img](https://example.com/a.png) after", TextType.TEXT),
            TextNode("untouched", TextType.BOLD),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://example.com/a.png"),
                TextNode(" after", TextType.TEXT),
                TextNode("untouched", TextType.BOLD),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another](https://youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.LINK, "https://youtube.com"),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode("[click](https://example.com) and more text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("click", TextType.LINK, "https://example.com"),
                TextNode(" and more text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode("go to [site](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("go to ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_link_only(self):
        node = TextNode("[site](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("site", TextType.LINK, "https://example.com")],
            new_nodes,
        )

    def test_split_link_no_links(self):
        node = TextNode("no links here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("no links here", TextType.TEXT)],
            new_nodes,
        )

    def test_split_link_non_text_passthrough(self):
        node = TextNode("italic text", TextType.ITALIC)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("italic text", TextType.ITALIC)], new_nodes)

    def test_split_link_mixed_nodes(self):
        nodes = [
            TextNode("see [here](https://example.com) for info", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("see ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://example.com"),
                TextNode(" for info", TextType.TEXT),
                TextNode("code block", TextType.CODE),
            ],
            new_nodes,
        )

    def test_split_link_ignores_images(self):
        node = TextNode("an ![image](https://example.com/pic.png) here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("an ![image](https://example.com/pic.png) here", TextType.TEXT)],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
