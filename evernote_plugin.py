import sublime, sublime_plugin

import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors
import html

#view.run_command('add_to_evernote')
class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")

# setting config

def getAuthToken():
	return 'S=s1:U=8cf25:E=149ed005b46:C=142954f2f49:P=1cd:A=en-devtoken:V=2:H=b8ac1a55f6073b310bc22bc449dd865b'

def getEvernoteHost():
	return "sandbox.evernote.com"

def getSublimeNotebook():
	return "sublime_notebook"

def getUserStoreUri():
	return "https://" + getEvernoteHost() + "/edam/user"

# globals
currentNote = None
#

def getUserStore():
	userStoreUri = THttpClient.THttpClient(getUserStoreUri())
	userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreUri)
	return UserStore.Client(userStoreProtocol)

def getNoteStore():
	noteStoreUrl = getUserStore().getNoteStoreUrl(getAuthToken())
	print(noteStoreUrl)
	noteStoreClient = THttpClient.THttpClient(noteStoreUrl)
	noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreClient)
	return NoteStore.Client(noteStoreProtocol)

def createSublimeNotebook():
	notebook = Types.Notebook()
	notebook.name = getSublimeNotebook()
	notebook = getNoteStore().createNotebook(notebook)
	print(notebook.guid)
	return

def makeNote(noteTitle, noteBody, parentNotebook=None):
	h = html.escape(noteBody)
	noteContent = r'<?xml version="1.0" encoding="UTF-8"?>'
	noteContent += r'<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
	noteContent += r'<en-note>%s</en-note>' %  h
	## Create note object
	newNote = Types.Note()
	newNote.title = noteTitle
	newNote.content = noteContent

	## parentNotebook is optional; if omitted, default notebook is used
	if parentNotebook and hasattr(parentNotebook, 'guid'):
		newNote.notebookGuid = parentNotebook.guid
 	
	## Attempt to create note in Evernote account
	try:
		note = getNoteStore().createNote(getAuthToken(), newNote)
	except Errors.EDAMUserException as err:
		## Something was wrong with the note data
		## See EDAMErrorCode enumeration for error code explanation
		## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
		print("EDAMUserException: code = %d" % (err.errorCode))
		return None
	except Errors.EDAMNotFoundException as err:
		## Parent Notebook GUID doesn't correspond to an actual notebook
		print("EDAMNotFoundException: Invalid parent notebook GUID")
		return None
	## Return created note object
	return note

def makeSublimeNotebook():
	try:
		newNotebook = Types.Notebook()
		newNotebook.name = "sublime"
		createdNotebook = getNoteStore().createNotebook(getAuthToken(), newNotebook)
	except Errors.EDAMUserException as err:
		## Something was wrong with the notebook data
		## See EDAMErrorCode enumeration for error code explanation
		## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
		print("EDAMUserException:", edue)
		return None
	except Errors.EDAMNotFoundException as err:
		## Parent Notebook GUID doesn't correspond to an actual notebook
		print("EDAMNotFoundException: Invalid parent notebook GUID")
		return None
	## Return created notebook object
	return createdNotebook
# commands

# List all of the notebooks in the user's account  
class ListEvernoteNotesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print("ListEvernoteNotesCommand")
		notebooks = getNoteStore().listNotebooks(getAuthToken())
		print("Found ", len(notebooks), " notebooks:")
		for notebook in notebooks:
			print("  * ", notebook.name)
			if notebook.name == "sublime":
				notes = notebook.listNote

class AddToEvernoteCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		def onNewTitle(inputTitle):
			if not inputTitle:
				inputTitle = 'Note from sublime text'
			print("AddToEvernoteCommand")
			body = self.view.substr(sublime.Region(0, self.view.size()))
			title = inputTitle
			sublime.status_message('Creating new evernote...')
			createdNote = makeNote(title, body)
			if createdNote != None:
				view.settings().set('current_guid', createdNote.guid)
				sublime.status_message("Successfully created a new note with GUID: " + createdNote.guid)
			else:
				sublime.status_message('Creating new evernote failed.')
			return

		self.view.window().show_input_panel('New Title:', '', onNewTitle, None, None)

class SaveToEvernoteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print("SaveToEvernoteCommand")
		global currentNote
		updatedNote = getNoteStore().updateNote(getAuthToken(), currentNote)
		return

class DeleteFromEvernoteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print("DeleteFromEvernoteCommand")
		currentGuid = settings.get('current_guid')
		result = getNoteStore().expungeNote(getAuthToken(), currentGuid)
		return