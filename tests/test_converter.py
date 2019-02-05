from opml2markdown import converter


def test_remove_html_tags_underline():
    node = converter.NodeText('<u>Link</u>')
    node.remove_html_tags()
    assert node.txt == 'Link'


def test_remove_html_tags_bold():
    node = converter.NodeText('<b>Link</b>')
    node.remove_html_tags()
    assert node.txt == 'Link'


def test_remove_html_tags_italics():
    node = converter.NodeText('<i>Link</i>')
    node.remove_html_tags()
    assert node.txt == 'Link'


def test_remove_html_tags_bold_italics():
    node = converter.NodeText('<b><i>Link</i></b>')
    node.remove_html_tags()
    assert node.txt == 'Link'


def test_reformat_workflowy_tag():
    assert converter.NodeText('@Figure').reformat_workflow_tags().txt == '**Figure**'
    assert converter.NodeText('@Figure_1').reformat_workflow_tags().txt == '**Figure 1**'
    assert converter.NodeText('@Table_1A').reformat_workflow_tags().txt == '**Table 1A**'
    assert converter.NodeText('@File').reformat_workflow_tags().txt == '**File**'
    assert converter.NodeText('@Figure blah blah @File_1').reformat_workflow_tags().txt == '**Figure** blah blah **File 1**'


def test_remove_workflowy_tags():
    assert converter.NodeText('#p blah').remove_workflowy_tags().remove_space().txt == '#p blah'
    assert converter.NodeText('#p blah @Figure').remove_workflowy_tags().remove_space().txt == '#p blah @Figure'


def test_workflowy_tags_and_html():
    node = converter.NodeText('#p <b>@Figure</b> @wip @fup #word-count')
    assert node.format().txt == '**Figure**'


def test_workflowy_tags_w_markdown():
    assert converter.NodeText('## Header @fup <i>*italics*</i>').format().txt == '## Header *italics*'


def test_remove_double_space():
    assert converter.NodeText('One      Two').remove_space().txt == 'One Two'


def test_crawl_tree():
    from xml.etree import cElementTree as ElementTree
    dom = ElementTree.fromstring("""
    <body>
        <outline text='l1'>
            <outline text='l2'>
                <outline text='l3'></outline>
                <outline text='l3.2'></outline>
            </outline>
        </outline>
    </body>
    """)

    assert [child for child in converter.crawl_tree(dom)] == ['l1', 'l2', 'l3', 'l3.2']
