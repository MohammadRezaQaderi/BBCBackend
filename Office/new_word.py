from docx import *
import zipfile
import os
import shutil
from lxml import etree
from docx2pdf import convert
import pythoncom
import win32com.client as client
import copy
import uuid
import glob


def CovertDocxToPDF(SourceFile: str, DestinationFile: str) -> None:
    """Convert a Word file to PDF.

    Args:
        SourceFile: Input Word file path
        DestinationFile: Output PDF file path
    """
    if os.path.exists(DestinationFile):
        os.remove(DestinationFile)
    convert(SourceFile, DestinationFile)


def CovertWordToPDF(SourceFile: str, DestinationFile: str) -> None:
    """Convert a Word file to PDF using Word COM interface.

    Args:
        SourceFile: Input Word file path
        DestinationFile: Output PDF file path
    """
    if os.path.isfile(DestinationFile):
        os.remove(DestinationFile)

    pythoncom.CoInitialize()
    word = client.DispatchEx("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(SourceFile)
    doc.SaveAs(DestinationFile, FileFormat=17)  # wdFormatPDF
    doc.Close()
    word.Quit()


def GetXMLTagWithoutNS(XMLTag: str) -> str:
    """Remove namespace from an XML tag.

    Args:
        XMLTag: Input XML tag

    Returns:
        Tag without namespace
    """
    i = len(XMLTag) - 1
    while i >= 0 and XMLTag[i] not in (':', '}'):
        i -= 1
    return XMLTag if i == -1 else XMLTag[i + 1:]


def GetXMLTagNamespace(XMLTag: str) -> str:
    """Get namespace from an XML tag.

    Args:
        XMLTag: Input XML tag

    Returns:
        Namespace of the tag
    """
    i = len(XMLTag) - 1
    while i >= 0 and XMLTag[i] not in (':', '}'):
        i -= 1
    return XMLTag[0:i + 1]


def UnzipWordFile(SourceFile: str, OutputFolder: str) -> None:
    """Unzip a Word file to a folder.

    Args:
        SourceFile: Input Word file path
        OutputFolder: Output folder path
    """
    with zipfile.ZipFile(SourceFile, 'r') as zip_ref:
        zip_ref.extractall(OutputFolder)


def ZipWordFolder(
        SourceFolder: str,
        DestinationFile: str,
        RemoveFolder: bool = True
) -> None:
    """Zip a folder into a Word file.

    Args:
        SourceFolder: Input folder path
        DestinationFile: Output Word file path
        RemoveFolder: Whether to remove the source folder
    """
    shutil.make_archive(DestinationFile, 'zip', SourceFolder)

    if RemoveFolder:
        shutil.rmtree(SourceFolder)

    if os.path.isfile(DestinationFile):
        os.remove(DestinationFile)

    os.rename(DestinationFile + '.zip', DestinationFile)


def LoadXMLFile(SourceFile: str) -> etree.ElementTree:
    """Load an XML file into an ElementTree.

    Args:
        SourceFile: Input XML file path

    Returns:
        Parsed XML ElementTree
    """
    parser = etree.XMLParser(ns_clean=True, recover=True)
    return etree.parse(SourceFile, parser)


def SaveXMLToFile(
        XMLTree: etree.ElementTree,
        DestinationFile: str
) -> None:
    """Save an ElementTree to an XML file.

    Args:
        XMLTree: Input ElementTree
        DestinationFile: Output XML file path
    """
    XMLTree.write(
        DestinationFile,
        xml_declaration=True,
        encoding='UTF-8'
    )


def ReplaceText(
        XMLTree: etree.ElementTree,
        OldText: str,
        NewText: str
) -> None:
    """Replace text in XML elements.

    Args:
        XMLTree: Input ElementTree
        OldText: Text to replace
        NewText: New text
    """
    for item in XMLTree.iter():
        if item.text is not None:
            item.text = item.text.replace(OldText, NewText)


def ReplaceTexts(
        XMLTree: etree.ElementTree,
        OldTexts: list[str],
        NewTexts: list[str]
) -> etree.ElementTree:
    """Replace multiple texts in XML elements.

    Args:
        XMLTree: Input ElementTree
        OldTexts: List of texts to replace
        NewTexts: List of new texts

    Returns:
        Modified ElementTree
    """
    if XMLTree is not None:
        for item in XMLTree.iter():
            if item.text is not None:
                for i, ot in enumerate(OldTexts):
                    item.text = item.text.replace(ot, NewTexts[i])
    return XMLTree


def ReplaceImageInWordFolder(
        SourceFolder: str,
        OldImageFile: str,
        NewImageFile: str
) -> None:
    """Replace an image in a Word document folder.

    Args:
        SourceFolder: Word document folder path
        OldImageFile: Existing image filename
        NewImageFile: New image file path
    """
    old_file = os.path.join(SourceFolder, 'word', 'media', OldImageFile)

    with open(NewImageFile, 'rb') as file:
        data = file.read()

    with open(old_file, 'rb+') as file:
        file.seek(0)
        file.write(data)
        file.truncate()


def ReplaceImagesInWordFolder(
        SourceFolder: str,
        OldImageFiles: list[str],
        NewImageFiles: list[str]
) -> None:
    """Replace multiple images in a Word document folder.

    Args:
        SourceFolder: Word document folder path
        OldImageFiles: List of existing image filenames
        NewImageFiles: List of new image file paths
    """
    for i, o in enumerate(OldImageFiles):
        old_file = os.path.join(SourceFolder, 'word', 'media', o)

        with open(NewImageFiles[i], 'rb') as file:
            data = file.read()

        with open(old_file, 'rb+') as file:
            file.seek(0)
            file.write(data)
            file.truncate()


def InsertValuesIntoTable(
        XMLTree: etree.ElementTree,
        Fields: list[str],
        Values: list[list[str]],
        Bookmark: str = None
) -> etree.ElementTree:
    """Insert values into a Word table.

    Args:
        XMLTree: Input ElementTree
        Fields: List of field names
        Values: List of records to insert
        Bookmark: Optional bookmark name

    Returns:
        Modified ElementTree
    """
    for item in XMLTree.iter():
        if GetXMLTagWithoutNS(item.tag) == 'tbl':
            BookmarkCheck = Bookmark is None
            if not BookmarkCheck:
                for element in item.iter():
                    if GetXMLTagWithoutNS(element.tag) == 'bookmarkStart':
                        for k in element.attrib:
                            if (GetXMLTagWithoutNS(k) == 'name' and
                                    element.attrib.get(k) == Bookmark):
                                BookmarkCheck = True

            if BookmarkCheck:
                secondRow = None
                rowNumber = 0

                for element in item:
                    if GetXMLTagWithoutNS(element.tag) == 'tr':
                        rowNumber += 1
                        if rowNumber == 2:
                            secondRow = copy.deepcopy(element)
                            ns = GetXMLTagNamespace(element.tag)
                            elns = ns[1:len(ns) - 1]
                            map = list(item.nsmap.keys())[
                                list(item.nsmap.values()).index(elns)
                            ]
                        if rowNumber > 1:
                            item.remove(element)

                if secondRow is not None:
                    rowNumber = len(item.getchildren()) - 1
                    for v in Values:
                        replacedRow = copy.deepcopy(secondRow)
                        replacedRow = ReplaceTexts(replacedRow, Fields, v)

                        for i in replacedRow.iter():
                            for att in i.attrib:
                                if GetXMLTagWithoutNS(att) in ('paraId', 'editId'):
                                    i.set(att, uuid.uuid4().hex[:8].upper())

                            if GetXMLTagWithoutNS(i.tag) == 'AlternateContent':
                                anchorId = uuid.uuid4().hex[:8].upper()
                                for j in i.iter():
                                    for att in j.attrib:
                                        if GetXMLTagWithoutNS(att) == 'anchorId':
                                            j.set(att, anchorId)

                            elif GetXMLTagWithoutNS(i.tag) == 'docPr':
                                for att in i.attrib:
                                    if GetXMLTagWithoutNS(att) == 'id':
                                        id = str(int(uuid.uuid4().hex[:8], base=16))
                                        while len(id) < 9:
                                            id = '1' + id
                                        while len(id) > 9:
                                            id = id[:len(id) - 1]
                                        i.set(att, id)

                            elif GetXMLTagWithoutNS(i.tag) == 'roundrect':
                                for att in i.attrib:
                                    if GetXMLTagWithoutNS(att) == 'id':
                                        id = str(int(uuid.uuid4().hex[:3], base=16))
                                        while len(id) < 4:
                                            id = '0' + id
                                        while len(id) > 4:
                                            id = id[:len(id) - 1]
                                        i.set(att, '_x0000_s' + id)
                                    elif GetXMLTagWithoutNS(att) == 'gfxdata':
                                        i.attrib.pop(att)

                        rowNumber += 1
                        item.insert(rowNumber, replacedRow)
    return XMLTree


def ChangeGraphicBackColor(
        XMLTree: etree.ElementTree,
        BackColor: str,
        Field: str = None,
        Bookmark: str = None
) -> etree.ElementTree:
    """Change background color of a graphic object.

    Args:
        XMLTree: Input ElementTree
        BackColor: New color value
        Field: Optional field name in the graphic
        Bookmark: Optional bookmark name

    Returns:
        Modified ElementTree
    """
    for item in XMLTree.iter():
        if GetXMLTagWithoutNS(item.tag) == 'graphic':
            BookmarkCheck = Bookmark is None
            if not BookmarkCheck:
                for element in item.iter():
                    if GetXMLTagWithoutNS(element.tag) == 'bookmarkStart':
                        for k in element.attrib:
                            if (GetXMLTagWithoutNS(k) == 'name' and
                                    element.attrib.get(k) == Bookmark):
                                BookmarkCheck = True

            FieldCheck = Field is None
            if not FieldCheck:
                for element in item.iter():
                    if (GetXMLTagWithoutNS(element.tag) == 't' and
                            element.text is not None and
                            element.text.find(Field) > -1):
                        FieldCheck = True

            if BookmarkCheck and FieldCheck:
                for element in item.iter():
                    if GetXMLTagWithoutNS(element.tag) == 'spPr':
                        ln = None
                        for t in element:
                            ns = GetXMLTagNamespace(t.tag)
                            if GetXMLTagWithoutNS(t.tag) == 'ln':
                                ln = copy.deepcopy(t)
                            if GetXMLTagWithoutNS(t.tag) in ('solidFill', 'noFill', 'ln'):
                                element.remove(t)

                        elns = ns[1:len(ns) - 1]
                        map = list(item.nsmap.keys())[
                            list(item.nsmap.values()).index(elns)
                        ]
                        s = f'<solidFill xmlns:{map}="{elns}"><srgbClr val="{BackColor}"/></solidFill>'
                        s = s.replace('<', f'<{map}:')
                        s = s.replace(f'<{map}:/', f'</{map}:')
                        solidFill = etree.fromstring(s)
                        element.append(solidFill)

                        if ln is not None:
                            element.append(ln)

                        inline = item.getparent()
                        for att in inline.attrib:
                            if GetXMLTagWithoutNS(att) == 'anchorId':
                                anchorId = inline.attrib.get(att)

                                for r in XMLTree.iter():
                                    if GetXMLTagWithoutNS(r.tag) in ('roundrect', 'shape'):
                                        for att in r.attrib:
                                            if GetXMLTagWithoutNS(att) == 'anchorId':
                                                if r.attrib.get(att) == anchorId:
                                                    r.set('fillcolor', '#' + BackColor.lower())
                            elif GetXMLTagWithoutNS(att) == 'gfxdata':
                                inline.attrib.pop(att)

    return XMLTree


def ChangeGraphicEffect(
        XMLTree: etree.ElementTree,
        StyleTags: list[str],
        ReplacedStyles: list[str],
        Field: str = None,
        Bookmark: str = None
) -> etree.ElementTree:
    """Change style of a graphic object.

    Args:
        XMLTree: Input ElementTree
        StyleTags: List of style tags to replace
        ReplacedStyles: List of new style XML strings
        Field: Optional field name in the graphic
        Bookmark: Optional bookmark name

    Returns:
        Modified ElementTree
    """
    for item in XMLTree.iter():
        if GetXMLTagWithoutNS(item.tag) == 'graphic':
            BookmarkCheck = Bookmark is None
            if not BookmarkCheck:
                for element in item.iter():
                    if GetXMLTagWithoutNS(element.tag) == 'bookmarkStart':
                        for k in element.attrib:
                            if (GetXMLTagWithoutNS(k) == 'name' and
                                    element.attrib.get(k) == Bookmark):
                                BookmarkCheck = True

            FieldCheck = Field is None
            if not FieldCheck:
                for element in item.iter():
                    if (GetXMLTagWithoutNS(element.tag) == 't' and
                            element.text is not None and
                            element.text.find(Field) > -1):
                        FieldCheck = True

            if BookmarkCheck and FieldCheck:
                for element in item.iter():
                    if GetXMLTagWithoutNS(element.tag) == 'spPr':
                        for t in element:
                            ns = GetXMLTagNamespace(t.tag)
                            if GetXMLTagWithoutNS(t.tag) in StyleTags:
                                element.remove(t)

                        for i, st in enumerate(StyleTags):
                            elns = ns[1:len(ns) - 1]
                            map = list(item.nsmap.keys())[
                                list(item.nsmap.values()).index(elns)
                            ]
                            s = ReplacedStyles[i].replace(
                                f'<{st}',
                                f'<{st} xmlns:{map}="{elns}"'
                            )
                            s = s.replace('<', f'<{map}:')
                            s = s.replace(f'<{map}:/', f'</{map}:')
                            e = etree.fromstring(s)
                            element.insert(len(element.getchildren()), e)

    return XMLTree


def ReplaceTextsInHeaders(
        SourceFolder: str,
        OldTexts: list[str],
        NewTexts: list[str]
) -> None:
    """Replace texts in header files.

    Args:
        SourceFolder: Word document folder path
        OldTexts: List of texts to replace
        NewTexts: List of new texts
    """
    Headers = glob.glob(os.path.join(SourceFolder, 'word', 'header*.xml'))
    for header in Headers:
        xml = LoadXMLFile(header)
        xml = ReplaceTexts(xml, OldTexts, NewTexts)
        SaveXMLToFile(xml, header)


def ReplaceTextsInFooters(
        SourceFolder: str,
        OldTexts: list[str],
        NewTexts: list[str]
) -> None:
    """Replace texts in footer files.

    Args:
        SourceFolder: Word document folder path
        OldTexts: List of texts to replace
        NewTexts: List of new texts
    """
    Footers = glob.glob(os.path.join(SourceFolder, 'word', 'footer*.xml'))
    for footer in Footers:
        xml = LoadXMLFile(footer)
        xml = ReplaceTexts(xml, OldTexts, NewTexts)
        SaveXMLToFile(xml, footer)


def remove_all_files(user_directory: str, file_to_keep: str) -> None:
    """Remove all files in directory except specified one.

    Args:
        user_directory: Directory path
        file_to_keep: Filename to keep
    """
    for filename in os.listdir(user_directory):
        file_path = os.path.join(user_directory, filename)
        if os.path.isfile(file_path) and filename not in file_to_keep:
            os.remove(file_path)
            print(f'Removed {file_path}')
        else:
            print(f'Keeping {file_path}')


def generate_word_with_info(
        tag_name: list[str],
        user_report_info: list[str],
        image_name: list[str],
        user_report_picture: list[str],
        user_directory: str,
        fields_matched: list[list[list[str]]],
        fields_benchmark_name: list[list[tuple[str, str]]],
        phone: str,
        name: str
) -> None:
    """Generate Word document with provided information.

    Args:
        tag_name: List of tags to replace
        user_report_info: List of replacement values
        image_name: List of image filenames
        user_report_picture: List of image file paths
        user_directory: Output directory
        fields_matched: Table data to insert
        fields_benchmark_name: Table field names
        phone: Phone number suffix for filename
    """
    folder_word = os.path.join(user_directory, 'Tree')
    UnzipWordFile(r'D:\WebSites\ERS\FileAG\Report.docx', folder_word)
    tree_path = os.path.join(folder_word, 'word')

    ReplaceTextsInHeaders(
        folder_word,
        ['#name'],
        [name]
    )

    ReplaceImagesInWordFolder(folder_word, image_name, user_report_picture)

    tree = LoadXMLFile(os.path.join(tree_path, 'document.xml'))
    tree = ReplaceTexts(tree, tag_name, user_report_info)

    for index in range(len(fields_matched)):
        tree = InsertValuesIntoTable(
            tree,
            fields_benchmark_name[index][0][1],
            fields_matched[index][0],
            fields_benchmark_name[index][0][0]
        )
        tree = InsertValuesIntoTable(
            tree,
            fields_benchmark_name[index][1][1],
            fields_matched[index][1],
            fields_benchmark_name[index][1][0]
        )

    SaveXMLToFile(tree, os.path.join(tree_path, 'document.xml'))
    ZipWordFolder(
        folder_word,
        os.path.join(user_directory, f'Report{phone}.docx')
    )
    CovertDocxToPDF(
        os.path.join(user_directory, f'Report{phone}.docx'),
        os.path.join(user_directory, 'Report.pdf')
    )
    remove_all_files(user_directory, ["Report.pdf"])
