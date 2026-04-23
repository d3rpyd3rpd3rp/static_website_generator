from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    textnode = TextNode("Hello, World!", TextType.BOLD, "https://example.com")
    htmlnode = HTMLNode("p", None, [textnode], {"class": "my-class"})
    leafnode = LeafNode("a", "definitely not a rickroll", {"href": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
    parentnode = ParentNode("p", [textnode, htmlnode, leafnode], None)
    printable = f"{textnode}\n{htmlnode}\n{leafnode}\n{parentnode}"
    print(printable)

if __name__ == "__main__":
    main()
