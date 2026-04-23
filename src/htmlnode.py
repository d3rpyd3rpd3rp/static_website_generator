from src.textnode import TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Not Implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        formatted = ""
        for props in self.props:
            formatted += f' {props}=\"{self.props[props]}\"'
        return formatted
    
    def __repr__(self):
        formatted = f"HTMLNode(tag={self.tag}, value={self.value}, children={{ "
        if self.children:
            for child in self.children:
                formatted += f"{child}, "
        else:
            formatted += "None, "
        formatted += "}, props={ "
        if self.props:
            for prop in self.props:
                formatted += f"{prop}: {self.props[prop]}, "
        else:
            formatted += "None, "
        formatted += "})"
        return formatted

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("Error: LeafNodes must have values")
        if not self.tag:
            return self.value
        formatted = f'<{self.tag}'
        if self.props:
            formatted += f'{self.props_to_html()}>'
        else:
            formatted += '>'
        formatted += f'{self.value}</{self.tag}>'
        return formatted
    
    def __repr__(self):
        if not self.value:
            raise ValueError("Error: LeafNodes must have values")
        formatted = f"LeafNode(tag={self.tag}, value={self.value}, props={{ "
        if self.props:
            for prop in self.props:
                formatted += f"{prop}: {self.props[prop]}, "
        else:
            formatted += "None, "
        formatted += "})"
        return formatted

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Error: ParentNodes must have tags")
        if not self.children:
            raise ValueError("Error: ParentNodes must have children")
        formatted = f"<{self.tag}>"
        for child in self.children:
            formatted += child.to_html()
        formatted += f"</{self.tag}>"
        return formatted
    
    def __repr__(self):
        if not self.tag:
            raise ValueError("Error: ParentNodes must have tags")
        if not self.children:
            raise ValueError("Error: ParentNodes must have children")
        formatted = f"ParentNode(tag={self.tag}, children={{ "
        for child in self.children:
            formatted += f"{child}, "
        formatted += "}, props={ "
        if self.props:
            for prop in self.props:
                formatted += f"{prop}: {self.props[prop]}, "
        else:
            formatted += "None, "
        formatted += "})"
        return formatted

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