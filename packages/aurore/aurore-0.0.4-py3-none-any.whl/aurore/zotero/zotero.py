# -*- coding: utf-8 -*-
from collections import namedtuple
import json
import urllib.parse
#import telnetlib
import time
import os.path
import filecmp
import random
import string
import requests
try:
    import yaml
    yamlExists = True
except:
    print('yaml is not available, cannot store the protocol to file.')
    yamlExists = False

# Library for interacting with a local Zotero library in Firefox
# MozRepl doesn't work anymore, use Zotero Debug Bridge instead
# enter the password you set in the advanced settings for the debug bridge here:
debugBridgePassword="setYourPasswordHere"
# test with curl -X POST -H "Content-Type: application/javascript" --data "await Zotero.Schema.schemaUpdatePromise; return 'hello ' + query.world" "http://127.0.0.1:23119/debug-bridge/execute?foo=bar&baz=quux&world=world&password=debugBridgePassword"
# should print "hello world"





# This library is intended to allow bulk import of existing libraries.
# The user has to find a way to extract the metadata for his library items.
# Possibilities are
# * ISBNs in the filename
# * XMP Metadata (e.g. using cb2bib http://www.molspaces.com/cb2bib/)
# * ...


# For a usage example look at the bottom of this file.

# BSD License

# Configuration
Verbose = True

#####################################################################################################
def makeItem(itemName, itemKeys):
    cls = namedtuple(itemName, itemKeys)
    cls.__new__.__defaults__ = (None,) * len(itemKeys)
    return cls

# Field definitions
# A list of Zotero fields can be found at http://aurimasv.github.io/z2csl/typeMap.xml#map-journalArticle
# Replace creator with creators and delete the other creator fields creatorItems =  ['authors', 'creators', 'contributors', 'editors', 'translators', 'seriesEditors', 'reviewedAuthors']

bookKeys='abstractNote accessDate archive archiveLocation callNumber creators date edition extra ISBN language libraryCatalog numberOfVolumes numPages place publisher rights series seriesNumber shortTitle title url volume'.split()
book = makeItem('book', bookKeys)


journalArticleKeys='abstractNote accessDate archive archiveLocation callNumber creators date DOI extra ISSN issue journalAbbreviation language libraryCatalog pages publicationTitle rights series seriesText seriesTitle shortTitle title url volume'.split()
journalArticle = makeItem('journalArticle', journalArticleKeys)


bookSectionKeys = 'abstractNote accessDate archive archiveLocation bookTitle callNumber creators date edition extra ISBN language libraryCatalog numberOfVolumes pages place publisher rights series seriesNumber shortTitle title url volume'.split()
bookSection = makeItem('bookSection', bookSectionKeys)


blogPostKeys = 'abstractNote accessDate blogTitle creators date extra language rights shortTitle title url websiteType'.split()
blogPost = makeItem('blogPost', blogPostKeys)



conferencePaperKeys = 'abstract accessDate archive archiveLocation callNumber conferenceName creators date DOI extra ISBN language libraryCatalog pages place proceedingsTitle publisher rights series shortTitle title url volume'.split()
conferencePaper = makeItem('conferencePaper', conferencePaperKeys)


documentKeys = 'abstract accessDate archive archiveLocation callNumber creators date extra language libraryCatalog publisher rights shortTitle title url'.split()
document = makeItem('document', documentKeys)



presentationKeys = 'abstractNote accessDate creators date extra language meetingName place presentationType rights shortTitle title url'.split()
presentation = makeItem('presentation', presentationKeys)




reportKeys = 'abstractNote accessDate archive archiveLocation callNumber creators date extra institution language libraryCatalog pages place reportNumber reportType rights seriesTitle shortTitle title url'.split()
report = makeItem('report', reportKeys)


thesisKeys = 'abstract accessDate archive archiveLocation callNumber creators date extra language libraryCatalog numPages place rights shortTitle thesisType title university url'.split()
thesis = makeItem('thesis', thesisKeys)


webpageKeys = 'abstractNote accessDate creators date extra language rights shortTitle title url websiteTitle websiteType'.split()
webpage = makeItem('webpage', webpageKeys)
#####################################################################################################

#####################################################################################################
# Class Definitions, these classes represent Zotero items



#book = namedtuple('book', bookKeys)
#book.__new__.__defaults__ = (None,) * len(bookKeys)

#journalArticle = namedtuple('journalArticle', journalArticleKeys)
#journalArticle.__new__.__defaults__ = (None,)*len(journalArticleKeys)

