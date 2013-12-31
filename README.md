EvernotePlugin
==============

A [Sublime Text 3](http://www.sublimetext.com/) plugin for creating and editing notes in Evernote.

The aim is to provide the following functions:

Stage 1:

1. create a new note with the current file content in evernote.

2. get a list of evernotes under "sublime" notebook, 
select one to display the text content in sublime text in a new tab.
The notebook "sublime" will be created if it doesn't exist.

3. get a list of evernotes under "sublime" notebook, 
select one to delete it from evernote.

4. update an opened note with its modified content.

Stage 2:

1. save the content to evernote with syntax highlight

==========
Specification
==========

# Installation

## Package Control (Comming soon...)

Install [Package Control](http://wbond.net/sublime_packages/package_control). Evernote will show up in the package list. This is the recommended installation method.


# Usage

All functionality of the plugin is available in the `Tools` / `Evernote` menu and in the command pallette.

## Creating Evernote

Use the `Evernote` / `Add to Evernote` commands. A note under a notebook "Evernote" will be created with contents of current file.

## List Evernote Notes

Use the `Evernote` / `List Evernote Notes` command to see a list of your notes in notebook "Evernote". Selecting one will load the content of the note from that Evernote in new tab. You can then edit the files normally and use `Evernote` / `Save to Evernote` to update the Evernote.

## Delete From Evernote

Use the `Evernote` / `Delete From Evernote` command to see a list of your notes in notebook "Evernote". Selecting one will delete the note.

## Save to Evernote

Use the `Evernote` / `Save to Evernote` command to see a list of your notes in notebook "Evernote". Selecting one will save the content of current file to the selected note.

# Default key bindings:

## Save to Evernote

* Windows and Linux: `Ctrl+K` `Ctrl+S`
* OS X: `Super+K` `Super+S`

## List Evernote Notes

* Windows and Linux: `Ctrl+K` `Ctrl+L`
* OS X: `Super+K` `Super+L`

## Add to Evernote

* Windows and Linux: `Ctrl+K` `Ctrl+A`
* OS X: `Super+K` `Super+A`

## Delete From Evernote

* Windows and Linux: `Ctrl+K` `Ctrl+D`
* OS X: `Super+K` `Super+D`

# Information

Source: https://github.com/lnhote/EvernotePlugin

Authors: [Hunter Lin](https://github.com/lnhote/)
