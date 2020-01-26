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

buttonColor = 'silver' # Background color for all buttons


# Login Screen
class App(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		self.m_frame_config()
		self.m_frame()

		self.place(relx=.05, rely=.05, relwidth=.9, relheight=.9)

	def m_frame_config(self):
		self.config(bg='white')

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
		self.buttonSubmit = tk.Button(self, text='Submit', font=('Helvetica',15,'bold'), bg=buttonColor, fg='black', command=self.submit_call)
		self.buttonSubmit.bind('<Return>', lambda event: self.submit_call(event))

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
			# Very simple input validation just to assure user doesn't accidentally reigster a blank account.
			if len(self.entrySword.get()) < 8 or len(self.entryPword.get()) < 8:
				self.labelStatus['fg'] = 'red'
				self.labelStatus['text'] = 'Invalid username or password.'
			
			else:
				with shelve.open('data') as file:
					file['user'] = self.entrySword.get()
					file['pword'] = self.entryPword.get()

					self.labelStatus['fg'] = 'green'
					self.labelStatus['text'] = 'Account successfully registered! Logging in!'
					self.after(1000, self.submit_call)

		# If dbm file is NOT empty, move to the next window if account details are correct. 
		else:
			with shelve.open('data') as file:
					# Checks if username and password matches what is stored in the dbm file. 
					if self.entrySword.get() == file['user'] and self.entryPword.get() == file['pword']:
						self.labelStatus['fg'] = 'green'
						self.labelStatus['text'] = 'Success!'
						self.destroy()
						MainWindow(root)
					
					else:
						self.labelStatus['fg'] = 'red'
						self.labelStatus['text'] = 'Wrong password!'


# Main window after successful login.
class MainWindow(tk.Frame):
	def __init__(self,master):
		super().__init__(master)
		self.master = master

		self.frame_config()

		self.top_frame()
		self.mid_frame()
		self.bot_frame()

		self.pack(fill=tk.BOTH, expand=True)

	def frame_config(self):
		self['bg'] = 'black'

	def top_frame(self):
		self.platforms = []
		self.buttonsDic = {}
		self.mButtonPos = 0.075

		self.topFrame = tk.Frame(self, bg='white')
		self.topFrame.place(relheight=.7, relwidth=1)

		tk.Label(self.topFrame, bg='white').pack()

		# Check paltforms data file for a list of services/platforms you are using that has a saved password
		with shelve.open('platform') as file:
			for each in file:
				self.platforms.append(each.title()) # Append to self.platforms list for easy generation of button widget.

		# Make buttons for each platform.
		for each in self.platforms:
			self.buttonsDic.setdefault(each, tk.Button(self.topFrame, text=each, bg=buttonColor, fg='black', font=('Helvetica',14,'bold'), 
														command=lambda x=each: self.get_password(x)))
			self.buttonsDic[each].place(rely=self.mButtonPos, relx=.25, relheight=.075, relwidth=.5)
			self.mButtonPos += .1

	# Get password for platform. 
	def get_password(self, event):

		with shelve.open('platform') as file:
			pyperclip.copy(file[event.lower()]['pass'])
			tempString = file[event.lower()]['user']
			self.var1.set(f'Your password for {tempString} on {event} has been copied to clipboard!')

	# Status bar for button press.
	def mid_frame(self):
		self.var1 = tk.StringVar()
		self.midFrame = tk.Frame(self, bg='white')
		self.sample = tk.Label(self.midFrame, textvariable=self.var1, bg='white', font=(None,12))

		self.midFrame.place(rely=.7, relheight=.1, relwidth=1)
		self.sample.pack(fill=tk.BOTH, expand=True)

	# Menu buttons for navigation. 
	def bot_frame(self):
		self.botFrame = tk.Frame(self, bg='white')
		self.buttonCreate = tk.Button(self.botFrame, text='New Platform', font=('Helvetica',20,'bold'), command=self.create_call, bg=buttonColor, fg='black')
		self.buttonDelete = tk.Button(self.botFrame, text='Remove Platform', font=('Helvetica',20,'bold'), command=self.w_delete_call, bg=buttonColor, fg='black')
		self.buttonBack = tk.Button(self.botFrame, text='Back', font=('Helvetica',20,'bold'), command=self.back_call, bg=buttonColor, fg='black')

		self.botFrame.place(rely=.8, relheight=.2, relwidth=1)
		self.buttonCreate.place(rely=0, relx=0, relwidth=.5, relheight=.5)
		self.buttonDelete.place(rely=0, relx=.5, relwidth=.5, relheight=.5)
		self.buttonBack.place(rely=.5, relx=0, relwidth=1, relheight=.5)
	# Create new window that has inputs to store new platforms and accounts.
	def create_call(self):
		self.destroy()
		CreateWindow(root)

	# Create window for deleting current platforms and accounts.	
	def w_delete_call(self):
		self.destroy()
		DeleteWindow(root)

	# Go back to main window. 
	def back_call(self):
		self.destroy()
		App(root)

# New window for registering new platforms and accounts. 
class CreateWindow(tk.Frame):

	def __init__(self, master):
		super().__init__(master)
		self.master = master

		self.c_frame_config()
		self.c_frame_top()
		self.c_frame_bot()

		self.pack(fill=tk.BOTH, expand=True)

	def c_frame_config(self):
		self['bg'] = 'white'

	def c_frame_top(self):
		self.platformLabel = tk.Label(self, text='Platform', font=(None,20))
		self.userLabel = tk.Label(self, text='Username', font=(None,20))
		self.passLabel = tk.Label(self, text='Password', font=(None,20))
		self.platformName = tk.Entry(self)
		self.username = tk.Entry(self)
		self.password = tk.Entry(self)
		self.statusVar = tk.StringVar()
		self.statusLabel = tk.Label(self, textvariable=self.statusVar, font=(None,20))

		self.platformLabel.place(relx=0, rely=0, relwidth=.5, relheight=.1)
		self.userLabel.place(relx=0, rely=.1, relwidth=.5, relheight=.1)
		self.passLabel.place(relx=0, rely=.2, relwidth=.5, relheight=.1)
		self.platformName.place(relx=.5, rely=0, relwidth=.5, relheight=.1)
		self.username.place(relx=.5, rely=.1, relwidth=.5, relheight=.1)
		self.password.place(relx=.5, rely=.2, relwidth=.5, relheight=.1)
		self.statusLabel.place(rely=.7, relwidth=1, relheight=.1)

	def c_frame_bot(self):
		self.registerButton = tk.Button(self, text='Register Platform', font=('Helvetica',20,'bold'), bg=buttonColor, fg='black', command=self.register_platform)
		self.backButton = tk.Button(self, text='Back', font=('Helvetica',20,'bold'), bg=buttonColor, fg='black', command=self.back_call)

		self.registerButton.place(rely=.8, relwidth=1, relheight=.1)
		self.backButton.place(rely=.9, relwidth=1, relheight=.1)

	def register_platform(self):

		with shelve.open('platform') as file:
			file[self.platformName.get().lower()] = {'user':self.username.get(), 'pass':self.password.get()}

		self.statusVar.set('Successfully registered!')
		self.statusLabel['fg'] = 'lime'

	def back_call(self):
		self.destroy()
		MainWindow(root)

# New window to delete existing platforms and accounts. 
class DeleteWindow(tk.Frame):
	def __init__(self,master):
		super().__init__(master)
		self.master = master 

		self.d_window_config()
		self.d_frame_top()
		self.d_frame_bot()

		self.pack(fill=tk.BOTH, expand=True)

	def d_window_config(self):
		self['bg'] = 'black'

	def d_frame_top(self):
		self.dButtonDic = {}
		buttonPos = 0.05
		self.frameTop = tk.Frame(self)

		with shelve.open('platform') as file:
			for key in file:
				self.dButtonDic.setdefault(key, tk.Button(self.frameTop, text=key.title(), bg=buttonColor, fg='black', font=('Helvetica',14,'bold'),
													 command=lambda each=key:self.select_platform(each)))

		for key in self.dButtonDic.keys():
			self.dButtonDic[key].place(rely=buttonPos , relx=.25, relheight=.05, relwidth=.5)
			buttonPos += .075

		self.frameTop.place(rely=0, relheight=.8, relwidth=1)


	def d_frame_bot(self):
		self.frameBot = tk.Frame(self)
		self.deleteButton = tk.Button(self.frameBot, text='Remove Platform', bg=buttonColor, fg='black', font=('Helvetica',20,'bold'), command=self.delete_call) 
		self.backButton =  tk.Button(self.frameBot, text='Back', bg=buttonColor, fg='black', font=('Helvetica',20,'bold'), command=self.back_call)

		self.frameBot.place(rely=.8, relheight=.2, relwidth=1)
		self.deleteButton.pack(fill=tk.BOTH, expand=True)
		self.backButton.pack(fill=tk.BOTH, expand=True)

	def select_platform(self, event):
		if self.dButtonDic[event]['relief'] != 'sunken':
			self.dButtonDic[event]['relief']= 'sunken'
			self.dButtonDic[event]['bg'] = 'white'
		else:
			self.dButtonDic[event]['relief']= 'flat'
			self.dButtonDic[event]['bg'] = buttonColor

	def delete_call(self):
		for each in self.dButtonDic.keys():
			if self.dButtonDic[each]['relief'] == 'sunken':
				with shelve.open('platform') as file:
					del file[each]

		self.destroy()
		DeleteWindow(root)

	def back_call(self):
		self.destroy()
		MainWindow(root)

# Run our app.
if __name__ == '__main__':
	root = tk.Tk()
	root.title('Pass Volt')
	root.geometry('600x500')
	root.config(bg='black')
	App(root)
	root.mainloop()