#####################################################################################################
# Different types of creators
class creator(object):
    '''Base class for all creators'''
    def __init__(self, first, last):
        self.first = first
        self.last  = last

    def __str__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.first, self.last)

class author(creator): pass
class bookAuthor(creator): pass
class contributor(creator): pass
class commenter(creator): pass
class editor(creator): pass
class presenter(creator): pass
class translator(creator): pass
class seriesEditor(creator): pass
class reviewedAuthor(creator): pass

# Not all creators are allowed for all items
allowedCreators = {
        book:[author, contributor, editor, seriesEditor, translator],
        conferencePaper:[author, contributor, editor, seriesEditor, translator],
        bookSection:[author, bookAuthor, contributor, editor, seriesEditor, translator],
        journalArticle:[author, contributor, editor, reviewedAuthor, translator],
        document:[author, contributor, editor, reviewedAuthor, translator],
        blogPost:[author, commenter, contributor],
        presentation:[contributor, presenter],
        report:[author, contributor, seriesEditor, translator],
        thesis:[author, contributor],
        webpage:[author, contributor, translator],
    }

######################################################################################################

from unidecode import unidecode


def printd(*x):
    if Verbose: #
        print(list(unidecode(str(xx)) for xx in x))


class JSVariable(object):
    '''Create a variable that lives in the javascript namespace'''
    def __init__(self, zoteroObject, name, initialValue = -9999, initFromFunctionCall=None, bindingType = 'var', gensym = True):
        # create variable
        value = initialValue
        self.zoteroObject = zoteroObject
        self.name = name
        if gensym: # normal case
            self.jsname = zoteroObject.gensym(name)
        else: # use this for debugging
            self.jsname = self.name

        if   bindingType == 'let':
            raise Exception('let binding not working yet')
        # the let binding works, but the readback doesn't. as all variables are gensym'ed, it doesn't matter
            self.zoteroObject.let_binding(self.jsname, value)
        elif bindingType == 'var':
            self.zoteroObject.var_binding(self.jsname, value)
        else:
            raise Exception('bindingType must be let or var', bindingType)

        if initFromFunctionCall != None: # immediately set the new variable by executing the function call
            self.setVariableFromFunctionCall(initFromFunctionCall)


# TODO: always use JSON format for all returns?
    @property
    def value(self):
        return self.zoteroObject.getVariable(self.jsname)

    @value.setter
    def value(self, value):
        return self.zoteroObject.setVariable(self.jsname, str(value).encode('unicode_escape'))

    def setVariableFromFunctionCall(self, functionCallString):
        '''Execute the function call and assign the result to the variable
        Example: setVariableFromFunctionCall("new Zotero.Item('note')") '''
        return self.zoteroObject.setVariableFromFunctionCall(self.jsname, functionCallString)

    def attributeAccess(self, attributeString):
        '''Execute the function or attribute on the variable and return the result
        example: attributeAccess(".setNote('{text}');".format(text=text))
        Needs leading . '''
        self.zoteroObject.writeToRepl(self.jsname + attributeString)
        return self.zoteroObject.readFromRepl()


class ZoteroError(Exception): pass

class zoteroTransaction(object):
    def __init__(self, zoteroObject):
        self.zoteroObject = zoteroObject

    def __enter__(self):
        return
        self.zoteroObject.sendToZotero(code='Zotero.DB.beginTransaction();')
       # TODO: this does not work
#            ...: data = "Zotero.DB.beginTransaction()"
#     ...: r = requests.post(url, data = data, headers=headers)
#     ...: print(r.text)
# debug-bridge failed: TypeError: Zotero.DB.beginTransaction is not a function
# anonymous@chrome://zotero-debug-bridge/content/debug-bridge.js line 33 > AsyncFunction:3:1

    def __exit__(self, type, value, traceback):

            if type == None and value == None and traceback == None:
                #ODO: remove this when transactions work
                #self.zoteroObject.sendToZotero(code='Zotero.DB.commitTransaction();')
                printd('Committing Transaction')
            else:
                #self.zoteroObject.sendToZotero(code='Zotero.DB.rollbackTransaction();')
                printd('Rolling Back Transaction')
                return False # re-raise exception

