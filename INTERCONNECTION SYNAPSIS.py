import pandas as pd
import os
import shutil
import datetime
import math
import random
import numpy as np
import pyperclip
import dropbox
import threading

import win32gui
import win32con
import winxpgui
import win32api

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty

global MOD
global Protocol
MOD = pd.read_csv('MAGNUM OPUS DEI.csv')
MOD['Fragments'] = MOD['Fragments'].apply(lambda x: eval(x))
Settings = pd.read_csv('SETTINGS.csv', header=None).set_index(0)[1]
LOG = pd.read_csv('LOG.csv')
Protocol = ['CENTRAL REGNUM', 'LUX DOMINIUM', 'NOBILIS MUNDI', 'MYSTERIUM FIDEI', 'OUTER SAPIENTIA', 'OUTER MYSTERIUM', 'AMORPHOUS SAPIENTIA', 'AMORPHOUS MYSTERIUM']

def MsgBox(self, InputText, Duration=5):
	global LOG, MessageCounter
	MessageCounter = Duration
	self.ids.MessageBox.text = InputText
	if InputText != '': LOG = LOG.append(pd.DataFrame(data=[[datetime.datetime.now(), InputText]], columns=['Date', 'Log']), ignore_index=True)
	print(InputText)
def Copy(self, Copy, Message):
	pyperclip.copy(Copy)
	MsgBox(self, Message)
	print(pyperclip.paste())
def Sort(self):
	global MOD
	MOD = MOD.join(MOD['World'].apply(lambda x: x.lower()).to_frame('i')).sort_values('i', ascending=True).drop(['i'], axis=1).reset_index(drop=True)

