from zotero import *

###############################################################################
# Usage examples
# Create a series of items

def itemCreationTest():
    with zotero() as z:
        # First create a standalone note (unrelated to next entry)
        z.addNote(text='This is the text of a standalone note', parent=None)

        # Create library item without unicode first
        book0 = book(
                abstractNote='''This is the abstract''',
                accessDate='2013-01-01',
                archive='Archive',
                archiveLocation='Archive Location',
                callNumber='Call 1234',
                creators=[
                            #author('Иван Иванович', 'Иванов'),
                            author('Author First 2', 'Author Last 2'),
                            author('Author First 3', 'Author Last 3'),
                            contributor('Contributor First 1', 'Contributor Last 1'),
                            contributor('Contributor First 2', 'Contributor Last 2'),
                            contributor('Contributor First 3', 'Contributor Last 3'),
                            editor('Editor First 1', 'Editor Last 1'),
                            editor('Editor First 2', 'Editor Last 2'),
                            editor('Editor First 3', 'Editor Last 3'),
                            seriesEditor('S. Editor First 1', 'S. Editor Last 1'),
                            seriesEditor('S. Editor First 2', 'S. Editor Last 2'),
                            seriesEditor('S. Editor First 3', 'S. Editor Last 3'),
                            translator('Translator First 1', 'Translator Last 1'),
                            translator('Translator First 2', 'Translator Last 2'),
                            translator('Translator First 3', 'Translator Last 3'),
                    ],
                date='1234-12-34',
                edition='1st Edition',
                #extra='Extras', # Default value None -> ''
                ISBN='12345678x',
                language='SomeLanguage',
                libraryCatalog='library catalog',
                numberOfVolumes='10 Volumes',
                numPages='3141',
                place='Publisher place',
                publisher='Publisher',
                rights='Rights',
                series='Series',
                seriesNumber='Series Number 1',
                shortTitle='A short title',
                title='Item with file attachments',
                url='http://a.b.c',
                volume='12')

        # Add the book to the library
        # Attachments are linked or imported, see mode argument of attachFile
        report = z.addItem(
                book0,
                # to test, add files to folder. If not, comment out next line
                attachmentMode='import', # the default
                attachmentList=['book toc.pdf', 'book chapter 2.pdf', 'Test.png'],
                tags=['defaultTag_type0', ('tag2', 0), ('tag_type_1', 1)],
                notes=['A simple text note.', 'another note'])



        # Create library item and populate the fields
        book1 = book(
                abstractNote='''
This is a long abstract with some unicode content.
По оживлённым берегам
Громады стройные теснятся
Дворцов и башен; корабли
Толпой со всех концов земли
К богатым пристаням стремятся;
    子曰：「學而時習之，不亦說乎？有朋自遠方來，不亦樂乎？
    人不知而不慍，不亦君子乎？」
    有子曰：「其為人也孝弟，而好犯上者，鮮矣；
    不好犯上，而好作亂者，未之有也。君子務本，本立而道生。
    孝弟也者，其為仁之本與！」
''',
                accessDate='2013-01-01',
                archive='Archive',
                archiveLocation='Archive Location',
                callNumber='Call 1234',
                creators=[
                            author('Иван Иванович', 'Иванов'),
                            author('AAuthor First 2', 'Author Last 2'),
                            author('Author First 3', 'Author Last 3'),
                            contributor('Contributor First 1', 'Contributor Last 1'),
                            contributor('Contributor First 2', 'Contributor Last 2'),
                            contributor('Contributor First 3', 'Contributor Last 3'),
                            editor('Editor First 1', 'Editor Last 1'),
                            editor('Editor First 2', 'Editor Last 2'),
                            editor('Editor First 3', 'Editor Last 3'),
                            seriesEditor('S. Editor First 1', 'S. Editor Last 1'),
                            seriesEditor('S. Editor First 2', 'S. Editor Last 2'),
                            seriesEditor('S. Editor First 3', 'S. Editor Last 3'),
                            translator('Translator First 1', 'Translator Last 1'),
                            translator('Translator First 2', 'Translator Last 2'),
                            translator('Translator First 3', 'Translator Last 3'),
                    ],
                date='1234-12-34',
                edition='1st Edition',
                #extra='Extras', # Default value None -> ''
                ISBN='12345678x',
                language='Русский',
                libraryCatalog='library catalog',
                numberOfVolumes='10 Volumes',
                numPages='3141',
                place='Publisher place',
                publisher='Publisher',
                rights='Rights',
                series='Series',
                seriesNumber='Series Number 1',
                shortTitle='A short title',
                title='Item with linked attachments',
                url='http://a.b.c',
                volume='12')

        # Add the book to the library
        # Attachments are linked or imported, see mode argument of attachFile
        report = z.addItem(
                book1,
                # to test, add files to folder. If not, comment out next line
                attachmentMode='link', # 'import' is the default
                attachmentList=['book toc.pdf', 'book chapter 2.pdf', 'Test.png', 'sample-bitmap.png'],
                tags=['defaultTag_type0', ('tag2', 0), ('tag_type_1', 1)],
                notes=[ 'A simple text note.',
                        'A note with unicode Без муки нет науки.',
                        # A note with html
                        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"> <head> <title>HTML Note</title> <style type="text/css" media="all"> </style> </head> <body> <h1>Heading 1 (h1)</h1> <h2>Heading 2 (h2)</h2> <h3>Heading 3 (h3)</h3> <h4>Heading 4 (h4)</h4> <h5>Heading 5 (h5)</h5> <h6>Heading 6 (h6)</h6> </body> </html>'
                ])



        if yamlExists: # save report for each entry
            with open('report.yaml', 'w') as f:
                printd( yaml.dump(report))
                yaml.dump(report, f)


        # Add an article
        article = journalArticle(
                abstractNote='This is a long abstract for an article. It has some unicode'*5,
                accessDate='2013-09-09',
                archive='Article archive',
                archiveLocation='Nowhere',
                callNumber='123 Article',
                creators=[
                            author('Иван Иванович', 'Иванов'),
                            author('AAuthor First 2', 'Author Last 2'),
                            author('Author First 3', 'Author Last 3'),
                            contributor('Contributor First 1', 'Contributor Last 1'),
                            contributor('Contributor First 2', 'Contributor Last 2'),
                            contributor('Contributor First 3', 'Contributor Last 3'),
                            editor('Editor First 1', 'Editor Last 1'),
                            editor('Editor First 2', 'Editor Last 2'),
                            editor('Editor First 3', 'Editor Last 3'),
                            reviewedAuthor('Reviewed Author First 1', 'Reviewed AuthorLast 1'),
                            reviewedAuthor('Reviewed Author First 2', 'Reviewed AuthorLast 2'),
                            reviewedAuthor('Reviewed Author First 3', 'Reviewed AuthorLast 3'),
                            translator('Translator First 1', 'Translator Last 1'),
                            translator('Translator First 2', 'Translator Last 2'),
                            translator('Translator First 3', 'Translator Last 3'),
                    ],
                date='1234-45-79',
                DOI='10.1.1.168.4008',
                extra='Extra notes for article',
                #ISSN='',
                issue='Issue 4',
                journalAbbreviation='ABC',
                language='Language',
                libraryCatalog='No Catalog',
                pages='1234564645',
                publicationTitle='Some Example Article',
                rights='Unknown',
                series='Article Series',
                seriesText='Series Text',
                seriesTitle='Series Title',
                shortTitle='A short title',
                title='The real title',
                url='citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.168.4008',
                volume='Vol 123')

        report = z.addItem(
                article,
                attachmentList=['book toc.pdf', 'book chapter 2.pdf'],# 'cover1.png', 'cover2.bmp'],
                tags=['tag1_0', ('tag2_0', 0), ('tag3_1', 1)],
                notes=['A simple text note.', 'Без муки нет науки.',
                '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"> <head> <title>HTML Note</title> <style type="text/css" media="all"> </style> </head> <body> <h1>Heading 1 (h1)</h1> <h2>Heading 2 (h2)</h2> <h3>Heading 3 (h3)</h3> <h4>Heading 4 (h4)</h4> <h5>Heading 5 (h5)</h5> <h6>Heading 6 (h6)</h6> </body> </html>'])


def interfaceTest():
    '''Get currently selected items and their attachments '''
    with zotero() as z:
        selectedItems = z.getSelectedItems()

        for itemID, item, isRegularItem in selectedItems:
            print('#' * 5)
            printd(itemID, item, isRegularItem)
            attachments = z.getAttachmentInfo(itemID)
            if attachments != None:
                for ID, att, fileURL in attachments:
                    print('Attachments', ID, att, fileURL)


def testZoteroConnection():
    '''Make sure the debug bridge is working'''
    with zotero() as z:
        z.testZoteroConnection()



if __name__=='__main__':
    testZoteroConnection()
    interfaceTest() # get currently selected item
    itemCreationTest() # add a few items to Zotero