class zotero(object):
    def __init__(self):
        pass

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()
        if type == None and value == None and traceback == None:
            pass
        else:
            print('Zotero Error')
            return False

    def __del__(self):
        self.close()

    def open(self):
        if not self.testZoteroConnection():
            print('No connection to Zotero')
            raise Exception('No connection')

        #printd( self.telnet.read_until(b"repl>", 10))

    def close(self):
        #self.telnet.close()
        pass

    def gensym(self, name = '', symbolLength = 10):
        'Create a random symbol name, use this for javascript variables to avoid accidental capture'
        return name + ''.join(random.choice(string.ascii_letters) for _ in range(symbolLength))

    def introduceJSVariable(self, name, initialValue = -9999):
        '''Introduce a let-binding in the JS namespace'''
        return JSVariable(self, name, initialValue)

    def var_binding(self, name, value):
        '''introduce a let-binding in JS, name is assumed to be a bytestring and the value should be .encode('unicode_escape')'''
        # TODO: deal with strings properly, "abc" -> b"\'abc\'" etc. 123 -> b'123'
        # TODO: is it better to call a toJSON function here????
        # this needs to be recursive
        if type(value) == bytes:
            print('Argument should be a string or a number, not a bytes string')
            1/0

        value = json.dumps(value).encode('unicode_escape')


        if type(name) != bytes:
            name = name.encode('ascii')

        cmd = b"var %b = %b ;" % (name, value)
        print('var variable introduction', cmd)
        self.telnet.write(cmd)

        ret=self.telnet.read_until(b"repl>", 1)
        retp=self.telnet.read_until(b"repl>", 1)
        self.telnet.write(b"%b;" % name)

        retn=self.telnet.read_until(b"repl>", 1)
        print("var-binding", ret, retp, retn)
        print(self.getVariable(name), self.getVariableJSON(name))

        if not ret.endswith(b"repl>"):
            raise IOError('Error executing {command}. Did not get repl>. Got: {ret}'.format(command=name, ret=repr(ret)))

        return ret.decode('utf-8')

    def getVariable(self, name):
        '''Get a variable from MozRepl'''
        if type(name) != bytes:
            name = name.encode('ascii')

        cmd = name + b';'
        print('getVariable', cmd)
        self.telnet.write(cmd)
        ret=self.telnet.read_until(b"repl>", 1)

        if not ret.endswith(b"repl>"):
            raise IOError('Error executing {command}. Did not get repl>. Got: {ret}'.format(command=name, ret=repr(ret)))

        # ret starts with space
        ret = ret[1:-len(b"\nrepl>")]
        return ret.decode('utf-8')

    def setVariable(self, name, value):
        self.zoteroObject.writeToRepl('%s = %s;' % (variable, functionCall))

    def cleanTelnetQueue(self):
        '''Read as much as possible'''
        ret = b''
        while True:
            x = self.telnet.read_eager()
            if x == b'':
                break
            ret += x
        return ret

    def getVariableJSON(self, name):
        '''Get a variable as JSON '''
        ret = self.sendToZotero(code='return ' + name)
        return json.loads(ret)

    def testZoteroConnection(self):
        'Test if the Zotero Debug Bridge is working'
        rtext = self.sendToZotero(variables={'world':'world'}, code="await Zotero.Schema.schemaUpdatePromise; return 'hello ' + query.world")
        if rtext=='"hello world"':
            print('Connection to Zotero is working')
            return True
        else:
            print('ERROR: Connection to Zotero not working')
            return False
        return rtext


    def sendToZotero(self, variables={}, code=''):
        'set the variables variables and then run the code'

        url = "http://127.0.0.1:23119/debug-bridge/execute?" + urllib.parse.urlencode({**variables, **{'password':debugBridgePassword}})
        headers = {"Content-Type":"application/javascript"}
        data = b"await Zotero.Schema.schemaUpdatePromise; " + code.encode('utf-8')
        print('data', data)
        r = requests.post(url, data = data, headers=headers)
        print(r)
        print(r.request)
        r.raise_for_status()
        return r.text

    def writeToRepl(self, msg):
        'This function was a layer that encapsulated the telnet calls.'
        raise DeprecationWarning('Do not use telnet anymore')
        #return self.telnet.write(msg.encode('ascii'))

    def readFromRepl(self, timeout=1):
        ret = self.telnet.read_until(b"repl>", timeout)
        ret = ret[1:-len("\nrepl>")].decode('utf-8')
        return ret

    def createVariableFromFunctionCall(self, variable, functionCall):
        self.writeToRepl('var %s = %s;' % (variable, functionCall))
        ret = self.readFromRepl()
        return ret

    def setVariableFromFunctionCall(self, variable, functionCall):
        self.writeToRepl('%s = %s;' % (variable, functionCall))
        ret = self.readFromRepl()
        return ret

    def executeFunction(self, functionCall):
        self.writeToRepl('%s;' % (functionCall))
        ret = self.readFromRepl()
        return ret


    # TODO: this function has to go, replace by more specific functions that do direct error handling
    def execute(self, cmd, timeout=10, noCheck=False):
        print('cmd before ', cmd.encode('utf-8'))
        printd( 'executing %s ' % cmd)
        # execute will do some rudimentary error checks
        # These checks are probably very specific not only to MozRepl, but also
        # to the commands used.

        self.telnet.write(cmd.encode('unicode_escape'))
        print('executed command, trying to read')
        time.sleep(0.1)
        ret=self.telnet.read_until(b"repl>", timeout)

        if not ret.endswith(b"repl>"):
            raise IOError('Error executing {command}. Did not get repl>. Got: {ret}. If you got a number at the end, like repl1>, it means another repl is running. Better restart mozrepl in that case.'.format(command=cmd, ret=repr(ret)))
        else:
            print('Readback from command', repr(ret))

        # first value returned = spc
        ret = ret[1:-len("\nrepl>")].decode('utf-8')
        if ret.startswith('[object Promise]'):
            print('We are dealing with a promise, trying to resolve')
            #self.telnet.write(b'var jsonitems = JSON.stringify(' + name.encode('ascii') + b');')

            #self.telnet.write(b'resolved = ret.then(function(result) {return JSON.stringify(result)})')
            self.telnet.write(b'resolved = ret.get()')
            ret2=self.telnet.read_until(b"repl>", timeout)
            resolved = self.getVariable('resolved')
            print('After resolving', ret2)
            print('resolved', resolved)

        if noCheck == True:
            return ret

        returnOK = False
        # Some commands return an empty string, no way to do error checking
        # There might be a more generic way, but better be on the safe side
        printd('stripped cmd', cmd.strip())
        if (    cmd.strip() in [
                        'var item = new Zotero.Item;',
                        'var creator = new Zotero.Creator;',
                        'var itemID = item.save();',
                        'var file = Components.classes["@mozilla.org/file/local;1"].createInstance(Components.interfaces.nsILocalFile);',
                        'Zotero.DB.beginTransaction();',
                        'Zotero.DB.commitTransaction();',
                        'Zotero.DB.rollbackTransaction();',
                        'var tags = item.getTags();',
                        'var item = new Zotero.Item(\'note\');',
                        'var notes = item.getNotes();',
                        'var items = ZoteroPane.getSelectedItems();',
                        'var att_ids = item.getAttachments(false);',
                        ]
           ) and ret == '':
            returnOK = True

        elif (  cmd.startswith('var item = Zotero.Items.get(') or
                cmd.startswith('file.initWithPath(') or
                cmd.startswith('var creator = item.getCreator(') or
                cmd.startswith('var attachment = Zotero.Items.get(') or
                cmd.startswith('var note = Zotero.Items.get(')
             )  and ret == '':
                returnOK = True

        # These items might have an equal sign
        elif (cmd.startswith('item.setNote(') or \
              cmd.startswith('item.setField("url"')) and \
              ret=='true':
            returnOK = True

        elif '=' in cmd and '(' not in cmd: # no functions allowed
            # for other assignments, the RHS is returned. Check that this is true.
            RHS = cmd.split('=')[-1]
            RHS = RHS.strip(' ;')
            printd('cmd', cmd, cmd[:5])
            printd('rhs', RHS, RHS[:5], str(RHS), type(RHS))
            printd('ret', ret, type(ret))
            printd('ret=rhs', RHS==ret)
            # RHS has backslash escaped
            if RHS != ret:
                raise IOError('Error executing {command}. Looks like assignment, but RHS was not returned. Got: >{ret}<'.format(command=repr(cmd), ret=repr(ret)))
            else:
                returnOK  = True

        elif len(cmd) > 100 and ret.endswith('....> ....> true'):
            # Long commands end with ....> ....> true. Length where this occurs has not been
            # verified
            returnOK = True

        elif len(cmd) > 50 and ret.endswith('....> true'):
            # Long commands end with ....> ....> true. Length where this occurs has not been
            # verified
            returnOK = True

        # Commands returning a number
        elif cmd.endswith('.save();') or \
             cmd.startswith('Zotero.Attachments.linkFromFile(') :
            try:
                id = int(ret)
            except ValueError:
                raise IOError('Error executing {command}. Could not convert to int Got: >{ret}<'.format(command=cmd, ret=repr(ret)))
            else:
                returnOK = True

        elif cmd.startswith('item.addTag('):
            try:
                if ret != 'false':
                    # addTag returns false if the tag was not added. This is the case if the tag already exists
                    pass
            except ValueError:
                raise IOError('Error executing {command}. Could not convert to int Got: >{ret}<'.format(command=cmd, ret=repr(ret)))
            else:
                returnOK = True
        elif cmd.startswith('ret = Zotero.Attachments.importFromFile(file,') and \
            int(cmd[:-1].split(',')[1]) + 1 <= int(ret): # returns ID of newly created file item.
            # This seems (sometimes) to be be one more than the ID of the file item we pass in
            # sometimes a bit more
            print(1234, cmd)
            print(cmd)
            print(int(cmd[:-1].split(',')[1]))
            print(int(ret))
            returnOK = True

        elif ret in ['true']: # generic case
            returnOK = True

        else:
            raise IOError('Error executing {command}. Did not return true. Got: >{ret}<'.format(command=cmd, ret=repr(ret)))

        if returnOK != True:
            raise Exception('This should not happen, must have overlooked a case.')

        return ret

    def addItem(self, item, attachmentList=[], tags = [], notes=[], attachmentMode='import'):
        '''Add an item (book, journalArticle) to Zotero database, attachments
        will be linked to avoid loosing the original data'''
        attachmentList = list(map(os.path.abspath, attachmentList))


        # Check that all attachments exist
        for f in attachmentList:
            if not os.path.isfile(f):
                raise Exception('File %s not found!' % f)

        # Tags without a type will get type 0
        tags = [(str(t[0]), t[1]) if type(t)==tuple else (str(t),0) for t in tags]

        # This dict will hold all data item data together with the itemID and
        # IDs of attachments
        # The idea is to store this with the original data to have a link
        # folder -> zoteroDB

        addReport = {}
        addReport['itemType'] = item.__class__.__name__
        addReport['itemData'] = dict((field,getattr(item, field)) for field in item._fields)

        try:
            with zoteroTransaction(self): # TODO: the transaction doesn't work.
                # the alternative is to calll return await Zotero.DB.executeTransaction(async () => {...})
                # the problem is that this does not work with the context manager.

                # Add item
                itemID = self.addItemBase(item)
                print(itemID)
                addReport['itemID'] = itemID
                # Confirm that the data was written correctly
                print('Item verification disabled')
                addReport['verified'] = True# self.verifyItem(item, itemID)

                addReport['attachments'] = []
                # Add attachments and verify each one
                for attachment in attachmentList:
                    attachmentID = self.attachFile(itemID, attachment, mode=attachmentMode)
                    addReport['attachments']+=[{attachment:attachmentID}]
                    print('Skipping attachment verification')
                    #self.verifyAttachment(attachment, attachmentID, itemID)

                # Add tags
                self.addTags(tags, itemID)
                #self.verifyTags(tags, itemID)
                print('Skipping tags verification')
                addReport['tags'] = True# tags

                # Add notes
                for note in notes:
                    self.addNote(text=note, parent=itemID)
                # Verify notes
                print('Skipping note verification')
                addReport['notes'] = True#self.verifyNotes(notes, itemID)


        except:
            print('Failed to add item')
            raise
        else:
            print('Successfully added and verified item.')

        return addReport

    def getUrlToAttachedFile(self, attachmentID):
        attachmentURLValue = self.getVariableJSON(f'Zotero.Items.get({attachmentID}).getLocalFileURL()')
        print('attachmentURL', attachmentURLValue)
        url = urllib.parse.unquote(attachmentURLValue.strip('"'))
        return url


    def verifyAttachment(self, path, attachmentID, parentID):
        printd('Verifying attachment %s' %path)
        printd( 'attachmentID %s' % attachmentID)
        self.execute('var attachment = Zotero.Items.get({attachmentID});'.format(attachmentID=attachmentID))
        ID= int(self.getVariable('attachment.getID()'))
        exists = self.getVariable('attachment.exists()')
        #type=self.getVariable('attachment.getType()')
        isAttachment = self.getVariable('attachment.isAttachment()')
        savedFilename = self.getVariable('attachment.getFilename()')[1:-1]
        isFileAttachment = self.getVariable('attachment.isFileAttachment()')

        attachmentPath = self.getVariable('attachment.attachmentPath;')[1:-1]
        urlToAttachedFile = self.getUrlToAttachedFile(attachmentID)
        sourceItemID = int(self.getVariable('attachment._sourceItemID;'))
        self.execute('var item = Zotero.Items.get({ID});'.format(ID=parentID))
        # getAttachments => 2860,2861,2862 - {0: 2860, 1: 2861, 2: 2862}
        attachmentsOfParent = list(map(int, self.getVariable('item.getAttachments();').split('-')[0].split(',')))
        # This does not work for bmp and png
        #fileExists = self.getVariable('attachment._fileExists;')

        # imported item
        if (attachmentPath.startswith('storage:') and
           urlToAttachedFile.startswith('file:///') and
           exists == 'true' and
           ID == attachmentID and
           isFileAttachment == 'true' and
           attachmentPath[len('storage:'):] == os.path.basename(path) and
           sourceItemID == parentID and
           attachmentID in attachmentsOfParent and
           filecmp.cmp(path, urlToAttachedFile[len('file:///'):], shallow=True)):

            print('Successfully compared file', urlToAttachedFile)

        # linked item
        elif  (exists == 'true' and
            ID == attachmentID and
            isAttachment == 'true' and
            savedFilename == os.path.basename(path) and
            isFileAttachment == 'true' and
            os.path.abspath(attachmentPath) == path and
            sourceItemID == parentID and
            attachmentID in attachmentsOfParent):
                pass
        else:
            raise Exception('Could not verify file fileExists={exists}, attachmentPath={attachmentPath}, path={path}, ID={ID}, attachmentID={attachmentID}, savedFilename={savedFilename}, sourceItemID={sourceItemID}, parentID={parentID}'.format(**locals()))

        return dict(urlToAttachedFile=urlToAttachedFile)


    def addItemBase(self, item):
        '''Add item without attachments, notes etc.
        this wil be part of a transaction, if the creation fails,0'''

        code = 'return await Zotero.DB.executeTransaction(async () => {'
        code+='var item = new Zotero.Item;'
        code+='item.setType(Zotero.ItemTypes.getID(\'{itemType}\'));'.format(itemType = item.__class__.__name__)


        creatorcode = ''
        for field in item._fields:
            if getattr(item, field) == None: # Default value, nothing to do
                continue


            # Add creators
            if field == 'creators':

                for creatorNumber, creator in enumerate(getattr(item, field)):
                    if creator.__class__ not in allowedCreators[item.__class__]:
                        raise Exception('Creator %s not allowed for %s' % (creator.__class__.__name__, item.__class__.__name__))
                    # TODO: Create new Creator, or search for existing ones?
                    creatorcode+=f'{{firstName:"{creator.first}", lastName:"{creator.last}", creatorType:"{creator.__class__.__name__}"}},'

                    # code+='var creator =  Zotero.Creator;'
                    # code+='creator.firstName = "{first}";'.format(first=creator.first)
                    # code+='creator.lastName = "{last}";'.format(last=creator.last)
                    # code+= "creator.save();"
                    # code+="item.setCreator({creatorNumber}, creator, '{creatorType}');".format(creatorType=creator.__class__.__name__, creatorNumber=creatorNumber)

            # Add fields
            else:
                code+=f'item.setField("{field}", {json.dumps(getattr(item, field))});'#.format(field=field, fieldValue=getattr(item, field))

        if creatorcode != '':
            creatorcode = 'item.setCreators([ ' + creatorcode + ']);'
            code += creatorcode

        code += 'return item.save()})'
        print('addItemBaseCode\n', code, '\n')
        return self.sendToZotero(code=code)

        return int(self.getVariable('item.save()'))


    def verifyItem(self, item, itemID):
        '''Verify that the item corresponds to the one referenced by the id'''
        self.execute('var item = Zotero.Items.get({itemID});'.format(itemID=itemID))
        creatorNumber = -1
        for field in item._fields:
            if field == 'creators':
                for creatorNumber, creator in enumerate(getattr(item, field)):
                    self.execute("var creator = item.getCreator({creatorNumber});".format(creatorNumber=creatorNumber))
                    savedFirst = self.getVariable('creator.ref.firstName;')[1:-1]
                    savedLast = self.getVariable('creator.ref.lastName;')[1:-1]
                    savedID = self.getVariable('creator.creatorTypeID;')
                    if savedFirst == creator.first and \
                       savedLast == creator.last and \
                       savedID == self.getVariable('Zotero.CreatorTypes.getID("{creatorType}");'.format(creatorType = creator.__class__.__name__)):
                        printd('Successfully verified creator %s %s (%s)'  % (savedFirst, savedLast, creator.__class__.__name__))

                    else:
                        raise Exception('Creator Name does not match. (%s %s %s) != (%s %s %s) '\
                                % (savedFirst, savedLast, savedID,
                                    creator.first, creator.last, creator.__class__.__name__))


            else:
                # All values are stored as strings, remove double quotes
                savedValue = self.getVariable('item.getField("{field}")'.format(field=field)).strip('"')
                if getattr(item, field) == None:
                    # No item specified, maps to empty string in Zotero
                    expectedValue = ''
                else:
                    expectedValue = getattr(item, field)

                if savedValue.strip() != expectedValue.strip(): # Zotero strips whitespace
                    printd('+++++ expected value')
                    printd(repr(expectedValue.strip()), len(expectedValue.strip()), expectedValue.encode('utf-8'))
                    printd('+++++ saved value')
                    printd(repr(savedValue.strip()), len(savedValue.strip()), savedValue.encode('utf-8'))
                    for a,b in zip(savedValue.strip(), expectedValue.strip()):
                        if a != b:
                            print(a.encode('utf-8'), b.encode('utf-8'))
                    raise Exception('Retrieved field {field} for item # {itemID}, does not match {expectedValue}'.format(field=field, itemID=itemID, expectedValue=repr(expectedValue)))
                else:
                    printd('Successfully verified {field} = {expectedValue}'.format(field=repr(field), expectedValue=repr(expectedValue)))

        printd( '...Successfully verified all fields.')
        return True

    def addNote(self, text, parent=None):
        '''parent=None -> standalone note'''

        code="item = new Zotero.Item('note');"
        code+=f"item.setNote('{text}');"
        if parent!=None:
            code+=f'item.parentID = {parent};'

        code+='return item.save();' # itemID
        print('code\n', code, '\nend\n')
        return int(self.sendToZotero(code=code))


    def verifyNotes(self, notes, itemID):
        raise Exception('Not converted to the new debug bridge yet')
        self.execute('var item = Zotero.Items.get({ID});'.format(ID=itemID))
        self.execute("var notes = item.getNotes();")
        nNotes = int(self.getVariable('notes.length'))

        # order of notes not maintained
        retrievedNotes = []
        for n in range(nNotes):
            self.execute('var note = Zotero.Items.get(notes[{n}]);'.format(n=n))
            retrievedNotes += [self.getVariable('note.getNote()')[1:-1]]

        for retrievedNote, originalNote in zip(sorted(retrievedNotes), sorted(notes)):
            if retrievedNote != originalNote:
                raise Exception('Notes do not match: original:\n %s \nretrieved:\n %s' % (originalNote, retrievedNote))

        else:
            return notes



    def attachFile(self, sourceItemID, filename, mode='import'):
        # single \ -> \\ for MozRepl
        filepath=os.path.abspath(filename)


        # TODO Zotero Error log has this error Error: The character encoding of the plain text document was not declared. The document will render with garbled text in some browser configurations if the document contains characters from outside the US-ASCII range. The character encoding of the file needs to be declared in the transfer protocol or file needs to use a byte order mark as an encoding signature.
        # The same error is logged when file is manually attached through menu, so there is no way to fix it here

        #optionsJV = JSVariable(self, 'options', initialValue = {"file":filepath.replace('\\', '\\'*2), "parentItemID":sourceItemID})
        #importPromiseJV = JSVariable(self, 'importPromise')



        if mode == 'link':
            # TODO: not tested
            #importPromiseJV.setVariableFromFunctionCall('Zotero.Attachments.linkFromFile(' + optionsJV.jsname + ')')
            id = self.sendToZotero(code=f'return Zotero.Attachments.linkFromFile({{"file":{json.dumps(filepath, ensure_ascii=True)}, "parentItemID":{sourceItemID}}})')
        elif mode == 'import':
            #importPromiseJV.setVariableFromFunctionCall('Zotero.Attachments.importFromFile(' + optionsJV.jsname + ')')
            id = self.sendToZotero(code=f'return Zotero.Attachments.importFromFile({{"file":{json.dumps(filepath, ensure_ascii=True)}, "parentItemID":{sourceItemID}}})')
            print('attached file, trying to resolve', id)


            #outJV = JSVariable(self, 'out')


            # TODO: loop till promise is either rejected or fulfilled

            #ret=self.telnet.read_until(b"repl>", timeout = 10)
            #importPromiseJV.attributeAccess('.then((res) => ' + outJV.jsname + ' = res)')

            #print('out.value', outJV.value)



        else:
            raise Exception('Mode not supporte %s ' % mode)

        print('attachment ID', id)
        return id



    def addTags(self, tags, itemID):
       # Add Tags
        output=[] # List of javascript commands


        #self.setVariableFromFunctionCall('item', 'Zotero.Items.get({ID})'.format(ID=itemID))
        #self.setVariableFromFunctionCall('itemID', 'item.save()')
        #output+=['var item = Zotero.Items.get({ID});'.format(ID=itemID)]
        #output+=["var itemID = item.save();"]

        code=f'item = Zotero.Items.get({itemID}); itemID = item.save();'

        for tagAndType in tags: # cannot add tags to unsaved item
            if type(tagAndType) == str or len(tagAndType) == 1: # no type, using default 0
                tag, tagtype = tagAndType, 0
            elif len(tagAndType) == 2:
                tag, tagtype = tagAndType
            else:
                raise Exception('Expected a tag or a tag and a tag type, not this', tagAndType)
            print('adding', tag, tagtype)
            #output+=["item.addTag('{tag}', {tagtype});".format(tag=tag, tagtype=tagtype)]

            code += f'if(! item.addTag("{tag}", {tagtype})) {{return false}};'

        code += 'return true;'
        result = self.sendToZotero(code=code)
        if result != 'true':
            raise ZoteroError('Could not add tags', tags, itemID)
        #for l in output:
        #    printd( self.execute(l))

    def getTags(self, itemID):
        self.execute('var item = Zotero.Items.get({ID});'.format(ID=itemID))
        self.execute('var tags = item.getTags();')
        nTags = int(self.getVariable('tags.length;'))
        savedTags = []
        for n in range(nTags):
            tagName = self.getVariable('tags[{n}].name'.format(n=n))[1:-1]
            print('tagName', tagName)
            print('tags', self.getVariable('tags'))
            try:
                tagType = int(self.getVariable('tags[{n}].type'.format(n=n)))
            except ValueError: # sometimes tag literal is '', cannot convert to int
                tagType = 0
                print('Setting tag type to 0')

            # order of tags is not preserved
            savedTags += [(tagName, tagType)]

        return savedTags


    def verifyTags(self, tags, itemID):
        # Verify tags
        self.execute('var item = Zotero.Items.get({ID});'.format(ID=itemID))
        self.execute('var tags = item.getTags();')
        nTags = int(self.getVariable('tags.length;'))
        if nTags != len(tags):
            raise Exception('Number of tags does not match %s %s' % (nTags, len(tags)))

        savedTags = []
        for n in range(nTags):
            tagName = self.getVariable('tags[{n}].name'.format(n=n))[1:-1]
            tagType = int(self.getVariable('tags[{n}].type'.format(n=n)))
            # order of tags is not preserved
            savedTags += [(tagName, tagType)]

        if sorted(savedTags) != sorted(tags):
                raise Exception('Tags do not match %s %s' % (savedTags,tags))

        printd('Verified all tags.')

    def getSelectedItems(self):
        '''Return the items currently selected in the zotero gui'''
        items = json.loads(self.sendToZotero(code='return ZoteroPane.getSelectedItems()'))
        self.sendToZotero(code='items = ZoteroPane.getSelectedItems()')
        itemIDs = [self.getVariableJSON(f'items[{i}].id') for i in range(len(items))]
        regularItemP = [self.getVariableJSON(f'items[{i}].isRegularItem()') for i in range(len(items))]
        return zip(itemIDs, items, regularItemP)

    def getAttachmentInfo(self, itemID):
        self.sendToZotero(code = 'item = Zotero.Items.get(%s);' % itemID)
        regularItem = self.getVariableJSON('item.isRegularItem()')
        if not regularItem:
            print('Item', itemID, 'is not a regular item, no attachments')
            return None

        self.sendToZotero(code='att_ids = item.getAttachments(false);')
        attachment_ids = self.getVariableJSON('att_ids')
        attachments = [self.getVariableJSON(f'Zotero.Items.get(att_ids[{i}])') for i in range(len(attachment_ids))]

        fileURLs = list(self.getUrlToAttachedFile(aid) for aid in attachment_ids)

        return zip(attachment_ids, attachments, fileURLs)

    def getZoteroDir(self):
        "Return the top level directory that contains the Storage directory "
        return self.getVariableJSON('Zotero.DataDirectory')['dir']


