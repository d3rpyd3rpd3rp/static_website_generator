from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.functions import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

def main():
    text = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
    nodes = split_nodes_link([text])
    print(nodes)

if __name__ == "__main__":
    main()
