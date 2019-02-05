import sys
import re
from xml.etree import cElementTree as ElementTree


class NodeText:
    def __init__(self, txt):
        self.txt: str = txt.strip()

    def reformat_workflow_tags(self):
        self.txt = re.sub(f'@((Figure|Table|File)\w*)', r'**\1**', self.txt)
        self.txt = re.sub('[_\-]', ' ', self.txt)
        return self

    def remove_html_tags(self):
        self.txt = re.sub('<[ubi]>', '', self.txt)
        self.txt = re.sub('<\/[ubi]>', '', self.txt)
        return self

    def remove_workflowy_tags(self):
        self.txt = re.sub('[@#](?!Figure|Table|File|\#|p|REF|XXX)[\w\-]+', '', self.txt)
        return self

    def remove_space(self):
        self.txt = re.sub('\s+', ' ', self.txt)
        self.txt = self.txt.strip()
        return self

    def format(self):
        return (self.remove_html_tags()
                .remove_workflowy_tags()
                .reformat_workflow_tags()
                .remove_space())


def main():
    tree = ElementTree.parse(sys.argv[1])
    root = tree.getroot()
    dom = root.find('body/outline')
    document = [
        line
        for line in crawl_tree(dom)

    ]

    print(re.sub('\n\n\n', '\n\n', '\n'.join(document)))


def crawl_tree(dom):
    for child in dom:
        txt = NodeText(child.attrib['text']).format().txt
        if re.match(r'#+ ', txt):
            # header
            yield '\n' + txt + '\n'

        elif re.match('^\*\*(Figure|Table|File)', txt):
            paragraph = [NodeText(txt).format().txt]
            for gc in crawl_tree(child):
                paragraph.append(gc)
            yield ' '.join(paragraph) + '\n'
            continue

        elif re.match('^#p\s*', txt):
            paragraph = [
                gc
                for gc in crawl_tree(child)
            ]
            yield ' '.join(paragraph) + '\n'
            continue
        elif txt == '':
            yield '\n'
        else:
            yield txt
        yield from crawl_tree(child)


if __name__ == '__main__':
    main()
