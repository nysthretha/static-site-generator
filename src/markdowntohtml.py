from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from markdowntoblocks import markdown_to_blocks
from blocktype import BlockType, block_to_block_type
from texttotextnodes import text_to_textnodes


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    code = ParentNode("code", [text_node_to_html_node(text_node)])
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = block.split("\n")
    stripped = []
    for line in lines:
        if line.startswith("> "):
            stripped.append(line[2:])
        else:
            stripped.append(line[1:])
    text = " ".join(stripped)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[line.index(". ") + 2:]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)


def paragraph_to_html_node(block):
    text = " ".join(block.split("\n"))
    children = text_to_children(text)
    return ParentNode("p", children)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
            case BlockType.CODE:
                children.append(code_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                children.append(unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                children.append(ordered_list_to_html_node(block))
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))
    return ParentNode("div", children)