Builder.load_string('''
#: import NoTransition kivy.uix.screenmanager.NoTransition
<Label>:
	font_name: 'computer_7'
	font_size: 16
	color: (0,1,1,1)
	text_size: self.size
	valign: 'center'
	halign: 'center'
<Button>:
	background_color: (0.2,0.2,0.2,1)
<TextInput>:
	font_name: 'computer_7'
	font_size: 16
	disabled_foreground_color: (0,1,1,1)
	foreground_color: (0,1,0,1)
	background_color: (0.1,0.1,0.1,1)
	multiline: False

<List_Dest_Anime>:
	viewclass: 'SBL_Dest_Anime'
	do_scroll_y: True
	bar_width: 15
	scroll_type: ['bars', 'content']
	SelectableRecycleGridLayout:
		spacing: 2
		default_size: None, 25
		default_size_hint: 1, None
		size_hint_y: None
		height: self.minimum_height
		orientation: 'vertical'
		multiselect: False
		touch_multiselect: True
		cols: 1
<SBL_Dest_Anime>:
	orientation: 'horizontal'
	canvas.before:
		Color:
			rgba: (.2, .2, .2, 1) if self.selected else (.1, .1, .1, 1)
		Rectangle:
			size: self.size
			pos: self.pos
	item_Index: ''
	item_World: ''
	item_Protocol: ''
	item_Status: ''
	item_Fragmented: ''
	item_color_World: (1,1,1,1)
	item_color_Extension: (0,1,1,1)
	item_color_Status: (0,.5,1,1)
	Label:
		text: root.item_Index
		size_hint_x: .1
		color: (1,1,1,1)
	Label:
		text: root.item_World
		halign: 'left'
		color: root.item_color_World
	Label:
		text: root.item_Protocol
		size_hint_x: .36
		halign: 'left'
		color: root.item_color_Extension
	Label:
		text: root.item_Status
		size_hint_x: .2
		halign: 'left'
		color: root.item_color_Status
	Label:
		text: root.item_Fragmented
		size_hint_x: .1
		halign: 'left'
		color: root.item_color_Status
<List_Dest_Episode>:
	viewclass: 'SBL_Dest_Episode'
	do_scroll_y: True
	bar_width: 15
	scroll_type: ['bars', 'content']
	SelectableRecycleGridLayout:
		spacing: 2
		default_size: None, 25
		default_size_hint: 1, None
		size_hint_y: None
		height: self.minimum_height
		orientation: 'vertical'
		multiselect: False
		touch_multiselect: True
		cols: 1
<SBL_Dest_Episode>:
	orientation: 'horizontal'
	canvas.before:
		Color:
			rgba: (.2, .2, .2, 1) if self.selected else (.1, .1, .1, 1)
		Rectangle:
			size: self.size
			pos: self.pos
	item_Fragment: ''
	item_Extension_Display: ''
	item_color: (0,1,1,1)
	Label:
		text: root.item_Fragment
		halign: 'left'
		color: root.item_color
	Label:
		size_hint_x: 0.1
		text: root.item_Extension_Display
		halign: 'center'
		color: root.item_color

<Nexus_Initial>:
	BoxLayout:
		orientation: 'vertical'
		padding: 10

		BoxLayout:
			id: CurrentDate
			orientation: 'horizontal'
			size_hint_y: 0.05
			Label:
				id: TimeClock_Date
				halign: 'left'
				valign: 'top'
				font_size: 24
			Label:
				id: TimeClock_DaysElapsed
				halign: 'left'
				valign: 'top'
				font_size: 24

		GridLayout:
			id: MainLayout
			spacing: 5
			rows: 2
			cols: 2

			BoxLayout:
				size_hint_x: 0.5
				size_hint_y: 0.7
				VideoPlayer:
					id: ConquerorLens
					options: {'allow_stretch': True}

			FloatLayout:
				size_hint_y: 0.7
				Label:
					id: Label_Selected_Anime_Name
					size_hint_x: 1
					size_hint_y: .1
					pos_hint: {'x': 0, 'y': .9}
					font_size: 22
				Label:
					id: Label_Selected_Anime_Protocol
					halign: 'left'
					size_hint_x: 1
					size_hint_y: .1
					pos_hint: {'x': 0, 'y': 0}
				Label:
					id: Label_Selected_Anime_Status
					size_hint_x: .2
					size_hint_y: .1
					pos_hint: {'x': .4, 'y': .8}
				Label:
					id: Label_Selected_Anime_Fragmented
					size_hint_x: .2
					size_hint_y: .1
					pos_hint: {'x': .4, 'y': .4}
				Label:
					id: Label_Selected_Anime_COrder
					halign: 'left'
					size_hint_x: 1
					size_hint_y: .1
					pos_hint: {'x': 0, 'y': .1}
				Button:
					text: '+'
					size_hint_x: .05
					size_hint_y: .1
					pos_hint: {'x': .475, 'y': .525}
					on_release: root.Plus(True)
				Button:
					text: '-'
					size_hint_x: .05
					size_hint_y: .1
					pos_hint: {'x': .475, 'y': .275}
					on_release: root.Plus(False)
			ScreenManager:
				id: Management_Menu
				size_hint_x: 0.5
				Screen:
					name: 'Screen_Menu_Main'
					GridLayout:
						rows: 5
						cols: 2
						spacing: 30
						padding: 30
						Button:
							text: 'Start Interconnection'
							on_release: root.ids.Management_Misc.current = 'Screen_Misc_Anime'
						Button:
							text: 'Mission Progress'
							on_release: root.ids.Management_Misc.current = 'Screen_Misc_Stats'
						Button:
							id: Button_Menu_Assemble
							text: 'Assemble'
							disabled: True
							on_release: [root.ids.Management_Misc.current, root.ids.Management_Menu.current] = ['Screen_Misc_Anime', 'Screen_Menu_Assemble_Anime']
						Button:
							id: Button_Menu_SelectionMenu
							text: 'Selection Menu'
							disabled: True
							on_release: [root.Select_Mode_Anime('Fragmentation'), root.Select_Anime(root.ids.Label_Selected_Anime_Name.text)]
						Button:
							text: 'Options'
							on_release: [root.ids.Management_Misc.current, root.ids.Management_Menu.current] = ['Screen_Misc_Options', 'Screen_Menu_Options']
						Button:
							id: Button_Menu_Save
							text: 'Overwrite Memoria'
							on_release: root.Save(True)
						Button:
							text: 'Back to Reality'
							on_release: app.stop()
						Label:
						Label:
				Screen:
					name: 'Screen_Menu_Selection'
					GridLayout:
						rows: 5
						cols: 2
						spacing: 30
						padding: 30
						Button:
							id: Button_Menu_Copy
							text: 'Recognize World'
							disabled: True
							on_release: root.Copy_Anime()
						Button:
							id: Button_Menu_Source
							text: 'Open Source'
							disabled: True
							on_release: root.OpenSource()
						Button:
							id: Button_Menu_Materialize
							text: 'Materialize Fragment'
							disabled: True
							on_release: root.Copy_Episode()
						Button:
							id: Button_Menu_Defragment
							text: 'Defragment'
							disabled: True
							on_release: root.Defragment()
						Button:
							id: Button_Menu_Desynapse
							text: 'Desynapse'
							disabled: True
							on_release: root.Desynapse()
						Button:
							id: Button_Menu_Resynapse
							text: 'Resynapse'
							disabled: True
							on_release: root.Resynapse()
						Button:
							id: Button_Menu_Conquer
							text: 'Resonate'
							disabled: True
							on_release: root.ConquerNew()
						Button:
							id: Button_Menu_AlterLens
							text: 'Alternate Lens'
							disabled: True
							on_release: root.Select_Episode_Alter()
						Button:
							text: 'Main Menu'
							on_release: root.ids.Management_Menu.current = 'Screen_Menu_Main'
				Screen:
					name: 'Screen_Menu_Options'
					GridLayout:
						rows: 5
						cols: 2
						spacing: 30
						padding: 30
						Button:
							text: 'Alternate Protocol'
							on_release: root.ids.Management_Misc_Options.current = 'Screen_Options_AlterProtocol'
						Button:
							text: 'Mission Function'
							on_release: root.ids.Management_Misc_Options.current = 'Screen_Options_MissionFunction'
						Button:
							text: 'Create Remnant'
							on_release: root.ids.Management_Misc_Options.current = 'Screen_Options_Backup'
							on_release: root.Backup_Reset()
						Button:
							text: 'Synchronize'
							on_release: root.ids.Management_Misc_Options.current = 'Screen_Options_Synchronize'
						Button:
							text: 'Memoria Settings'
							on_release: root.ids.Management_Misc_Options.current = 'Screen_Options_Save'
							on_release: root.Upload_Reset()
						Button:
							text: 'Lens Settings'
							on_release: root.ids.Management_Misc_Options.current = 'Screen_Options_Screen'
						Button:
							text: 'Main Menu'
							on_release: root.ids.Management_Menu.current = 'Screen_Menu_Main'
						Label:
						Label:
						Label:
				Screen:
					name: 'Screen_Menu_Assemble_Anime'
					GridLayout:
						rows: 5
						cols: 2
						spacing: 30
						padding: 30
						Button:
							id: Button_Menu_Install_Anime
							text: 'Install'
							on_release: [root.ids.Management_Menu.current, root.ids.Management_Misc_Mode.current] = ['Screen_Menu_Install_Anime', 'Screen_Mode_Install']
						Button:
							id: Button_Menu_Uninstall_Anime
							text: 'Uninstall'
							on_release: root.Remove_Anime([root.ids.List_Dest_Anime.data[i]['item_World'] for i in root.ids.List_Dest_Anime._layout_manager.selected_nodes])
						Button:
							id: Button_Menu_Combine
							text: 'Combine'
							on_release: root.Combine_Select()
						Button:
							id: Button_Menu_Execute
							text: 'Execute'
							disabled: True
						Button:
							text: 'Main Menu'
							on_release: root.ids.Management_Menu.current = 'Screen_Menu_Main'
						Label:
						Label:
						Label:
						Label:
				Screen:
					name: 'Screen_Menu_Assemble_Episode'
					GridLayout:
						rows: 5
						cols: 2
						spacing: 30
						padding: 30
						Button:
							id: Button_Menu_Install_Episode
							text: 'Install'
							on_release: root.ids.Management_Misc_List_Episode.current = 'Screen_List_Episode_Install'
							on_release: root.ids.Button_Menu_Install_Episode.disabled = root.ids.Button_Menu_Uninstall_Episode.disabled = root.ids.Button_Menu_Transfer.disabled = True
						Button:
							id: Button_Menu_Uninstall_Episode
							text: 'Uninstall'
							on_release: root.Remove_Episode([root.ids.List_Dest_Episode.data[i]['item_Fragment'] for i in root.ids.List_Dest_Episode._layout_manager.selected_nodes])
						Button:
							id: Button_Menu_Transfer
							text: 'Transfer'
							on_release: root.Transfer_Select()
						Label:
						Label:
						Label:
						Label:
						Label:
						Label:
				Screen:
					name: 'Screen_Menu_Install_Anime'
					BoxLayout:
						orientation: 'vertical'
						spacing: 50
						padding: 80
						Button:
							id: Button_InstallOnS
							text: 'Install on AMORPHOUS SAPIENTIA'
							on_release: root.Install_Anime(self.text[11:])
							disabled: root.ids.Text_Install_Anime_Name.text == ''
						Button:
							id: Button_InstallOnM
							text: 'Install on AMORPHOUS MYSTERIUM'
							on_release: root.Install_Anime(self.text[11:])
							disabled: root.ids.Text_Install_Anime_Name.text == ''
						Button:
							text: 'Cancel Installation'
							on_release: [root.ids.Management_Menu.current, root.ids.Management_Misc_Mode.current] = ['Screen_Menu_Assemble_Anime', 'Screen_Mode_Destination'] 

			ScreenManager:
				id: Management_Misc

				Screen:
					name: 'Screen_Misc_Anime'
					BoxLayout:
						orientation: 'vertical'
						spacing: 1
						BoxLayout:
							orientation: 'horizontal'
							size_hint_y: .1
							Button:
								id: Button_Mode_Fragmentation
								text: 'Fragmentation'
								on_release:	root.Select_Mode_Anime(self.text)
							Button:
								id: Button_Mode_Librorum
								text: 'Omnis Librorum'
								on_release: root.Select_Mode_Anime(self.text)
							Button:
								id: Button_Mode_Reminiscence
								text: 'Reminiscence'
								on_release: root.Select_Mode_Anime(self.text)
							Button:
								id: Button_Mode_IncertusTerrae
								text: 'Incertus Terrae'
								on_release: root.Select_Mode_Anime(self.text)
							Button:
								id: Button_Mode_Randomize
								text: 'Randomize'
								on_release: root.Select_Anime_Randomize()
							Button:
								id: Button_Mode_Assemble
								text: 'Assemble'
								on_release: root.Select_Mode_Anime(self.text)
						ScreenManager:
							id: Management_Misc_Mode
							transition: NoTransition()
							Screen:
								name: 'Screen_Mode_Fragmentation'
								FloatLayout:
									TextInput:
										id: Text_Frag_Anime_1
										size_hint_x: 0.75
										size_hint_y: 0.1
										pos_hint: {"x": 0, "y": 0.7}
										disabled: True
										on_focus: root.ConquerNew_legalize(0)
										on_text: root.ConquerNew_Check(0)
									TextInput:
										id: Text_Frag_Episode_1
										size_hint_x: 0.2
										size_hint_y: 0.1
										pos_hint: {"x": 0.75, "y": 0.7}
										disabled: True
									Button:
										text: ">"
										size_hint_x: 0.05
										size_hint_y: 0.1
										pos_hint: {"x": 0.95, "y": 0.7}
										on_release: root.Select_Anime(root.ids.Text_Frag_Anime_1.text)
									TextInput:
										id: Text_Frag_Anime_2
										size_hint_x: 0.75
										size_hint_y: 0.1
										pos_hint: {"x": 0, "y": 0.45}
										disabled: True
										on_focus: root.ConquerNew_legalize(1)
										on_text: root.ConquerNew_Check(1)
									TextInput:
										id: Text_Frag_Episode_2
										size_hint_x: 0.2
										size_hint_y: 0.1
										pos_hint: {"x": 0.75, "y": 0.45}
										disabled: True
									Button:
										text: ">"
										size_hint_x: 0.05
										size_hint_y: 0.1
										pos_hint: {"x": 0.95, "y": 0.45}
										on_release: root.Select_Anime(root.ids.Text_Frag_Anime_2.text)
									TextInput:
										id: Text_Frag_Anime_3
										size_hint_x: 0.75
										size_hint_y: 0.1
										pos_hint: {"x": 0, "y": 0.2}
										disabled: True
										on_focus: root.ConquerNew_legalize(2)
										on_text: root.ConquerNew_Check(2)
									TextInput:
										id: Text_Frag_Episode_3
										size_hint_x: 0.2
										size_hint_y: 0.1
										pos_hint: {"x": 0.75, "y": 0.2}
										disabled: True
									Button:
										text: ">"
										size_hint_x: 0.05
										size_hint_y: 0.1
										pos_hint: {"x": 0.95, "y": 0.2}
										on_release: root.Select_Anime(root.ids.Text_Frag_Anime_3.text)
							Screen:
								name: 'Screen_Mode_Destination'
								BoxLayout:
									orientation: 'vertical'
									BoxLayout:
										orientation: 'horizontal'
										size_hint_y: .1
										Button:
											text: '#'
											size_hint_x: .1
										Button:
											text: 'World'
										Button:
											text: 'Protocol'
											size_hint_x: .36
										Button:
											text: 'Status'
											size_hint_x: .3
									List_Dest_Anime:
										id: List_Dest_Anime
							Screen:
								name: 'Screen_Mode_Install'
								FloatLayout:
									TextInput:
										id: Text_Install_Anime_Name
										size_hint_x: .59
										size_hint_y: .1
										pos_hint: {'x':.1 , 'y': .45}
										on_text: self.text = self.text.replace('/', '-').replace(":", '-').replace('*', '-').replace("?", '-').replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-').replace('\\\\', '-')
										on_text: root.Install_Anime_Check()
									TextInput:
										id: Text_Install_Anime_Episodes
										size_hint_x: .2
										size_hint_y: .1
										pos_hint: {'x': .7, 'y': .45}
										on_text: [root.ids.Button_InstallOnS.text, root.ids.Button_InstallOnM.text] = ['Install on ' + ('AMORPHOUS ' if self.text in ['', '0'] else 'OUTER ') + i for i in ['SAPIENTIA', 'MYSTERIUM']]
				
				Screen:
					name: 'Screen_Misc_Episode'
					BoxLayout:
						orientation: 'vertical'
						spacing: 2
						BoxLayout:
							orientation: 'horizontal'
							size_hint_y: .1
							Button:
								text: '<<<'
								on_release: [root.ids.Management_Menu.current, root.ids.Management_Misc.current] = ['Screen_Menu_Assemble_Anime' if root.ids.Management_Menu.current == 'Screen_Menu_Assemble_Episode' else root.ids.Management_Menu.current, 'Screen_Misc_Anime']
							Button:
								id: Button_Mode_Destination
								text: 'Destination'
								on_release: root.Select_Mode_Episode(self.text)
							Button:
								id: Button_Mode_NovusMundus
								text: 'Mundus Novus'
								on_release: root.Select_Mode_Episode(self.text)
							Button:
								id: Button_Mode_IncertusFragments
								text: 'Incertus Fragments'
								on_release: root.Select_Mode_Episode(self.text)
						ScreenManager:
							id: Management_Misc_List_Episode
							transition: NoTransition()
							Screen:
								name: 'Screen_List_Episode_Loaded'
								List_Dest_Episode:
									id: List_Dest_Episode
							Screen:
								name: 'Screen_List_Episode_Empty'
								FloatLayout:
									TextInput:
										id: Text_List_Episode_Populate
										size_hint_x: .2
										size_hint_y: .1
										pos_hint: {'x':.3, 'y': .45}
									Button:
										text: 'Populate'
										size_hint_x: .2
										size_hint_y: .1
										pos_hint: {'x':.5, 'y': .45}
										on_release: root.Populate(root.ids.Text_List_Episode_Populate.text)
							Screen:
								name: 'Screen_List_Episode_Install'
								FloatLayout:
									TextInput:
										id: Text_Install_Episode_Name
										size_hint_x: .8
										size_hint_y: .1
										pos_hint: {'x':.1, 'y': .6}
										on_text: self.text = self.text.replace('/', '-').replace(":", '-').replace('*', '-').replace("?", '-').replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-').replace('\\\\', '-')
										on_text: root.Install_Episode_Check()
									Button:
										text: 'Install Fragment'
										size_hint_x: .3
										size_hint_y: .1
										pos_hint: {'x':.6, 'y': .3}
										on_release: root.Install_Episode()
										on_release: root.ids.Button_Menu_Install_Episode.disabled = root.ids.Button_Menu_Uninstall_Episode.disabled = root.ids.Button_Menu_Transfer.disabled = False
										disabled: root.ids.Text_Install_Episode_Name.text == ''
									Button:
										text: 'Cancel Installation'
										size_hint_x: .3
										size_hint_y: .1
										pos_hint: {'x':.1, 'y': .3}
										on_release: root.Select_Mode_Episode('Assemble')
										on_release: root.ids.Button_Menu_Install_Episode.disabled = root.ids.Button_Menu_Uninstall_Episode.disabled = root.ids.Button_Menu_Transfer.disabled = False

				Screen:
					name: 'Screen_Misc_Stats'
					ScreenManager:
						id: Management_Misc_Stats
						Screen:
							name: 'Screen_Stats_Conquer'
							FloatLayout:
								Label:
									halign: 'left'
									text: 'Current Stats:'
									color: (1,1,1,1)
									size_hint_x: 1
									size_hint_y: 0.1
									pos_hint: {'x':0, 'y':0.9}
								GridLayout:
									rows: 4
									cols: 2
									size_hint_x: 0.95
									size_hint_y: 0.7
									pos_hint: {'x':0.05, 'y':0.2}
									Label:
										halign: 'left'
										text: 'Worlds'
									Label:
										id: Label_Stats_Conquer_Worlds
										halign: 'left'
										size_hint_x: 0.5
									Label:
										halign: 'left'
										text: 'Fragments'
									Label:
										id: Label_Stats_Conquer_Fragments
										halign: 'left'
										size_hint_x: 0.5
									Label:
										halign: 'left'
										text: 'Progress'
									Label:
										id: Label_Stats_Conquer_Progress
										halign: 'left'
										size_hint_x: 0.5
									Label:
										halign: 'left'
										text: 'Speed'
									Label:
										id: Label_Stats_Conquer_Speed
										halign: 'left'
										size_hint_x: 0.5
								Button:
									text: 'Mission Objective'
									on_release: root.ids.Management_Misc_Stats.current = 'Screen_Stats_Mission'
									size_hint_x: 1
									size_hint_y: 0.15
									pos_hint: {'x':0, 'y':0}

						Screen:
							name: 'Screen_Stats_Mission'
							FloatLayout:
								rows: 3
								Label:
									halign: 'left'
									text: 'Mission Objectives:'
									color: (1,1,1,1)
									size_hint_x: 1
									size_hint_y: 0.1
									pos_hint: {'x':0, 'y':0.9}
								GridLayout:
									rows: 4
									cols: 2
									size_hint_x: 0.95
									size_hint_y: 0.7
									pos_hint: {'x':0.05, 'y':0.2}
									Label:
										halign: 'left'
										text: 'Easy'
										color: (0,1,0,1)
									Label:
										id: Label_Stats_Mission_Easy
										halign: 'left'
										size_hint_x: 0.5
										color: (0,1,0,1)
									Label:
										halign: 'left'
										text: 'Normal'
										color: (1,0.5,0,1)
									Label:
										id: Label_Stats_Mission_Normal
										halign: 'left'
										size_hint_x: 0.5
										color: (1,0.5,0,1)
									Label:
										halign: 'left'
										text: 'Hard'
										color: (1,0,0,1)
									Label:
										id: Label_Stats_Mission_Hard
										halign: 'left'
										size_hint_x: 0.5
										color: (1,0,0,1)
									Label:
										halign: 'left'
										text: 'Insane'
										color: (0.5,0,1,1)
									Label:
										id: Label_Stats_Mission_Insane
										halign: 'left'
										size_hint_x: 0.5
										color: (0.5,0,1,1)
								Button:
									text: 'Current Stats'
									on_release: root.ids.Management_Misc_Stats.current = 'Screen_Stats_Conquer'
									size_hint_x: 1
									size_hint_y: 0.15
									pos_hint: {'x':0, 'y':0}

				Screen:
					name: 'Screen_Misc_Options'
					ScreenManager:
						id: Management_Misc_Options
						Screen:
							name: 'Screen_Options_AlterProtocol'
							BoxLayout:
								orientation: 'vertical'
								GridLayout:
									rows: 5
									cols: 2
									padding: 30
									spacing: 35
									Label:
										text: 'CENTRAL REGNUM'
										halign: 'left'
										size_hint_x: .2
									TextInput:
										id: Text_Protocol_1
										on_text: root.AlterProtocol_Check(0, True)
									Label:
										text: 'LUX DOMINIUM'
										halign: 'left'
										size_hint_x: .2
									TextInput:
										id: Text_Protocol_2
										on_text: root.AlterProtocol_Check(1, True)
									Label:
										text: 'NOBILIS MUNDI'
										halign: 'left'
										size_hint_x: .2
									TextInput:
										id: Text_Protocol_3
										on_text: root.AlterProtocol_Check(2, True)
									Label:
										text: 'MYSTERIUM FIDEI'
										halign: 'left'
										size_hint_x: .2
									TextInput:
										id: Text_Protocol_4
										on_text: root.AlterProtocol_Check(3, True)
									Label:
										text: 'INCERTUS TERRAE'
										halign: 'left'
										size_hint_x: .2
									TextInput:
										id: Text_Protocol_5
										on_text: root.AlterProtocol_Check(4, True)
								BoxLayout:
									orientation: 'horizontal'
									size_hint_y: .1
									Button:
										text: 'Reset'
										on_release: root.AlterProtocol_Reset()
									Button:
										id: Button_AlterProtocol_Confirm
										text: 'Confirm'
										on_release: root.AlterProtocol_Confirm()
						Screen:
							name: 'Screen_Options_MissionFunction'
							BoxLayout:
								orientation: 'vertical'
								GridLayout:
									rows: 4
									cols: 2
									padding: 40
									spacing: 50
									Label:
										text: 'Easy'
										halign: 'left'
										size_hint_x: .2
									TextInput:
										id: Text_Function_1
										on_text: root.ids.Button_MissionFunction_Confirm.color = (1,1,0,1)
									Label:
										text: 'Normal'
										halign: 'left'
										size_hint_x: .2
									TextInput:
										id: Text_Function_2
										on_text: root.ids.Button_MissionFunction_Confirm.color = (1,1,0,1)
									Label:
										text: 'Hard'
										halign: 'left'
										size_hint_x: .2
									TextInput:
										id: Text_Function_3
										on_text: root.ids.Button_MissionFunction_Confirm.color = (1,1,0,1)
									Label:
										text: 'Insane'
										halign: 'left'
										size_hint_x: .2
									TextInput:
										id: Text_Function_4
										on_text: root.ids.Button_MissionFunction_Confirm.color = (1,1,0,1)
								BoxLayout:
									orientation: 'horizontal'
									size_hint_y: .1
									Button:
										text: 'Reset'
										on_release: root.MissionFunction_Reset()
									Button:
										id: Button_MissionFunction_Confirm
										text: 'Confirm'
										on_release: root.MissionFunction_Confirm()
						Screen:
							name: 'Screen_Options_Backup'
							FloatLayout:
								BoxLayout:
									size_hint_x: .8
									size_hint_y: .08
									pos_hint: {'x':.1, 'y':.7}
									TextInput:
										id: Text_Backup_Protocol
										on_text: root.Backup_Check()
									Button:
										size_hint_x: .1
										text: 'Set'
										on_release: root.Backup_Set()
								TextInput:
									id: Text_Backup_Msg
									size_hint_x: .8
									size_hint_y: .08
									pos_hint: {'x':.1, 'y':.5}
								BoxLayout:
									size_hint_x: .7
									size_hint_y: .08
									pos_hint: {'x': 0, 'y': .3}
									Label:
										text: 'On existing:'
										halign: 'left'
									Button:
										text:'<'
										size_hint_x: 0.1
										on_release: root.ids.Label_Backup_OnExisting.text = 'Duplicate' if root.ids.Label_Backup_OnExisting.text == 'Overwrite' else 'Cancel' if root.ids.Label_Backup_OnExisting.text == 'Duplicate' else 'Overwrite'
									Label:
										id: Label_Backup_OnExisting
										text: 'Duplicate'
									Button:
										text:'>'
										size_hint_x: 0.1
										on_release: root.ids.Label_Backup_OnExisting.text = 'Cancel' if root.ids.Label_Backup_OnExisting.text == 'Overwrite' else 'Duplicate' if root.ids.Label_Backup_OnExisting.text == 'Cancel' else 'Overwrite'
								Button:
									size_hint_x: .2
									size_hint_y: .08
									pos_hint: {'x':.4, 'y':.1}
									text: 'Create Remnant'
									on_release: root.Backup()
						Screen:
							name: 'Screen_Options_Synchronize'
							FloatLayout:
								BoxLayout:
									size_hint_x: .7
									size_hint_y: .08
									pos_hint: {'x': 0, 'y': .7}
									Label:
										text: 'On undetected Protocol:'
										halign: 'left'
									Button:
										text:'<'
										size_hint_x: 0.1
										on_release: root.ids.Label_Synch_OnUndetected.text = 'Keep' if root.ids.Label_Synch_OnUndetected.text == 'Remove' else 'Remove'
									Label:
										id: Label_Synch_OnUndetected
										text: 'Keep'
									Button:
										text:'>'
										size_hint_x: 0.1
										on_release: root.ids.Label_Synch_OnUndetected.text = 'Keep' if root.ids.Label_Synch_OnUndetected.text == 'Remove' else 'Remove'
								BoxLayout:
									size_hint_x: .7
									size_hint_y: .08
									pos_hint: {'x': 0, 'y': .4}
									Label:
										text: 'On duplicated World:'
										halign: 'left'
									Button:
										text:'<'
										size_hint_x: 0.1
										on_release: root.ids.Label_Synch_OnDuplicated.text = 'Ignore' if root.ids.Label_Synch_OnDuplicated.text == 'Spare One' else 'Remove All' if root.ids.Label_Synch_OnDuplicated.text == 'Ignore' else 'Spare One'
									Label:
										id: Label_Synch_OnDuplicated
										text: 'Ignore'
									Button:
										text:'>'
										size_hint_x: 0.1
										on_release: root.ids.Label_Synch_OnDuplicated.text = 'Remove All' if root.ids.Label_Synch_OnDuplicated.text == 'Spare One' else 'Ignore' if root.ids.Label_Synch_OnDuplicated.text == 'Remove All' else 'Spare One'
								Button:
									size_hint_x: .2
									size_hint_y: .08
									pos_hint: {'x':.4, 'y':.1}
									text: 'Synchronize'
									on_release: root.Synchronize()
						Screen:
							name: 'Screen_Options_Save'
							FloatLayout:
								BoxLayout:
									size_hint_x: 1
									size_hint_y: .1
									pos_hint: {'x':0, 'y':.7}
									CheckBox:
										id: Check_Upload
										size_hint_x: .1
										active: True
										on_active: root.ids.Text_AccessToken.disabled = root.ids.Button_SetAccessToken.disabled = not self.active
									Label: 
										text: 'Duplicate to Mare Aeternam'
										halign: 'left'
								BoxLayout:
									size_hint_x: .8
									size_hint_y: .08
									pos_hint: {'x':.1, 'y':.3}
									TextInput:
										id: Text_AccessToken
										disabled_foreground_color: (1,1,1,1)
									Button:
										id: Button_SetAccessToken
										text: 'Set'
										size_hint_x: .1
										on_release: root.Upload_Set()
						Screen:
							name: 'Screen_Options_Screen'
							FloatLayout:
								Label:
									size_hint_x:.2
									size_hint_y:.1
									pos_hint: {'x':0, 'y':.75}
									text: 'Lens Power'
									halign: 'left'
								Slider:
									size_hint_x:.8
									size_hint_y:.1
									pos_hint: {'x':.1, 'y':.6}
									min: 100
									max: 255
									value: 255
									on_touch_move: root.SetOpacity(self.value)
									on_touch_up: root.SetOpacity(self.value)
								BoxLayout:
									size_hint_x: 1
									size_hint_y: .1
									pos_hint: {'x':0, 'y':.15}
									CheckBox:
										id: Check_FullScreen
										size_hint_x: .1
										on_active: root.FullScreen(self.active)
									Label:
										text: 'Lens Takeover'
										halign: 'left'

		Label:
			id: MessageBox
			size_hint_y: 0.04
''')

