import re

from src.textnode import TextNode, TextType
from src.htmlnode import LeafNode

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
            raise TypeError("Error: TextType does not exist")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            for i in range(len(parts)):
                if parts[i] == '':
                    continue
                if i % 2 == 0:
                    nodes.append(TextNode(parts[i], TextType.TEXT))
                else:
                    nodes.append(TextNode(parts[i], text_type))
    return nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            remaining = node.text
            for image in images:
                before, after = remaining.split(f"![{image[0]}]({image[1]})", 1)
                if before != '':
                    nodes.append(TextNode(before, TextType.TEXT))
                nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                remaining = after
            if remaining != '':
                nodes.append(TextNode(remaining, TextType.TEXT))
    return nodes

def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            remaining = node.text
            for link in links:
                before, after = remaining.split(f"[{link[0]}]({link[1]})", 1)
                if before != '':
                    nodes.append(TextNode(before, TextType.TEXT))
                nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                remaining = after
            if remaining != '':
                nodes.append(TextNode(remaining, TextType.TEXT))
    return nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_image([node])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
