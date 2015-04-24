#! /usr/bin/python
# -*- coding: utf-8 -*-
#########
#Copyright (C) 2014  Mark Spurgeon <theduck.dev@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#########
import Config
import os
from PyQt4.QtGui import QIcon
import glob
from xdg.DesktopEntry import DesktopEntry
from xdg.IconTheme import IconTheme
import gtk
APPS=None
def info(filter_):
	global APPS
	appList=[]
	a=False
	all_apps=glob.glob(u"/usr/share/applications/*.desktop")
	for a in glob.glob(u"/usr/share/applications/kde4/*.desktop"):
	      all_apps.append(a)
	for a in glob.glob(u"{}/.local/share/applications/*.desktop".format(os.path.expanduser("~"))):
	      all_apps.append(a)
	for f in all_apps:
                de = DesktopEntry(f)
		try:
			if filter_ !="" and filter_.lower() in str(de.getName()).lower():
				show=True
			elif filter_=='':
				show=True
			else:show=False
			showTerminal= de.getTerminal()
			dNotShowIn= de.getNotShowIn()
			dNoDisplay = de.getNoDisplay()
			dHidden = de.getHidden()
			dType = de.getType()
			if dNoDisplay==False and dHidden==False and dType==u"Application" and show==True and os.environ.get("XDG_CURRENT_DESKTOP") not in dNotShowIn:  
				app={}
				OnlyShowIn =  de.getOnlyShowIn()
				current_desk=os.environ.get('XDG_CURRENT_DESKTOP')
				if len(OnlyShowIn)==0 or current_desk in OnlyShowIn:
					app["name"]=de.getName()
					e = de.getExec()

					#prevent '"' in exec
					if e[0] == '"' and e[-1] == '"':
						e = e[:-1][1:]
					try:
						pos= e.index("%")
						e= e[:pos-1]
					except ValueError:
						pass
					if showTerminal==True:
						app["exec"]=u"xterm -e {}".format(e)
					else:
						app["exec"]=e
					app["icon"]=de.getIcon()
					app["icon_path"]=ico_from_name(de.getIcon())
					appList.append(app)
		except:
			pass
	return sorted(appList,key=lambda x:x["name"])
	APPS=sorted(appList,key=lambda x:x["name"])



def ico_from_name(name,size="small"):
	icon_theme = gtk.icon_theme_get_default()
	icon_=icon_theme.lookup_icon(name, 48, 0)
	is_in_theme=False
	if icon_!=None:
		sizes=icon_theme.get_icon_sizes(name)
		if len(sizes)>0:
			highest_res= sorted(icon_theme.get_icon_sizes(name))[::-1][0]
			is_in_theme=True
			icon=icon_theme.lookup_icon(name, highest_res, 0).get_filename()
		else:
			icon=icon_theme.lookup_icon(name, 48, 0).get_filename()
	if is_in_theme==True:
		return str(icon)
	elif os.path.isfile(name):
		return str(name)
	else:
		found=False 
		dir_list=IconTheme.icondirs
		for d in dir_list:
			if os.path.isdir(d):
				for i in os.listdir(d)[::-1]:
					if i.startswith(name):
						path=os.path.join(d,i)
						found=True
						break
		if found==True:
			return str(path)
		else:
			return "/usr/share/duck-launcher/icons/apps.svg"
def ico_from_app(app_name):
	global APPS
	if APPS==None:
		APPS = info('')
	for a in APPS:
		if app_name.lower() in a['name'].lower():
			return a["icon_path"]
def find_info(apps):
	
	APPS=info('')
	a_list=[]
	if apps!=None:
		for a in apps:
			in_apps=False
			a_dict={}
			for app in APPS:
				if a in app['name']:
					in_apps=True
					a_dict = app
			if in_apps==True:
				a_list.append(a_dict)
			elif in_apps==False:
				Config.removeFromDockApps(a)
	return a_list