#Main Screen
class Nexus_Initial(Screen):
	def __init__(self, **kwargs):
		super(Nexus_Initial, self).__init__(**kwargs)
		for i in range(3): self.Fill_List_Frag(i)
		global Day_Initial, Year_Initial, MessageCounter
		Day_Initial = datetime.datetime.strptime(Settings['Day_Initial'], '%Y-%m-%d %H:%M:%S')
		Year_Initial = int(Settings['Year_Initial'])
		MessageCounter = 0
		self.Time_Refresh()
		def Timer(dt): self.Time_Refresh()
		Clock.schedule_interval(Timer, .1)
		self.Select_Mode_Anime('Fragmentation')
		self.Select_Anime(None)
		self.Update_Stats(True,True,True)
		self.Update_Mission()
		self.AlterProtocol_Reset()
		self.MissionFunction_Reset()
		self.Upload_Reset()
		self.Backup_Reset()

	def Time_Refresh(self):
		global Day_Running, Year_Running, Day_Initial, Year_Initial, MessageCounter
		Day_Running = datetime.datetime(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)
		Year_Running = int(datetime.datetime.now().strftime('%Y'))
		if Day_Initial != Day_Running: self.Time_EndDay()
		if Year_Initial != Year_Running: Nexus_Initial.Time_EndYear()
		Day_Initial = Day_Running
		Year_Initial = Year_Running
		self.ids.TimeClock_Date.text = datetime.datetime.now().strftime('%m/%d/%Y  %X')
		self.ids.TimeClock_DaysElapsed.text = 'Day: ' + str((datetime.datetime.now() - datetime.datetime(Year_Running,1,1,0,0,0,0)).days+1) + '/' + str((datetime.datetime(Year_Running+1,1,1,0,0,0,0) - datetime.datetime(Year_Running,1,1,0,0,0,0)).days)
		[self.AlterProtocol_Check(i, False) for i in range(5)]
		self.Update_Stats(Enable_Speed=True)
		if MessageCounter <= 0: self.ids.MessageBox.text = ''
		else:  MessageCounter -= .1

	def Time_EndDay(self):
		Settings['Day_Episodes'] = MOD['Fragmented'].values.sum()
		self.Update_Stats(Enable_Fragments=True)
		self.Update_Mission()

	def Time_EndYear(self):
		Settings['Year_Episodes'] = MOD['Fragmented'].values.sum()

	def Fill_List_Frag(self,i):
		x = MOD['World'][MOD['Status'] == 'Resonated'][MOD['Order'] == i]
		y = MOD['Fragmented'][MOD['Status'] == 'Resonated'][MOD['Order'] == i]
		if len(x) == 1:
			exec('self.ids.Text_Frag_Anime_' + str(i+1) + '.text = "' + x.reset_index(drop=True)[0] + '"')
			exec('self.ids.Text_Frag_Episode_' + str(i+1) + '.text = "' + str(y.reset_index(drop=True)[0]) + '"')

	def Fill_List_Dest_Anime(self, Data):
		self.ids.List_Dest_Anime._layout_manager.clear_selection()
		self.ids.List_Dest_Anime.refresh_from_data()
		List_Dest_Anime.data = [{'item_Index': str(x+1),
								 'item_World': str(Data['World'][x]),
								 'item_Protocol': str(Data['Protocol'][x]),
								 'item_Status': str(Data['Status'][x]),
								 'item_Fragmented': str(Data['Fragmented'][x]) + '/' + str(len(Data['Fragments'][x]) if Data['Protocol'][x] in Protocol[:6] else str('???')),
								 'item_color_World': (1,1,1,1) if Selected_Mode_Anime != 'Assemble' else (1,.5,1,1),
								 'item_color_Extension': (0,1,1,1) if Data['Protocol'][x] in Protocol[:4] else (1,1,0,1) if Data['Protocol'][x] in Protocol[4:6] else (1,.5,0,1),
								 'item_color_Status': (1,1,1,1) if Data['Status'][x] == 'Conquered' else (0,1,0,1) if Data['Status'][x] == 'Resonated' else (.5,.5,.5,1)} for x in range(len(Data))]

	def Select_Mode_Anime(self, Mode):
		global Selected_Mode_Anime
		Selected_Mode_Anime = Mode
		if Mode == 'Omnis Librorum':
			self.ids.Button_Mode_Librorum.disabled = True
			self.ids.Button_Mode_Assemble.disabled = self.ids.Button_Mode_Reminiscence.disabled = self.ids.Button_Mode_IncertusTerrae.disabled = self.ids.Button_Mode_Fragmentation.disabled = False
			self.ids.List_Dest_Anime._layout_manager.multiselect = False
			self.ids.Button_Menu_Assemble.disabled = True
			self.Fill_List_Dest_Anime(MOD)
			if self.ids.Management_Menu.current in ['Screen_Menu_Assemble_Anime', 'Screen_Menu_Install_Anime']: self.ids.Management_Menu.current = 'Screen_Menu_Main'
			self.ids.Management_Misc_Mode.current = 'Screen_Mode_Destination'
		elif Mode == 'Reminiscence':
			self.ids.Button_Mode_Reminiscence.disabled = True
			self.ids.Button_Mode_Assemble.disabled = self.ids.Button_Mode_Librorum.disabled = self.ids.Button_Mode_IncertusTerrae.disabled = self.ids.Button_Mode_Fragmentation.disabled = False
			self.ids.List_Dest_Anime._layout_manager.multiselect = False
			self.ids.Button_Menu_Assemble.disabled = True
			self.Fill_List_Dest_Anime(MOD[MOD['Status'] == 'Conquered'].set_index('Order'))
			if self.ids.Management_Menu.current in ['Screen_Menu_Assemble_Anime', 'Screen_Menu_Install_Anime']: self.ids.Management_Menu.current = 'Screen_Menu_Main'
			self.ids.Management_Misc_Mode.current = 'Screen_Mode_Destination'
		elif Mode == 'Incertus Terrae':
			self.ids.Button_Mode_IncertusTerrae.disabled = True
			self.ids.Button_Mode_Assemble.disabled = self.ids.Button_Mode_Librorum.disabled = self.ids.Button_Mode_Reminiscence.disabled = self.ids.Button_Mode_Fragmentation.disabled = False
			self.ids.List_Dest_Anime._layout_manager.multiselect = False
			self.ids.Button_Menu_Assemble.disabled = True
			self.Fill_List_Dest_Anime(MOD.query('World in ' + str(next(os.walk(Settings['Protocol: INCERTUS TERRAE']))[1])).reset_index(drop=True))
			if self.ids.Management_Menu.current in ['Screen_Menu_Assemble_Anime', 'Screen_Menu_Install_Anime']: self.ids.Management_Menu.current = 'Screen_Menu_Main'
			self.ids.Management_Misc_Mode.current = 'Screen_Mode_Destination'
		elif Mode == 'Fragmentation':
			self.ids.Button_Mode_Fragmentation.disabled = True
			self.ids.Button_Mode_Assemble.disabled = self.ids.Button_Mode_Librorum.disabled = self.ids.Button_Mode_Reminiscence.disabled = self.ids.Button_Mode_IncertusTerrae.disabled = False
			self.ids.List_Dest_Anime._layout_manager.multiselect = True
			self.ids.Button_Menu_Assemble.disabled = True
			if self.ids.Management_Menu.current in ['Screen_Menu_Assemble_Anime', 'Screen_Menu_Install_Anime']: self.ids.Management_Menu.current = 'Screen_Menu_Main'
			self.ids.Management_Misc_Mode.current = 'Screen_Mode_Fragmentation'
		elif Mode == 'Assemble':
			self.ids.Button_Mode_Assemble.disabled = True
			self.ids.Button_Mode_Fragmentation.disabled = self.ids.Button_Mode_Librorum.disabled = self.ids.Button_Mode_Reminiscence.disabled = self.ids.Button_Mode_IncertusTerrae.disabled = False
			self.ids.List_Dest_Anime._layout_manager.multiselect = True
			self.ids.Button_Menu_Assemble.disabled = False
			self.Fill_List_Dest_Anime(MOD.query('Protocol in ' + str(Protocol[4:])).reset_index(drop=True))
			self.ids.Management_Menu.current = 'Screen_Menu_Assemble_Anime'
			self.ids.Management_Misc_Mode.current = 'Screen_Mode_Destination'
			self.ids.Button_Menu_Execute.disabled = True
			self.ids.Button_Menu_Combine.disabled = self.ids.Button_Menu_Install_Anime.disabled = self.ids.Button_Menu_Uninstall_Anime.disabled = False

	def Select_Mode_Episode(self, Mode):
		global Selected_Mode_Episode
		Selected_Mode_Episode = Mode
		self.ids.List_Dest_Episode._layout_manager.clear_selection()
		self.ids.List_Dest_Episode.refresh_from_data()
		if Mode == 'Destination':
			self.ids.List_Dest_Episode._layout_manager.multiselect = False
			self.ids.Button_Mode_Destination.disabled = True
			self.ids.Button_Mode_NovusMundus.disabled = self.ids.Button_Mode_NovusMundus.disabled = True if Selected_Anime_Name not in next(os.walk(Settings['Protocol: INCERTUS TERRAE']))[1] else False
			self.ids.Button_Mode_IncertusFragments.disabled = False
			if Selected_Anime_Protocol in Protocol[:4]:
				List_Dest_Episode.data = [{'item_Fragment': str(x)[:-4], 'item_Extension_Real': str(x)[-3:], 'item_Extension_Display': str(x)[-3:].lower(), 'item_color': (0,1,1,1)} for x in MOD['Fragments'][MOD['World'] == Selected_Anime_Name].reset_index(drop=True)[0]]
				self.ids.Management_Misc_List_Episode.current = 'Screen_List_Episode_Loaded'
			elif Selected_Anime_Protocol in Protocol[4:6]:
				List_Dest_Episode.data = [{'item_Fragment': str(x)[:-4], 'item_Extension_Real': '', 'item_Extension_Display': '???', 'item_color': (0,1,1,1)} for x in MOD['Fragments'][MOD['World'] == Selected_Anime_Name].reset_index(drop=True)[0]]
				self.ids.Management_Misc_List_Episode.current = 'Screen_List_Episode_Loaded'
			else:
				List_Dest_Episode.data = [{'item_Fragment': Selected_Anime_Name + ' Episode ' + str(x+1), 'item_Extension_Real': '', 'item_Extension_Display': '???', 'item_color': (1,.5,0,1)} for x in range(100)]
				self.ids.Management_Misc_List_Episode.current = 'Screen_List_Episode_Loaded'
		elif Mode == 'Mundus Novus':
			self.ids.List_Dest_Episode._layout_manager.multiselect = False
			self.ids.Button_Mode_NovusMundus.disabled = True
			self.ids.Button_Mode_Destination.disabled = self.ids.Button_Mode_IncertusFragments.disabled = False
			List_Dest_Episode.data = [{'item_Fragment': str(x)[:-4], 'item_Extension_Real': str(x)[-3:], 'item_Extension_Display': str(x)[-3:].lower(), 'item_color': (0,1,1,1)} for x in next(os.walk(Settings['Protocol: INCERTUS TERRAE'] + '\\' + Selected_Anime_Name))[2]]
			self.ids.Management_Misc_List_Episode.current = 'Screen_List_Episode_Loaded'
		elif Mode == 'Incertus Fragments':
			self.ids.List_Dest_Episode._layout_manager.multiselect = False
			self.ids.Button_Mode_IncertusFragments.disabled = True
			self.ids.Button_Mode_Destination.disabled = False
			self.ids.Button_Mode_NovusMundus.disabled = True if Selected_Anime_Name not in next(os.walk(Settings['Protocol: INCERTUS TERRAE']))[1] else False
			List_Dest_Episode.data = [{'item_Fragment': str(x)[:-4], 'item_Extension_Real': str(x)[-3:], 'item_Extension_Display': str(x)[-3:].lower(), 'item_color': (0,1,1,1)} for x in next(os.walk(Settings['Recently_Downloaded']))[2]]
			self.ids.Management_Misc_List_Episode.current = 'Screen_List_Episode_Loaded'
		elif Mode == 'Assemble':
			self.ids.List_Dest_Episode._layout_manager.multiselect = True
			self.ids.Button_Mode_Destination.disabled = self.ids.Button_Mode_NovusMundus.disabled = self.ids.Button_Mode_IncertusFragments.disabled = True
			if Selected_Anime_Protocol_Edit in Protocol[4:6]:
				List_Dest_Episode.data = [{'item_Fragment': str(x)[:-4], 'item_Extension_Real': '', 'item_Extension_Display': '', 'item_color': (1,.5,1,1)} for x in MOD['Fragments'][MOD['World'] == Selected_Anime_Name_Edit].reset_index(drop=True)[0]]
				self.ids.Management_Misc_List_Episode.current = 'Screen_List_Episode_Loaded'
			else:
				List_Dest_Episode.data = []
				self.ids.Management_Misc_List_Episode.current = 'Screen_List_Episode_Empty'

	def Select_Anime(self, Selection):
		global Selected_Anime_Name, Selected_Anime_Protocol, Selected_Anime_Status, Selected_Anime_Fragmented, Selected_Anime_Fragments
		if Selection == None: #If nothing selected
			Selected_Anime_Name = Selected_Anime_Protocol = Selected_Anime_Status = Selected_Anime_Fragmented = Selected_Anime_Fragments = None
			self.ids.Label_Selected_Anime_Name.text = self.ids.Label_Selected_Anime_Protocol.text = self.ids.Label_Selected_Anime_Status.text = self.ids.Label_Selected_Anime_Fragmented.text = self.ids.Label_Selected_Anime_COrder.text = ''
			self.DisableButtons('Nothing')
		elif Selection == '': #If empty selection
			Selected_Anime_Name = Selected_Anime_Protocol = Selected_Anime_Status = Selected_Anime_Fragmented = Selected_Anime_Fragments = None
			self.ids.Label_Selected_Anime_Name.text = self.ids.Label_Selected_Anime_Protocol.text = self.ids.Label_Selected_Anime_Status.text = self.ids.Label_Selected_Anime_Fragmented.text = self.ids.Label_Selected_Anime_COrder.text = ''
			self.ids.Management_Menu.current = 'Screen_Menu_Selection'
			self.DisableButtons('Empty')
		else:
			Selected_Anime_Name = self.ids.Label_Selected_Anime_Name.text = Selection
			Selected_Anime_Protocol = MOD['Protocol'][MOD['World'] == Selected_Anime_Name].reset_index(drop=True)[0]
			self.ids.Label_Selected_Anime_Protocol.text = 'Protocol: ' + Selected_Anime_Protocol
			Selected_Anime_Status = self.ids.Label_Selected_Anime_Status.text = MOD['Status'][MOD['World'] == Selected_Anime_Name].reset_index(drop=True)[0]
			Selected_Anime_Fragmented = MOD['Fragmented'][MOD['World'] == Selected_Anime_Name].reset_index(drop=True)[0]
			Selected_Anime_Fragments = len(MOD['Fragments'][MOD['World'] == Selected_Anime_Name].reset_index(drop=True)[0])
			self.ids.Label_Selected_Anime_Fragmented.text = str(Selected_Anime_Fragmented) + '/' + (str(Selected_Anime_Fragments) if Selected_Anime_Fragments != 0 else '???')
			self.ids.Label_Selected_Anime_COrder.text = 'Completion no. ' + str(int(MOD['Order'][MOD['World'] == Selected_Anime_Name].reset_index(drop=True)[0] + 1)) if Selected_Anime_Status == 'Conquered' else ''
			self.Select_Mode_Episode('Destination')
			self.ids.Button_Mode_NovusMundus.disabled = True if Selected_Anime_Name not in next(os.walk(Settings['Protocol: INCERTUS TERRAE']))[1] else False
			self.ids.Management_Misc.current = 'Screen_Misc_Episode'
			self.ids.Management_Menu.current = 'Screen_Menu_Selection'
			self.ids.Button_Menu_SelectionMenu.disabled = False
			self.DisableButtons(Selected_Anime_Status)

	def Select_Anime_Assemble(self, Selection, Path):
		global Selected_Anime_Name_Edit, Selected_Anime_Protocol_Edit 
		Selected_Anime_Name_Edit = Selection
		Selected_Anime_Protocol_Edit = Path
		self.Select_Mode_Episode('Assemble')
		self.ids.Management_Menu.current = 'Screen_Menu_Assemble_Episode'
		self.ids.Management_Misc.current = 'Screen_Misc_Episode'
		self.ids.Button_Menu_Install_Episode.disabled = self.ids.Button_Menu_Uninstall_Episode.disabled = self.ids.Button_Menu_Transfer.disabled = False

	def Select_Anime_Randomize(self):
		self.Select_Mode_Anime('Fragmentation')
		i = random.randint(0, len(MOD) - 1)
		self.Select_Anime(MOD['World'][i])

	def Select_Episode(self, Selection, Extension):
		global Selected_Episode_Name, Selected_Episode_Extension
		Selected_Episode_Name = Selection
		Selected_Episode_Extension = Extension
		if Selected_Mode_Episode == 'Destination': Path = (Settings['Protocol: ' + Selected_Anime_Protocol] if Selected_Anime_Protocol in Protocol[:4] else '') + '\\' + Selected_Anime_Name + '\\' + Selection + '.' + Extension
		elif Selected_Mode_Episode == 'Mundus Novus': Path = Settings['Protocol: INCERTUS TERRAE'] + '\\' + Selected_Anime_Name + '\\' + Selection + '.' + Extension
		elif Selected_Mode_Episode == 'Incertus Fragments': Path = Settings['Recently_Downloaded'] + '\\' + Selection + '.' + Extension
		if os.path.isfile(Path):
			self.ids.ConquerorLens.source = Path
			MsgBox(self, 'Aligning to: ' + Selected_Episode_Name + '. Fragmentation ready.')
		else:
			self.ids.ConquerorLens.source = ''
			if Selected_Anime_Protocol[:9] != 'AMORPHOUS': MsgBox(self, 'Destination not found. Fragmentation of ' + Selected_Episode_Name + ' aborted.')

	def Select_Episode_Alter(self):
		Path = self.ids.ConquerorLens.source
		self.ids.ConquerorLens.state = 'pause'
		if os.path.isfile(Path):
			os.startfile(Path)

	def Update_Stats(self, Enable_Worlds=False, Enable_Fragments=False, Enable_Progress=False, Enable_Speed=False):
		if Enable_Worlds: self.ids.Label_Stats_Conquer_Worlds.text = str(len(MOD[MOD['Status'] == 'Conquered']))
		if Enable_Fragments: self.ids.Label_Stats_Conquer_Fragments.text = str(MOD['Fragmented'].values.sum()) + ' (' + ('+' if MOD['Fragmented'].values.sum() >= int(Settings['Day_Episodes']) else '') + str(MOD['Fragmented'].values.sum() - int(Settings['Day_Episodes'])) + ')'
		if Enable_Progress: self.ids.Label_Stats_Conquer_Progress.text = str("{:.3%}".format(MOD.query('Protocol not in' + str(Protocol[6:]))['Fragmented'].values.sum() / MOD['Fragments'].apply(lambda x: len(x)).values.sum()))
		if Enable_Speed: self.ids.Label_Stats_Conquer_Speed.text = str("{:.9}".format(MOD['Fragmented'].values.sum() / ((datetime.datetime.now() - datetime.datetime(2012, 8, 30)).days + (datetime.datetime.now() - datetime.datetime(2012, 8, 30)).seconds / 86400 + (datetime.datetime.now() - datetime.datetime(2012, 8, 30)).microseconds / (86400*1000000)))) #Avg speed since he recommended me Sword Art Online, 30 Aug 2012.

	def Update_Mission(self):
		self.ids.Label_Stats_Mission_Easy.text = str(int(Settings['Year_Episodes']) + math.ceil(eval(Settings['Objective_Easy'].replace("X", str((datetime.datetime.now() - datetime.datetime(Year_Running,1,1,0,0,0,0)).days+1)))))
		self.ids.Label_Stats_Mission_Normal.text = str(int(Settings['Year_Episodes']) + math.ceil(eval(Settings["Objective_Normal"].replace("X", str((datetime.datetime.now() - datetime.datetime(Year_Running,1,1,0,0,0,0)).days+1)))))
		self.ids.Label_Stats_Mission_Hard.text = str(int(Settings['Year_Episodes']) + math.ceil(eval(Settings["Objective_Hard"].replace("X", str((datetime.datetime.now() - datetime.datetime(Year_Running,1,1,0,0,0,0)).days+1)))))
		self.ids.Label_Stats_Mission_Insane.text = str(int(Settings['Year_Episodes']) + math.ceil(eval(Settings["Objective_Insane"].replace("X", str((datetime.datetime.now() - datetime.datetime(Year_Running,1,1,0,0,0,0)).days+1)))))

	def Update_Anime(self, Selection):
		self.ids.List_Dest_Anime._layout_manager.clear_selection()
		self.ids.List_Dest_Anime.refresh_from_data()
		x = [i['item_World'] for i in self.ids.List_Dest_Anime.data]
		if Selection in x: #Assign to RV
			List_Dest_Anime.data[x.index(Selection)]['item_Protocol'] = MOD['Protocol'][MOD['World'] == Selection].reset_index(drop=True)[0]
			List_Dest_Anime.data[x.index(Selection)]['item_Fragmented'] = str(MOD['Fragmented'][MOD['World'] == Selection].reset_index(drop=True)[0]) + '/' + str(len(MOD['Fragments'][MOD['World'] == Selection].reset_index(drop=True)[0]) if MOD['Protocol'][MOD['World'] == Selection].reset_index(drop=True)[0] in Protocol[:6] else '???')
			List_Dest_Anime.data[x.index(Selection)]['item_color_Extension'] = (1,1,0,1) if MOD['Protocol'][MOD['World'] == Selection].reset_index(drop=True)[0] in Protocol[:6] else (1,.5,0,1)

	def DisableButtons(self, Mode):
		def Disable(self, Enables, Disables):
			for i in Enables: exec('self.ids.' + i + '.disabled = False')
			for i in Disables: exec('self.ids.' + i + '.disabled = True')
		if Mode == 'Conquered': Disable(self, ['Button_Menu_Copy', 'Button_Menu_Source', 'Button_Menu_Materialize', 'Button_Menu_AlterLens'], ['Button_Menu_Conquer', 'Button_Menu_Desynapse', 'Button_Menu_Resynapse', 'Button_Menu_Defragment'])
		elif Mode == 'Resonated': Disable(self, ['Button_Menu_Copy', 'Button_Menu_Source', 'Button_Menu_Materialize', 'Button_Menu_AlterLens', 'Button_Menu_Desynapse', 'Button_Menu_Defragment'], ['Button_Menu_Resynapse', 'Button_Menu_Conquer'])
		elif Mode == 'Unfragmented': Disable(self, ['Button_Menu_Copy', 'Button_Menu_Source', 'Button_Menu_Materialize', 'Button_Menu_AlterLens', 'Button_Menu_Conquer'], ['Button_Menu_Resynapse', 'Button_Menu_Desynapse', 'Button_Menu_Defragment'])
		elif Mode == 'Empty': Disable(self, ['Button_Menu_Conquer', 'Button_Menu_Resynapse'], ['Button_Menu_AlterLens', 'Button_Menu_Materialize', 'Button_Menu_Source', 'Button_Menu_Copy', 'Button_Menu_Desynapse', 'Button_Menu_Defragment'])
		elif Mode == 'Nothing':  Disable(self, [], ['Button_Menu_Conquer', 'Button_Menu_Resynapse', 'Button_Menu_AlterLens', 'Button_Menu_Materialize', 'Button_Menu_Source', 'Button_Menu_Copy', 'Button_Menu_Desynapse', 'Button_Menu_Defragment', 'Button_Menu_SelectionMenu'])

	def Plus(self, Plus):
		try: Selected_Anime_Name
		except NameError: return
		if Selected_Anime_Status in ['Conquered', 'Resonated']:
			global Selected_Anime_Fragmented
			Selected_Anime_Fragmented = MOD['Fragmented'][MOD['World'] == Selected_Anime_Name] = Selected_Anime_Fragmented + (1 if Plus else -1 if Selected_Anime_Fragmented != 0 else 0) #Update variable and assign to MOD
			self.ids.Label_Selected_Anime_Fragmented.text = str(Selected_Anime_Fragmented) + '/' + (str(Selected_Anime_Fragments) if Selected_Anime_Fragments != 0 else '???') #Assign to Selection Label
			if Selected_Anime_Status == 'Resonated': exec('self.ids.Text_Frag_Episode_' + str(int(MOD['Order'][MOD['World'] == Selected_Anime_Name]+1)) + '.text = str(Selected_Anime_Fragmented)') #Assign to Fragmentation TextInput
			self.ids.List_Dest_Anime._layout_manager.clear_selection()
			self.ids.List_Dest_Anime.refresh_from_data()
			x = [i['item_World'] for i in self.ids.List_Dest_Anime.data]
			if Selected_Anime_Name in x: List_Dest_Anime.data[x.index(Selected_Anime_Name)]['item_Fragmented'] = self.ids.Label_Selected_Anime_Fragmented.text #Assign to RV
			self.Update_Stats(False,True,True,True)
			self.Save(False)

	def Copy_Anime(self):
		if self.ids.MessageBox.text[:13] == 'Copied World:': Copy(self, Settings['Protocol: ' + Selected_Anime_Protocol] + '\\' + Selected_Anime_Name, 'Copied World Protocol (Origin): ' + Selected_Anime_Name) if Selected_Anime_Protocol in Protocol[:4] else Copy(self, Settings['Protocol: INCERTUS TERRAE'] + '\\' + Selected_Anime_Name, 'Copied World Protocol (Alternative): ' + Selected_Anime_Name) #Copy World Path (Origin)
		elif self.ids.MessageBox.text[:31] == 'Copied World Protocol (Origin):': Copy(self, Settings['Protocol: INCERTUS TERRAE'] + '\\' + Selected_Anime_Name, 'Copied World Protocol (Alternative): ' + Selected_Anime_Name)  #Copy World Path (Alternative)
		else: Copy(self, Selected_Anime_Name, 'Copied World: ' + Selected_Anime_Name) #Copy World name

	def Copy_Episode(self):
		try: Selected_Episode_Name
		except NameError: return MsgBox(self, 'No Fragment selected.')
		if self.ids.MessageBox.text[22:25] == 'mp4': Copy(self, Settings['Protocol: INCERTUS TERRAE'] + '\\' + Selected_Anime_Name + '\\' + Selected_Episode_Name + '.flv', 'Materialize Fragment (flv): ' + Selected_Episode_Name)
		elif self.ids.MessageBox.text[22:25] == 'flv': Copy(self, Settings['Protocol: INCERTUS TERRAE'] + '\\' + Selected_Anime_Name + '\\' + Selected_Episode_Name + '.mkv', 'Materialize Fragment (mkv): ' + Selected_Episode_Name)
		elif self.ids.MessageBox.text[22:25] == 'mkv': Copy(self, Settings['Protocol: ' + Selected_Anime_Protocol] + '\\' + Selected_Anime_Name + '\\' + Selected_Episode_Name + '.' + Selected_Episode_Extension, 'Materialize Fragment (Path): ' + Selected_Episode_Name) if Selected_Anime_Protocol in Protocol[:4] else Copy(self, Settings['Protocol: INCERTUS TERRAE'] + '\\' + Selected_Anime_Name + '\\' + Selected_Episode_Name + '.mp4', 'Materialize Fragment (mp4): ' + Selected_Episode_Name)
		else: Copy(self, Settings['Protocol: INCERTUS TERRAE'] + '\\' + Selected_Anime_Name + '\\' + Selected_Episode_Name + '.mp4', 'Materialize Fragment (mp4): ' + Selected_Episode_Name)

	def OpenSource(self):
		if Selected_Mode_Episode == 'Destination':
			if Selected_Anime_Protocol not in Protocol[:4]: MsgBox(self, 'Protocol does not have real Destination. Access aborted.')
			elif not os.path.isdir(Settings['Protocol: ' + Selected_Anime_Protocol] + '\\' + Selected_Anime_Name): MsgBox(self, 'Destination does not exist. Access aborted.')
			else: os.startfile(Settings['Protocol: ' + Selected_Anime_Protocol] + '\\' + Selected_Anime_Name)
		elif Selected_Mode_Episode == 'Mundus Novus':
			Path = Settings['Protocol: INCERTUS TERRAE'] + '\\' + Selected_Anime_Name
			if not os.path.isdir(Path): MsgBox(self, 'Destination does not exist. Access aborted.')
			else: os.startfile(Path)
		elif Selected_Mode_Episode == 'Incertus Fragments':
			Path = Settings['Recently_Downloaded']
			if not os.path.isdir(Path): MsgBox(self, 'Destination does not exist. Access aborted.')
			else: os.startfile(Path)

	def Defragment(self):
		global Selected_Anime_Status, Selected_Anime_Fragmented
		exec('self.ids.Text_Frag_Anime_' + str(int(MOD['Order'][MOD['World'] == Selected_Anime_Name]) + 1) + '.text = self.ids.Text_Frag_Episode_' + str(int(MOD['Order'][MOD['World'] == Selected_Anime_Name]) + 1) + '.text = ""') #Empty Fragmentation TextInput
		x = MOD['Order'][MOD['World'] == Selected_Anime_Name] = np.nan #Assign Completion Order to MOD
		self.ids.Label_Selected_Anime_COrder.text = ''
		Selected_Anime_Status = MOD['Status'][MOD['World'] == Selected_Anime_Name] = self.ids.Label_Selected_Anime_Status.text = 'Unfragmented' #Update variable and assign to MOD and Selection Label
		Selected_Anime_Fragmented = MOD['Fragmented'][MOD['World'] == Selected_Anime_Name] = 0 #Defragment Episodes
		self.ids.Label_Selected_Anime_Fragmented.text = str(Selected_Anime_Fragmented) + '/' + str(Selected_Anime_Fragments) #Assign Defragment to TextInput
		self.ids.List_Dest_Anime._layout_manager.clear_selection()
		self.ids.List_Dest_Anime.refresh_from_data()
		x = [i['item_World'] for i in self.ids.List_Dest_Anime.data]
		if Selected_Anime_Name in x: #Assign to RV
			List_Dest_Anime.data[x.index(Selected_Anime_Name)]['item_Status'] = Selected_Anime_Status
			List_Dest_Anime.data[x.index(Selected_Anime_Name)]['item_Fragmented'] = self.ids.Label_Selected_Anime_Fragmented.text
			List_Dest_Anime.data[x.index(Selected_Anime_Name)]['item_color_Status'] = (.5,.5,.5,1)
		self.DisableButtons(Selected_Anime_Status)
		self.Update_Stats(True,True,True,True)
		self.Save(False)
		MsgBox(self, Selected_Anime_Name + ' defragmented.')

	def Desynapse(self):
		global Selected_Anime_Status
		exec('self.ids.Text_Frag_Anime_' + str(int(MOD['Order'][MOD['World'] == Selected_Anime_Name]) + 1) + '.text = self.ids.Text_Frag_Episode_' + str(int(MOD['Order'][MOD['World'] == Selected_Anime_Name]) + 1) + '.text = ""') #Empty Fragmentation TextInput
		x = MOD['Order'][MOD['World'] == Selected_Anime_Name] = MOD['Order'][MOD['Status'] == 'Conquered'].max() + 1 #Assign Completion Order to MOD
		self.ids.Label_Selected_Anime_COrder.text = 'Completion no. ' + str(int(x) + 1)
		Selected_Anime_Status = MOD['Status'][MOD['World'] == Selected_Anime_Name] = self.ids.Label_Selected_Anime_Status.text = 'Conquered' #Update variable and assign to MOD and Selection Label
		self.ids.List_Dest_Anime._layout_manager.clear_selection()
		self.ids.List_Dest_Anime.refresh_from_data()
		x = [i['item_World'] for i in self.ids.List_Dest_Anime.data]
		if Selected_Anime_Name in x: #Assign to RV
			List_Dest_Anime.data[x.index(Selected_Anime_Name)]['item_Status'] = Selected_Anime_Status
			List_Dest_Anime.data[x.index(Selected_Anime_Name)]['item_color_Status'] = (1,1,1,1)
		self.DisableButtons(Selected_Anime_Status)
		self.Update_Stats(Enable_Worlds=True)
		self.Save(False)
		MsgBox(self, Selected_Anime_Name + ' desynapsed.')

	def Resynapse(self):
		if len(MOD[MOD['Status'] == 'Conquered']) == 0: MsgBox(self, 'Reminiscence is empty. Nothing to resynapse.')
		else:
			Selection = MOD['World'][MOD['Status'] == 'Conquered'][MOD['Order'] == MOD['Order'].max()].reset_index(drop=True)[0]
			MOD['Status'][MOD['World'] == Selection] = 'Resonated'
			i = MOD['Order'][MOD['World'] == Selection] = 0 if self.ids.Text_Frag_Anime_1.text == '' else 1 if self.ids.Text_Frag_Anime_2.text == '' else 2 #Assign Order to MOD
			self.Fill_List_Frag(i)
			self.Select_Mode_Anime('Fragmentation')
			self.Select_Anime(Selection)
			self.Update_Stats(True,False,False,False)
			self.Save(False)
			MsgBox(self, Selection + ' resynapsed.')

	def ConquerNew(self):
		global Selected_Anime_Status
		if Selected_Anime_Status == 'Unfragmented':
			if self.ids.Text_Frag_Anime_1.text != '' and self.ids.Text_Frag_Anime_2.text != '' and self.ids.Text_Frag_Anime_3.text != '': MsgBox(self, 'Fragmentation limit reached.')
			else:
				Selected_Anime_Status = MOD['Status'][MOD['World'] == Selected_Anime_Name] = 'Resonated' #Update variable and assign to MOD and Selection Label
				self.ids.List_Dest_Anime._layout_manager.clear_selection()
				self.ids.List_Dest_Anime.refresh_from_data()
				x = [i['item_World'] for i in self.ids.List_Dest_Anime.data]
				if Selected_Anime_Name in x: #Assign to RV
					List_Dest_Anime.data[x.index(Selected_Anime_Name)]['item_Status'] = Selected_Anime_Status
					List_Dest_Anime.data[x.index(Selected_Anime_Name)]['item_color_Status'] = (0,1,0,1)
				i = MOD['Order'][MOD['World'] == Selected_Anime_Name] = 0 if self.ids.Text_Frag_Anime_1.text == '' else 1 if self.ids.Text_Frag_Anime_2.text == '' else 2 #Assign Order to MOD
				self.Fill_List_Frag(i)
				self.Select_Anime(Selected_Anime_Name)
				self.Update_Stats(True,False,False,False)
				self.Save(False)
				MsgBox(self, Selected_Anime_Name + ' resonated. Fragmentation is available.')
		elif Selected_Anime_Status == None:
			for i in range(3):
				if eval('self.ids.Text_Frag_Anime_' + str(i+1) + '.text == ""'): #Enable Fragmentation TextInput
					exec('self.ids.Text_Frag_Anime_' + str(i+1) + '.disabled = False')
					exec('self.ids.Text_Frag_Anime_' + str(i+1) + '.focus = True')
					break
			self.Select_Mode_Anime('Fragmentation')

	def ConquerNew_Check(self, n):
		if eval('self.ids.Text_Frag_Anime_' + str(n+1) + '.disabled') == False: #If Selected Input unfocused
			Text = eval('self.ids.Text_Frag_Anime_' + str(n+1) + '.text')
			if len(MOD.query('Status in' + str(['Resonated', 'Conquered']))[MOD['World'] == Text]) == 1: exec('self.ids.Text_Frag_Anime_' + str(n+1) + '.foreground_color = (1,.5,0,1)') #If in Progress or already Conquered
			elif len(MOD[MOD['World'] == Text][MOD['Status'] == 'Unfragmented']) == 1: exec('self.ids.Text_Frag_Anime_' + str(n+1) + '.foreground_color = (1,1,0,1)') #If Unfragmented
			else: exec('self.ids.Text_Frag_Anime_' + str(n+1) + '.foreground_color = (0,1,0,1)') #If not exist in MOD

	def ConquerNew_legalize(self, n):
		if not eval('self.ids.Text_Frag_Anime_' + str(n+1) + '.focus'): #If Selected Input unfocused
			Text = eval('self.ids.Text_Frag_Anime_' + str(n+1) + '.text')
			if Text == '': MsgBox(self, 'Cancelled. Please fill the new World you want to resonate.') #If left empty
			else:
				if len(MOD[MOD['World'] == Text][MOD['Status'] == 'Resonated']) == 1: #If in Progress
					MsgBox(self, 'Current World is already in Fragmentation list.')
					exec('self.ids.Text_Frag_Anime_' + str(n+1) + '.text = ""')
				elif len(MOD[MOD['World'] == Text][MOD['Status'] == 'Conquered']) == 1: #If already Conquered
					MsgBox(self, 'Cannot refragment a conquered World.')
					exec('self.ids.Text_Frag_Anime_' + str(n+1) + '.text = ""')
				elif len(MOD[MOD['World'] == Text][MOD['Status'] == 'Unfragmented']) == 1: #If Unfragmented
					MOD['Status'][MOD['World'] == Text] = 'Resonated' #Assign Status to MOD
					MOD['Order'][MOD['World'] == Text] = n
					exec('self.ids.Text_Frag_Episode_' + str(n+1) + '.text = str(0)') #Fill Episode TextInput
					self.Select_Anime(Text)
					self.Save(False)
					MsgBox(self, Text + ' added to Fragmentation list.')
				else: #If not exist in MOD
					MsgBox(self, 'Current World has not been installed into MAGNUM OPUS DEI.')
					exec('self.ids.Text_Frag_Anime_' + str(n+1) + '.text = ""')
			exec('self.ids.Text_Frag_Anime_' + str(n+1) + '.disabled = True')

	def Populate(self, n):
		try: n = int(n)
		except ValueError: n = 0
		if n == 0: MsgBox(self, 'Please fill the legit number of Fragments to populate.')
		else:
			MOD['Fragments'][MOD[MOD['World'] == Selected_Anime_Name_Edit].index[0]] = [Selected_Anime_Name_Edit + ' Episode ' + str(i+1) + '.mp4' for i in range(n)] #Fill Episodes
			MOD['Protocol'][MOD[MOD['World'] == Selected_Anime_Name_Edit].index[0]] = MOD['Protocol'][MOD[MOD['World'] == Selected_Anime_Name_Edit].index[0]].replace('AMORPHOUS', 'OUTER') #Change Protocol
			self.Update_Anime(Selected_Anime_Name_Edit)
			self.Update_Stats(False,False,True,True)
			self.Select_Anime_Assemble(Selected_Anime_Name_Edit, MOD['Protocol'][MOD['World'] == Selected_Anime_Name_Edit].reset_index(drop=True)[0])
			self.Save(False)
			MsgBox(self, Selected_Anime_Name_Edit + ' populated with ' + str(n) + (' Fragments.' if n != 1 else ' Fragment.'))
			self.ids.Text_Install_Episode_Name.text = ''

	def Install_Anime(self, Protocol):
		global MOD
		Name = self.ids.Text_Install_Anime_Name.text
		Episodes = 0 if self.ids.Text_Install_Anime_Episodes.text == '' else int(self.ids.Text_Install_Anime_Episodes.text)
		if len(MOD[MOD['World'] == Name]) != 0: MsgBox(self, Name + ' already exist. Installation failed.')
		else: 
			MOD = MOD.append(pd.DataFrame(data = [[Name, Protocol, [Name + ' Episode ' + str(i+1) + '.mp4' for i in range(Episodes)] if Episodes != 1 else [Name + '.mp4'], 'Unfragmented', 0, np.nan]], columns = MOD.columns), ignore_index=True)
			Sort(self)
			self.ids.Text_Install_Anime_Name.text = self.ids.Text_Install_Anime_Episodes.text = ''
			self.Select_Mode_Anime('Assemble')
			self.Save(False)
			MsgBox(self, Name + ' installed on ' + Protocol + '.')

	def Install_Anime_Check(self):
		self.ids.Text_Install_Anime_Name.foreground_color = self.ids.Text_Install_Anime_Episodes.foreground_color = (0,1,0,1) if len(MOD[MOD['World'] == self.ids.Text_Install_Anime_Name.text]) == 0 else (1,.5,0,1)

	def Install_Episode(self):
		Name = self.ids.Text_Install_Episode_Name.text + '.mp4'
		if Name in MOD['Fragments'][MOD['World'] == Selected_Anime_Name_Edit].reset_index(drop=True)[0]: MsgBox(self, self.ids.Text_Install_Episode_Name.text + ' already exist. Installation failed.')
		else:
			MOD['Fragments'][MOD[MOD['World'] == Selected_Anime_Name_Edit].index[0]] += [Name] #Assign To Episode List
			MOD['Protocol'][MOD[MOD['World'] == Selected_Anime_Name_Edit].index[0]] = MOD['Protocol'][MOD[MOD['World'] == Selected_Anime_Name_Edit].index[0]].replace('AMORPHOUS', 'OUTER') #Change Protocol
			self.Update_Anime(Selected_Anime_Name_Edit)
			self.Update_Stats(False,False,True,True)
			self.Select_Anime_Assemble(Selected_Anime_Name_Edit, MOD['Protocol'][MOD['World'] == Selected_Anime_Name_Edit].reset_index(drop=True)[0])
			self.Save(False)
			MsgBox(self, self.ids.Text_Install_Episode_Name.text + ' installed on World: ' + Selected_Anime_Name_Edit)
			self.ids.Text_Install_Episode_Name.text = ''

	def Install_Episode_Check(self):
		self.ids.Text_Install_Episode_Name.foreground_color = (0,1,0,1) if self.ids.Text_Install_Episode_Name.text not in [i['item_Fragment'] for i in self.ids.List_Dest_Episode.data] else (1,.5,0,1)

	def Remove_Anime(self, Selection):
		if len(Selection) == 0: MsgBox(self, 'Nothing selected to uninstall.')
		else:
			global MOD
			for i in MOD.query('World in ' + str(Selection) + ' and Status in ' + str(['Conquered', 'Resonated']) + ' and Protocol in ' + str(Protocol[4:6])).index: [MOD['Fragments'][i], MOD['Protocol'][i]] = [[], MOD['Protocol'][i].replace('OUTER', 'AMORPHOUS')]
			MOD = MOD.query('World not in ' + str(Selection) + ' or Status in ' + str(['Conquered', 'Resonated'])).reset_index(drop=True) #IMPORTANT: DON'T DROP 'CONQUERED' OR 'IN PROGRESS' status otherwise the Reminiscence will be broken. Instead, I emptied it.
			if Selected_Anime_Name in Selection: self.Select_Anime(None) #Unselect if currently selected
			self.Update_Stats(False,False,True,True)
			self.Select_Mode_Anime('Assemble')
			print(Selection)
			self.Save(False)
			MsgBox(self, str(len(Selection)) + (' World' if len(Selection) == 1 else ' Worlds') + ' uninstalled.')

	def Remove_Episode(self, Selection):
		if len(Selection) == 0: MsgBox(self, 'Nothing selected to uninstall.')
		else:
			global Selected_Anime_Protocol_Edit
			Selection = [i + '.mp4' for i in Selection]
			MOD['Fragments'][MOD[MOD['World'] == Selected_Anime_Name_Edit].index[0]] = [i for i in MOD['Fragments'][MOD['World'] == Selected_Anime_Name_Edit].reset_index(drop=True)[0] if i not in Selection]
			if len(MOD['Fragments'][MOD['World'] == Selected_Anime_Name_Edit].reset_index(drop=True)[0]) == 0: MOD['Protocol'][MOD[MOD['World'] == Selected_Anime_Name_Edit].index[0]] = MOD['Protocol'][MOD[MOD['World'] == Selected_Anime_Name_Edit].index[0]].replace('OUTER', 'AMORPHOUS') #Change Protocol
			Selected_Anime_Protocol_Edit = MOD['Protocol'][MOD['World'] == Selected_Anime_Name_Edit].reset_index(drop=True)[0]
			self.Update_Anime(Selected_Anime_Name_Edit)
			self.Update_Stats(False,False,True,True)
			self.Select_Mode_Episode('Assemble')
			self.Save(False)
			MsgBox(self, str(len(Selection)) + ' Fragments uninstalled on ' + Selected_Anime_Name_Edit + '.')

	def Combine_Select(self):
		global Selected_Anime_ToCombine
		Selected_Anime_ToCombine = [self.ids.List_Dest_Anime.data[i]['item_World'] for i in self.ids.List_Dest_Anime._layout_manager.selected_nodes]
		if len(Selected_Anime_ToCombine) == 0: MsgBox(self, 'Nothing selected to combine.')
		else:
			global MOD
			self.Fill_List_Dest_Anime(MOD.query('World not in ' + str(Selected_Anime_ToCombine)).query('Protocol in ' + str(Protocol[4:])).reset_index(drop=True)) #Remove selected worlds from the list
			self.ids.List_Dest_Anime._layout_manager.multiselect = self.ids.Button_Menu_Execute.disabled = False #Turn off multiselection and enable Execute button
			self.ids.Button_Menu_Combine.disabled = self.ids.Button_Menu_Install_Anime.disabled = self.ids.Button_Menu_Uninstall_Anime.disabled = True #Disable others
			for i in self.ids.List_Dest_Anime.data: i['item_color_World'] = (.5,.75,1,1) #Change list color
			self.ids.Button_Menu_Execute.on_release = self.Combine_Execute
			print(Selected_Anime_ToCombine)
			MsgBox(self, str(len(Selected_Anime_ToCombine)) + (' World' if len(Selected_Anime_ToCombine) == 1 else ' Worlds') + ' selected. Please select a world to Combine with.')

	def Combine_Execute(self):
		Selection = [self.ids.List_Dest_Anime.data[i]['item_World'] for i in self.ids.List_Dest_Anime._layout_manager.selected_nodes]
		if len(Selection) == 0: MsgBox(self, 'Please select a world to Combine with.')
		else:
			MOD['Fragments'][MOD[MOD['World'] == Selection[0]].index[0]] = MOD['Fragments'][MOD['World'] == Selection[0]].reset_index(drop=True)[0] + MOD.query('World in ' + str(Selected_Anime_ToCombine))['Fragments'].values.sum() #Assign combination to MOD
			MOD['Protocol'][MOD['World'] == Selection[0]] = MOD['Protocol'][MOD['World'] == Selection[0]].reset_index(drop=True)[0].replace('AMORPHOUS', 'OUTER' if len(MOD['Fragments'][MOD['World'] == Selection[0]].reset_index(drop=True)[0]) != 0 else 'AMORPHOUS') #Update Protocol
			self.Remove_Anime(Selected_Anime_ToCombine)
			if Selected_Anime_Name == Selection[0]: #If currently selected
				Selected_Anime_Protocol = MOD['Protocol'][MOD['World'] == Selected_Anime_Name].reset_index(drop=True)[0]
				self.ids.Label_Selected_Anime_Protocol.text = 'Protocol: ' + Selected_Anime_Protocol
				Selected_Anime_Fragments = len(MOD['Fragments'][MOD['World'] == Selected_Anime_Name].reset_index(drop=True)[0])
				self.ids.Label_Selected_Anime_Fragmented.text = str(Selected_Anime_Fragmented) + '/' + (str(Selected_Anime_Fragments) if Selected_Anime_Fragments != 0 else '???')
			MsgBox(self, str(len(Selected_Anime_ToCombine)) +  (' World' if len(Selected_Anime_ToCombine) == 1 else ' Worlds') + ' combined into ' + Selection[0] + '.')

	def Transfer_Select(self):
		global Selected_Episode_ToCombine
		Selected_Episode_ToCombine = [self.ids.List_Dest_Episode.data[i]['item_Fragment'] for i in self.ids.List_Dest_Episode._layout_manager.selected_nodes]
		if len(Selected_Episode_ToCombine) == 0: MsgBox(self, 'Nothing selected to transfer.')
		else:
			self.Fill_List_Dest_Anime(MOD.query('Protocol in ' + str(Protocol[4:]))[MOD['World'] != Selected_Anime_Name_Edit].reset_index(drop=True)) #Remove selected world from the list
			self.ids.List_Dest_Anime._layout_manager.multiselect = self.ids.Button_Menu_Execute.disabled = False #Turn off multiselection and enable Execute button
			self.ids.Button_Menu_Combine.disabled = self.ids.Button_Menu_Install_Anime.disabled = self.ids.Button_Menu_Uninstall_Anime.disabled = True #Disable others
			for i in self.ids.List_Dest_Anime.data: i['item_color_World'] = (.5,.75,1,1) #Change list color
			[self.ids.Management_Misc.current, self.ids.Management_Menu.current] = ['Screen_Misc_Anime', 'Screen_Menu_Assemble_Anime'] #Shift
			self.ids.Button_Menu_Execute.on_release = self.Transfer_Execute
			print(Selected_Episode_ToCombine)
			MsgBox(self, str(len(Selected_Episode_ToCombine)) + (' Fragment' if len(Selected_Episode_ToCombine) == 1 else ' Fragments') + ' selected. Please select a world to Transfer to.')

	def Transfer_Execute(self):
		Selection = [self.ids.List_Dest_Anime.data[i]['item_World'] for i in self.ids.List_Dest_Anime._layout_manager.selected_nodes]
		if len(Selection) == 0: MsgBox(self, 'Please select a world to Transfer to.')
		else:
			MOD['Fragments'][MOD[MOD['World'] == Selection[0]].index[0]] += [i + '.mp4' for i in Selected_Episode_ToCombine] #Assign combination to MOD
			MOD['Protocol'][MOD['World'] == Selection[0]] = MOD['Protocol'][MOD['World'] == Selection[0]].reset_index(drop=True)[0].replace('AMORPHOUS', 'OUTER' if len(MOD['Fragments'][MOD['World'] == Selection[0]].reset_index(drop=True)[0]) != 0 else 'AMORPHOUS') #Update Protocol
			self.Remove_Episode(Selected_Episode_ToCombine)
			self.Select_Mode_Anime('Assemble')

	def AlterProtocol_Confirm(self):
		[Settings['Protocol: CENTRAL REGNUM'], Settings['Protocol: LUX DOMINIUM'], Settings['Protocol: NOBILIS MUNDI'], Settings['Protocol: MYSTERIUM FIDEI'], Settings['Protocol: INCERTUS TERRAE']] =  [self.ids.Text_Protocol_1.text, self.ids.Text_Protocol_2.text, self.ids.Text_Protocol_3.text, self.ids.Text_Protocol_4.text, self.ids.Text_Protocol_5.text]
		self.ids.Button_AlterProtocol_Confirm.color = (0,1,1,1)
		self.Save(False)

	def AlterProtocol_Reset(self):
		[self.ids.Text_Protocol_1.text, self.ids.Text_Protocol_2.text, self.ids.Text_Protocol_3.text, self.ids.Text_Protocol_4.text, self.ids.Text_Protocol_5.text] = [Settings['Protocol: ' + i] for i in (Protocol[:4] + ['INCERTUS TERRAE'])]
		self.ids.Button_AlterProtocol_Confirm.color = (0,1,1,1)

	def AlterProtocol_Check(self, n, Unconfirm):
		exec('self.ids.Text_Protocol_' + str(n+1) + '.foreground_color = (0,1,0,1) if os.path.isdir(self.ids.Text_Protocol_' + str(n+1) + '.text) else (1,0,0,1)')
		if Unconfirm: self.ids.Button_AlterProtocol_Confirm.color = (1,1,0,1)

	def MissionFunction_Confirm(self):
		[Settings['Objective_Easy'], Settings['Objective_Normal'], Settings['Objective_Hard'], Settings['Objective_Insane']] =  [self.ids.Text_Function_1.text, self.ids.Text_Function_2.text, self.ids.Text_Function_3.text, self.ids.Text_Function_4.text]
		self.Update_Mission()
		self.ids.Button_MissionFunction_Confirm.color = (0,1,1,1)
		self.Save(False)

	def MissionFunction_Reset(self):
		[self.ids.Text_Function_1.text, self.ids.Text_Function_2.text, self.ids.Text_Function_3.text, self.ids.Text_Function_4.text] = [Settings['Objective_' + i] for i in ['Easy', 'Normal', 'Hard', 'Insane']]
		self.ids.Button_MissionFunction_Confirm.color = (0,1,1,1)

	def Synchronize(self):
		global MOD
		for i in Protocol[:4]: #For every protocol
			if not os.path.isdir(Settings['Protocol: ' + i]): pass #If protocol not exist
			else: #If Protocol exist
				x = MOD.query('World in ' + str(next(os.walk(Settings['Protocol: ' + i]))[1])).index #Get indexes of all existing Worlds in MOD
				y = pd.Series(data = [next(os.walk(Settings['Protocol: ' + i] + '\\' + MOD['World'][j]))[2] for j in x], index = x) # Series of List of Episodes in each World
				z = pd.Series(data = [i] * len(x), index = x) #Series of Protocol
				MOD.update(y.to_frame('Fragments')) #Combine it into MOD
				MOD.update(z.to_frame('Protocol')) #Combine it into MOD
				n = [j for j in next(os.walk(Settings['Protocol: ' + i]))[1] if j not in MOD['World'].tolist()] #List of newly added
				if len(n) != 0: MOD = MOD.append(pd.DataFrame(data={'World': n,
																	'Protocol': [i] * len(n),
																	'Fragments': [next(os.walk(Settings['Protocol: ' + i] + '\\' + j))[2] for j in n],
																	'Status': ['Unfragmented'] * len(n),
																	'Fragmented': [0] * len(n),
																	'Order': [np.nan] * len(n)}), ignore_index=True)
				x = MOD.query('World not in ' + str(next(os.walk(Settings['Protocol: ' + i]))[1]))[MOD['Protocol'] == i].index #Get indexes of all NON-existing Worlds in MOD
				y = pd.Series(data = [list(map(lambda k: k[:-3] + 'mp4', MOD['Fragments'][j])) for j in x], index = x) # Series of List of Episodes in each World (converted into mp4)
				z = pd.Series(data = [('OUTER ' if len(MOD['Fragments'][j]) != 0 else 'AMORPHOUS ') + ('SAPIENTIA' if MOD['Protocol'][j] in Protocol[:3] else 'MYSTERIUM') for j in x], index = x) #Series of Protocol
				MOD.update(y.to_frame('Fragments')) #Combine it into MOD
				MOD.update(z.to_frame('Protocol')) #Combine it into MOD
		Sort(self)
		self.Save(False)
		MsgBox(self, 'Synchronize completed.')

	def Backup(self):
		if self.Backup_Check(): #If path exist
			FolderName = 'MAGNUM OPUS DEI ' + str(datetime.datetime.now().year) + "%02d" % (datetime.datetime.now().month) + "%02d" % (datetime.datetime.now().day) + (' (' + self.ids.Text_Backup_Msg.text + ')' if self.ids.Text_Backup_Msg.text != '' else '') #Create folder name
			if os.path.isdir(self.ids.Text_Backup_Protocol.text + '\\' + FolderName): #If already exist
				if self.ids.Label_Backup_OnExisting.text == 'Overwrite':
					shutil.rmtree(self.ids.Text_Backup_Protocol.text + '\\' + FolderName)
					self.Save(True)
					shutil.copytree(os.getcwd(), self.ids.Text_Backup_Protocol.text + '\\' + FolderName) #Copy this folder
					MsgBox(self, 'Remnant already exist. Old remnant has been overwritten.')
				elif self.ids.Label_Backup_OnExisting.text == 'Duplicate':
					self.Save(True)
					i = 0
					while os.path.isdir(self.ids.Text_Backup_Protocol.text + '\\' + FolderName + ' (' + str(i) + ')'): i += 1 #Check if New named folder exist
					shutil.copytree(os.getcwd(), self.ids.Text_Backup_Protocol.text + '\\' + FolderName + ' (' + str(i) + ')') #Copy this folder
					MsgBox(self, 'Remnant already exist. Recreated new remnant.')
				elif self.ids.Label_Backup_OnExisting.text == 'Cancel': MsgBox(self, 'Remnant already exist. Create remnant aborted.')
			else:
				self.Save(True)
				shutil.copytree(os.getcwd(), self.ids.Text_Backup_Protocol.text + '\\' + FolderName) #Copy this folder
		else: MsgBox(self, 'Destination not found. Failed to create remnant')

	def Backup_Check(self):
		x = os.path.isdir(self.ids.Text_Backup_Protocol.text)
		if x: self.ids.Text_Backup_Protocol.foreground_color = (0,1,0,1)
		else: self.ids.Text_Backup_Protocol.foreground_color = (1,0,0,1)
		return x

	def Backup_Reset(self):
		self.ids.Text_Backup_Protocol.text = Settings['Backups']

	def Backup_Set(self):
		Settings['Backups'] = self.ids.Text_Backup_Protocol.text
		self.Save(False)
		MsgBox(self, 'New Backup location has been set.')

	def SetOpacity(self, i):
		hwnd = win32gui.GetForegroundWindow()
		win32gui.SetWindowLong (hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
		winxpgui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), int(i), win32con.LWA_ALPHA)

	def FullScreen(self, i):
		Window.fullscreen = i

	def Upload(self):
		global LOG
		access_token = self.ids.Text_AccessToken.text
		dbx = dropbox.Dropbox(access_token)
		for From in ['INTERCONNECTION SYNAPSIS.py', 'MAGNUM OPUS DEI.csv', 'LOG.csv', 'SETTINGS.csv']: 
			print('Uploading: ' + From)
			To = '/MEMORIA EPHEMERAL/' + From
			try: 
				with open(From, 'rb') as f: dbx.files_upload(f.read(), To, mode=dropbox.files.WriteMode.overwrite)
			except Exception as i:
				print('Upload error: ' + From)
				print(i)
		print('Upload completed.')

	def Upload_Reset(self):
		self.ids.Text_AccessToken.text = Settings['Access_Token']

	def Upload_Set(self):
		if Settings['Access_Token'] != self.ids.Text_AccessToken.text: 
			Settings['Access_Token'] = self.ids.Text_AccessToken.text
			self.Save(False)
			MsgBox(self, 'New Access Token has been set.')

	def Save(self, save):
		global Saved
		Saved = save
		if Saved:
			[Settings['Year_Initial'], Settings['Day_Initial']] = [Year_Running, Day_Running]
			Settings.to_csv('SETTINGS.csv', index=True, header=False)
			MOD.to_csv('MAGNUM OPUS DEI.csv', index=False, header=True)
			self.ids.Button_Menu_Save.color = (0,1,1,1)
			MsgBox(self, 'Save completed.')
			LOG.to_csv('LOG.csv', index=False, header=True)
			if self.ids.Check_Upload.active: threading.Thread(target=self.Upload).start()
		else: self.ids.Button_Menu_Save.color = (1,1,0,1)

