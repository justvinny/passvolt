'''
Simple password manager app to store complex passwords for various platforms.
This project's GUI is made with tkinter and python 3x. 

Author: github.com/justvinny

Dependencies: pyperclip 
'''

import tkinter as tk
import tkinter.ttk as ttk
import shelve
import pyperclip

buttonColor = '#0099ff' # Background color for all active buttons.
menuColor = '#2f2f1e' # Background color for all buttons. 

# Changes button color when mouse cursor hovers over it.
# This function is made specifically for windows as tkinter.button['activebackground'] doesn't work as intended.
def on_enter(event, button):
        button['bg'] = buttonColor

# Changes button color back to normal when mouse cursor stops hovering over it.
# This function is made specifically for windows as tkinter.button['activebackground'] doesn't work as intended.
def on_leave(event, button):
        button['bg'] = menuColor
        
        
# Login Screen
class Login(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		self.m_frame_config()
		self.m_frame()

		self.place(relx=.25, rely=0.03, relwidth=.74, relheight=.91)

	# All configuration for the App frame goes here. 
	def m_frame_config(self):
		self.config(bg='white')

	# All the widgets for m_frame. 
	def m_frame(self):
		# Defining our style
		self.style = ttk.Style()
		self.style.configure('TLabel', background='white', font=('Helvetica',15,'bold'))
		self.style.configure('Title.TLabel', background='white', font=('Helvetica',30, 'bold','underline'))
		# Defining our label widgets.
		self.labelTitle = ttk.Label(self, text='Pass Volt', style='Title.TLabel', anchor='center')
		self.labelSword = ttk.Label(self, text='Username ', anchor='e')
		self.labelPword = ttk.Label(self, text='Password ', anchor='e')
		self.labelStatus = tk.Label(self, text='', bg='white', font=('Helvetica',15,'bold'), anchor='center')
		# Defining our entry widgets.
		self.entrySword = tk.Entry(self)
		self.entryPword = tk.Entry(self, show='*')
		# Defining our submit button. 
		self.buttonSubmit = tk.Button(self, text='Submit', font=('Helvetica',15,'bold'), bg=menuColor, fg='white',
		 activebackground=buttonColor, command=self.submit_call)
		self.buttonSubmit.bind('<Return>', lambda event: self.submit_call(event))
		# Bindings for buttons to change color when mouse hovers over them on Windows OS.
		self.buttonSubmit.bind('<Enter>', lambda event: on_enter(event, self.buttonSubmit))
		self.buttonSubmit.bind('<Leave>', lambda event: on_leave(event, self.buttonSubmit))

		# Packing our widgets onto the screen.
		self.labelTitle.place(relx=.25, rely=.18, relwidth=.5, relheight=.1)
		self.labelSword.place(relx=.25, rely=.33, relwidth=.25, relheight=.05)
		self.entrySword.place(relx=.5, rely=.33, relwidth=.23, relheight=.05)
		self.labelPword.place(relx=.25, rely=.39, relwidth=.25, relheight=.05)
		self.entryPword.place(relx=.5, rely=.39, relwidth=.23, relheight=.05)
		self.buttonSubmit.place(relx=.375, rely=.45, relwidth=.25, relheight=.08)
		self.labelStatus.place(relx=0, rely=.55, relwidth=1, relheight=.05)

	# Check if input matches the one stored in database and then open a new frame. 
	def submit_call(self, event=None):
		checkIfEmpty = ''

		with shelve.open('data') as file:
			for each in file:
				checkIfEmpty += each

		# If dbm file is empty, register a new account based on user input. 
		if checkIfEmpty == '':
			# Very simple input validation just to ensure user doesn't accidentally register a blank account.
			if len(self.entrySword.get()) < 8 or len(self.entryPword.get()) < 8:
				self.labelStatus['fg'] = 'red'
				self.labelStatus['text'] = 'Invalid username or password.'
			
			else:
				with shelve.open('data') as file:
					file['user'] = self.entrySword.get()
					file['pword'] = self.entryPword.get()

					self.labelStatus['fg'] = 'green'
					self.labelStatus['text'] = 'Account successfully registered! Logging in...'
					self.after(1500, self.submit_call)

		# If dbm file is NOT empty, move to the next window if account details are correct. 
		else:
			with shelve.open('data') as file:
					# Checks if username and password matches what is stored in the dbm file. 
					if self.entrySword.get() == file['user'] and self.entryPword.get() == file['pword']:
						self.labelStatus['fg'] = 'green'
						self.labelStatus['text'] = 'Success!'
						self.after(1500, self.new_window)
					else:
						self.labelStatus['fg'] = 'red'
						self.labelStatus['text'] = 'Wrong password!'

	def new_window(self):
		self.destroy()
		ourMenu.menu_buttons()
		ourMenu.menu_logo()
		ourMenu.home_call()


# Main window after successful login.
class MainMenu(tk.Frame):
	def __init__(self,master):
		super().__init__(master)
		self.master = master
		self.master.geometry('850x550')

		self.frame_config()
		self.frame_menu()

		self.pack(fill=tk.BOTH, expand=True)

	# All configuration for MainMenu frame goes here. 
	def frame_config(self):
		self['bg'] = menuColor

	# Main menu frame and its widgets.
	def frame_menu(self):
		self.menu = tk.Frame(self, bg=menuColor)
		self.menu.place(relwidth=.25, relheight=1)

	# Main menu title/logo.
	def menu_logo(self):
		# Defining our title/logo label widget.
		self.labelLogo = tk.Label(self.menu, text='Pass Volt', bg=menuColor, fg='white', font=('Verdana', 16, 'bold'), anchor='s')
		# Defining our lines for menu styling.
		self.labelLine = tk.Label(self.menu, bg='#1a1a10')
		self.labelLine2 = tk.Label(self.menu, bg='#1a1a10')

		# Placing all of the widgets on to self.menu frame. 
		self.labelLogo.place(relwidth=1, relheight=.11)
		self.labelLine.place(rely=.14, relwidth=1, relheight=.0025)
		self.labelLine2.place(rely=.39, relwidth=1, relheight=.0025)

	# Main menu frame and its widgets.
	def menu_buttons(self):
		# Boolean values to check which frame--HomeFrame, RegisterFrame or RemoveFrame--is being used.
		self.fHome = False
		self.fRegister = False
		self.fRemove = False

		# Defining our widgets for the menu frame.
		self.buttonHome = tk.Button(self.menu, text='Home', command=self.home_call)
		self.buttonRegister = tk.Button(self.menu, text='Register', command=self.register_call)
		self.buttonRemove = tk.Button(self.menu, text='Remove', command=self.remove_call)
		self.buttonBack = tk.Button(self.menu, text='Exit', command=root.destroy)

		# Configure our button properties
		for each in [self.buttonHome, self.buttonRegister, self.buttonRemove, self.buttonBack]:
			each['bg'] = menuColor
			each['fg'] = 'white'
			each['bd'] = 0
			each['highlightthickness'] = 0
			each['activebackground'] = buttonColor
			each['font'] = ('Verdana', 10, 'bold')
			# Bindings for buttons to change color when mouse hovers over them on Windows OS.
			each.bind('<Enter>', lambda event, button = each: on_enter(event, button))
			each.bind('<Leave>', lambda event, button = each: on_leave(event, button))

		# Placing our widgets onto the menu frame. 
		self.buttonHome.place(rely=.15, relwidth=1, relheight=.05)
		self.buttonRegister.place(rely=.21, relwidth=1, relheight=.05)
		self.buttonRemove.place(rely=.27, relwidth=1, relheight=.05)
		self.buttonBack.place(rely=.33, relwidth=1, relheight=.05)

	# Check which frame to destroy.
	def check_destroy(self):
		if self.fHome:
			self.home.destroy()
			self.fHome = False

		elif self.fRegister:
			self.register.destroy()
			self.fRegister = False

		elif self.fRemove:
			self.remove.destroy()
			self.fRemove = False

	# Create home frame where we can get our stored accounts. 
	def home_call(self):
		self.check_destroy()
		self.home = HomeFrame(self)
		self.fHome = True

	# Create register frame that has inputs to store new platforms and accounts.
	def register_call(self):
		self.check_destroy()
		self.register = RegisterFrame(root)
		self.fRegister = True

	# Create remove frame for deleting current platforms and accounts.	
	def remove_call(self):
		self.check_destroy()
		self.remove = RemoveFrame(root)
		self.fRemove = True


# Status bar frame and its widgets.
class StatusFrame(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self['bg'] = 'white'

		self.status_bar()

		self.place(relx=.25, rely=.9525, relwidth=.74, relheight=.035)

	def status_bar(self):
		self.statusVar = tk.StringVar()
		self.statusLabel = tk.Label(self, textvariable=self.statusVar, bg='white', anchor='e')
		self.statusLabel.pack(fill=tk.BOTH, expand=True)

		
# Home frame for getting your stored passwords for each platform.
class HomeFrame(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self['bg'] = 'white'

		self.home_frame()

		self.place(relx=.25, rely=0.03, relwidth=.74, relheight=.91)

	# Defining and placing our widgets to the frame.
	def home_frame(self):
		self.buttonDic = {} # Dictionary containing our dbm file buttons
		self.xPos = .025
		self.yPos = .025 
		self.buttonFrame = tk.Frame(self, bg='white')
		self.buttonFrame.place(rely=.115, relwidth=1, relheight=.83)

		# Defining our buttons based on the contents of dbm file and storing them into a dictionary.
		with shelve.open('platform') as file:
			for each in file:
				self.buttonDic.setdefault(each, tk.Button(self.buttonFrame, text=each.title(),
				 command= lambda event = each: self.get_password(event)))

		# Configuring the button appearance.
		for each in self.buttonDic.keys():
			self.buttonDic[each]['bg'] = menuColor
			self.buttonDic[each]['fg'] = 'white'
			self.buttonDic[each]['activebackground'] = buttonColor
			self.buttonDic[each]['activeforeground'] = 'white'
			self.buttonDic[each]['bd'] = 0
			self.buttonDic[each]['highlightthickness'] = 0
			self.buttonDic[each]['font'] = ('Verdana', 10, 'bold')
			# Bindings for buttons to change color when mouse hovers over them on Windows OS.
			self.buttonDic[each].bind('<Enter>', lambda event, button=self.buttonDic[each]: on_enter(event, button))
			self.buttonDic[each].bind('<Leave>', lambda event, button=self.buttonDic[each]: on_leave(event, button))

		# Placing our buttons from the dictionary to the HomeFrame. 
		for each in self.buttonDic.keys():
			self.buttonDic[each].place(relx=self.xPos, rely=self.yPos, relwidth=.3, relheight=.3)
			self.xPos += .325
			if self.xPos > .9:
				self.xPos = .025
				self.yPos += .325

		# Defining our title label.
		self.labelHome = tk.Label(self, text='Stored Accounts', bg='white', font=('Verdana', 16, 'bold'), anchor='center')
		self.labelLine = tk.Label(self, bg=menuColor)

		# Placing our label onto the frame.
		self.labelHome.place(relwidth=1, relheight=.1)
		self.labelLine.place(rely=.1, relwidth=1, relheight=.015)
			
	# Get passwords for platform on press from the dbm file. 
	def get_password(self, event):

		with shelve.open('platform') as file:
			pyperclip.copy(file[event]['pass'])
			tempString = file[event]['user']
			ourStatus.statusVar.set(f'Your password for {tempString} on {event.title()} has been copied to clipboard')


# New window for registering new platforms and accounts. 
class RegisterFrame(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self['bg'] = 'white'

		self.register_frame()

		self.place(relx=.25, rely=0.03, relwidth=.74, relheight=.91)

	# All the widgets for RegisterFrame go here. 
	def register_frame(self):
		# Defining our label widgets.
		self.labelRegister = tk.Label(self, text='Register New Account', bg='white', font=('Verdana', 16, 'bold'), anchor='center')
		self.labelLine = tk.Label(self, bg=menuColor)
		self.labelPlatform = tk.Label(self, text='Platform ', bg='white', anchor='e')
		self.labelUsername = tk.Label(self, text='Username ', bg='white',  anchor='e')
		self.labelPassword = tk.Label(self, text='Password ', bg='white',  anchor='e')
		# Defining our entry widgets. 
		self.entryPlatform = tk.Entry(self)
		self.entryUsername = tk.Entry(self)
		self.entryPassword = tk.Entry(self, show='*') 
		# Defining our button widget. 
		self.buttonCreate = tk.Button(self, text='Create', bg=menuColor, fg='white', activebackground=buttonColor,
			bd=0, highlightthickness=0, font=('Verdana', 10, 'bold'), command=self.create_call)
		# Bindings for buttons to change color when mouse hovers over them on Windows OS.
		self.buttonCreate.bind('<Enter>', lambda event: on_enter(event, self.buttonCreate))
		self.buttonCreate.bind('<Leave>', lambda event: on_leave(event, self.buttonCreate))

		# Placing our widgets on the frame. 
		self.labelRegister.place(relwidth=1, relheight=.1)
		self.labelLine.place(rely=.1, relwidth=1, relheight=.015)
		self.labelPlatform.place(relx=.23, rely=.3, relwidth=.2, relheight=.05)
		self.labelUsername.place(relx=.23,rely=.37, relwidth=.2, relheight=.05)
		self.labelPassword.place(relx=.23,rely=.44, relwidth=.2, relheight=.05)
		self.entryPlatform.place(relx=.43, rely=.3, relwidth=.25, relheight=.05)
		self.entryUsername.place(relx=.43, rely=.37, relwidth=.25, relheight=.05)
		self.entryPassword.place(relx=.43, rely=.44, relwidth=.25, relheight=.05) 
		self.buttonCreate.place(relx=.35, rely=.51, relwidth=.28, relheight=.05)

	# Create a new account and add it to dbm file.
	def create_call(self):
		with shelve.open('platform') as file:
			tempTitle = self.entryPlatform.get().title()
			file[self.entryPlatform.get().lower()] = {'user':self.entryUsername.get(),'pass':self.entryPassword.get()}
			ourStatus.statusVar.set(f'{tempTitle} is successfully registered')

		self.entryPlatform.delete(0, tk.END)
		self.entryUsername.delete(0, tk.END)
		self.entryPassword.delete(0, tk.END)


# New window to delete existing platforms and accounts. 
class RemoveFrame(tk.Frame):
	def __init__(self,master):
		super().__init__(master)
		self.master = master
		self['bg'] = 'white'

		self.remove_frame()

		self.place(relx=.25, rely=0.03, relwidth=.74, relheight=.91)

	# Place all our RemoveFrame widgets here.  
	def remove_frame(self):
		self.buttonDic = {} # Dictionary containing our dbm file buttons
		self.xPos = .025
		self.yPos = .025 
		self.buttonFrame = tk.Frame(self, bg='white')
		self.buttonFrame.place(rely=.115, relwidth=1, relheight=.83)

		# Defining our buttons based on the contents of dbm file and storing them into a dictionary.
		with shelve.open('platform') as file:
			for each in file:
				self.buttonDic.setdefault(each, tk.Button(self.buttonFrame, text=each.title(), 
					command=lambda event=each: self.select_call(event)))

		# Configuring the button appearance.
		for each in self.buttonDic.keys():
			self.buttonDic[each]['bg'] = menuColor
			self.buttonDic[each]['fg'] = 'white'
			self.buttonDic[each]['activebackground'] = buttonColor
			self.buttonDic[each]['activeforeground'] = 'white'
			self.buttonDic[each]['bd'] = 0
			self.buttonDic[each]['highlightthickness'] = 0
			self.buttonDic[each]['font'] = ('Verdana', 10, 'bold')
			# Bindings for buttons to change color when mouse hovers over them on Windows OS.
			self.buttonDic[each].bind('<Enter>', lambda event, button=self.buttonDic[each]: on_enter(event, button))
			self.buttonDic[each].bind('<Leave>', lambda event, button=self.buttonDic[each]: on_leave(event, button))

		# Placing our buttons from the dictionary to the HomeFrame. 
		for each in self.buttonDic.keys():
			self.buttonDic[each].place(relx=self.xPos, rely=self.yPos, relwidth=.3, relheight=.3)
			self.xPos += .325
			if self.xPos > .9:
				self.xPos = .025
				self.yPos += .325

		# Defining our label widgets.
		self.labelRemove = tk.Label(self, text='Remove Account', bg='white', font=('Verdana', 16, 'bold'), anchor='center')
		self.labelLine = tk.Label(self, bg=menuColor)

		# Defining our delete button widget.
		self.buttonDelete = tk.Button (self, text='Delete Selected', bg=menuColor, fg='white', activebackground=buttonColor,
			bd=0, highlightthickness=0, font=('Verdana', 10, 'bold'), command=self.delete_call)
		# Bindings for buttons to change color when mouse hovers over them on Windows OS.
		self.buttonDelete.bind('<Enter>', lambda event: on_enter(event, self.buttonDelete))
		self.buttonDelete.bind('<Leave>', lambda event: on_leave(event, self.buttonDelete))

		# Placing all other widgets to the screen. 
		self.labelRemove.place(relwidth=1, relheight=.1)
		self.labelLine.place(rely=.1, relwidth=1, relheight=.015)
		self.buttonDelete.place(relx=.35, rely=.937, relwidth=.3, relheight=.05 )

	# Changes background for selected buttons. This method is connected to self.delete_call. 
	def select_call(self, event):
		if self.buttonDic[event]['bg'] == menuColor:
			self.buttonDic[event]['bg'] = buttonColor
		else:
			self.buttonDic[event]['bg'] = menuColor

	# Deletes the selected buttons in our dbm file. 
	def delete_call(self):
		deleted = []
		for each in self.buttonDic.keys():
			if self.buttonDic[each]['bg'] == buttonColor:
				deleted.append(each)
				with shelve.open('platform') as file:
					del file[each]
		deletedString = ','.join(deleted)
		ourMenu.remove_call()
		ourStatus.statusVar.set(f' {deletedString} have been deleted')

# Run our app.
if __name__ == '__main__':
	root = tk.Tk()
	root.title('Pass Volt')
	root.geometry('850x550')
	ourMenu = MainMenu(root)
	Login(ourMenu)
	ourStatus = StatusFrame(root)
	root.mainloop()