#Other Classes
class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,RecycleGridLayout): pass
class List_Dest_Anime(RecycleView): pass
class List_Dest_Episode(RecycleView): pass
class SBL_Dest_Anime(RecycleDataViewBehavior, BoxLayout):
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)
	DoubleTap = False
	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		return super(SBL_Dest_Anime, self).refresh_view_attrs(rv, index, data)
	def on_touch_down(self, touch):
		if super(SBL_Dest_Anime, self).on_touch_down(touch): return True
		if self.collide_point(*touch.pos) and self.selectable:
			self.DoubleTap = touch.is_double_tap 
			return self.parent.select_with_touch(self.index, touch)
	def apply_selection(self, rv, index, is_selected):
		self.selected = is_selected
		if self.DoubleTap:
			if Selected_Mode_Anime == 'Assemble': 
				if App.get_running_app().root.ids.Button_Menu_Execute.disabled: App.get_running_app().root.Select_Anime_Assemble(rv.data[rv._layout_manager._last_selected_node]['item_World'], rv.data[rv._layout_manager._last_selected_node]['item_Protocol'])
			else: App.get_running_app().root.Select_Anime(rv.data[index]['item_World'])
			self.DoubleTap = False 
class SBL_Dest_Episode(RecycleDataViewBehavior, BoxLayout):
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)
	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		return super(SBL_Dest_Episode, self).refresh_view_attrs(rv, index, data)
	def on_touch_down(self, touch):
		if super(SBL_Dest_Episode, self).on_touch_down(touch): return True
		if self.collide_point(*touch.pos) and self.selectable: return self.parent.select_with_touch(self.index, touch)
	def apply_selection(self, rv, index, is_selected):
		self.selected = is_selected
		if self.selected and Selected_Mode_Anime != 'Assemble': App.get_running_app().root.Select_Episode(rv.data[index]['item_Fragment'], rv.data[index]['item_Extension_Real'])

class InterconnectionSynapsis(App):
	def build(self):
		self.title = 'Interconnection Synapsis'
		Window.maximize()
		Config.set('input', 'mouse', 'mouse,disable_multitouch')
		return Nexus_Initial()

#Run App
if __name__ == '__main__': InterconnectionSynapsis().run()