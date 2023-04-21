from tkinter import Tk, ttk, Entry, Button, Label, filedialog, messagebox, END, scrolledtext, DISABLED, NORMAL
from psutil import disk_partitions
from os import remove, walk
from json import loads
from threading import Thread
from webbrowser import open_new_tab

class UI:
	def __init__(self):
		self.search_running = False


	def run(self):
		self.config = self.load_config()
		self.window = Tk()
		self.window.title(self.config.get("MainTitle", "ERROR⚠"))
		self.window.geometry(self.config.get("Geometry", None ))
		self.window.resizable(False, False)
		self.window.iconbitmap(self.config.get("MainIconPath", None))
		self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.s = ttk.Style()
		self.s.theme_use('default')
		self.s.configure("TNotebook", background='grey')
		self.s.configure("TNotebook.Tab", background='#adb5bd')
		self.tabs = ttk.Notebook(self.window)

		self.main_tab = ttk.Frame(self.tabs)
		self.search_tab = ttk.Frame(self.tabs) 
		self.delete_tab = ttk.Frame(self.tabs)

		self.tabs.add(self.main_tab, text='Main')
		self.tabs.add(self.search_tab, text='Search File')
		self.tabs.add(self.delete_tab, text='Delete File')
		self.tabs.pack(expand=1, fill='both')


		self.add_objects_tab1()
		self.add_objects_tab2()	
		self.add_objects_tab3()

		self.window.mainloop()

	def on_closing(self):
		self.search_running = False
		self.window.destroy()


	def load_config(self, file_path: str = "static/config.json"):
		with open(file_path, "r") as file:
			return loads(file.read())

	def delete_file(self, file_path: str):
		try:
			remove(file_path)
			self.delete_path.delete(0, END)
			messagebox.showinfo("Successfully✅", "Ok.")
		except Exception as e:
			messagebox.showerror("error⚠", e)

	def get_path(self):
		self.delete_path.delete(0, END)
		self.delete_path.insert(0, filedialog.askopenfilename())


	def add_objects_tab1(self):
		self.author = Label(self.main_tab, text="Made By Xsarz")
		self.beta = Label(self.main_tab, text="BETA 1.0")
		self.btn =  Button(self.main_tab, text="CONTACTS", command=lambda: open_new_tab("https://linktr.ee/xsarz"))
		self.author.pack(anchor ="n", pady=(50,70))
		self.btn.pack(anchor ="center", pady=(5,0))
		self.beta.pack(anchor ="s", pady=(130,0))


	def add_objects_tab3(self):
		self.delete_path = Entry(self.delete_tab, width=75) 
		self.delete_button = Button(self.delete_tab, text="Delete", command=lambda: self.delete_file(file_path=self.delete_path.get()), height = 3, width = 15, font='30', bg="red")
		self.delete_txt = Label(self.delete_tab, text="Enter file path") 
		self.delete_txt2 = Label(self.delete_tab, text="Or choose a file")
		self.choose_file_button = Button(self.delete_tab, text="Choose", command=lambda: self.get_path())

		self.delete_txt.pack(anchor ="n")
		self.delete_path.pack(anchor ="n")
		self.delete_txt2.pack(anchor ="n")
		self.choose_file_button.pack(anchor ="n")
		self.delete_button.pack(expand=True)


	def add_objects_tab2(self):
		self.txt_paths = scrolledtext.ScrolledText(self.search_tab, width=50, height=10)
		self.txt_paths.configure(state=DISABLED)

		self.search_clear_button = Button(self.search_tab, text="Clear", command=lambda: self.clear_paths(), bg="red")
		self.search_start_button = Button(self.search_tab, text="Search File", command=lambda: self.search_start())
		self.search_stop_button = Button(self.search_tab, text="Stop", command=lambda: self.search_stop())

		self.file_name = Entry(self.search_tab, width=20)
		self.file_name_lbl = Label(self.search_tab, text="Enter file to search")


		self.discs = ttk.Combobox(self.search_tab, state="readonly")
		d = [disc[1].replace(":\\", '') for disc in disk_partitions()]
		d.append("All disks")
		self.discs['values'] = tuple(d)
		self.discs.current(len(self.discs['values'])-1)

		self.file_name_lbl.pack(anchor ="n", pady=(5,0))
		self.file_name.pack(anchor ="n", pady=(5,5))
		self.txt_paths.pack(anchor ="n")
		self.discs.pack(anchor ="n", pady=(5,0))
		self.search_start_button.pack(anchor ="n", pady=(5,0))
		self.search_stop_button.pack(anchor ="n", pady=(5,0))
		self.search_clear_button.pack(anchor ="n", pady=(5,0))


	def write_path(self, text: str):
		self.txt_paths.configure(state=NORMAL)
		self.txt_paths.insert(END, text)
		self.txt_paths.configure(state=DISABLED)

	def clear_paths(self):
		self.txt_paths.configure(state=NORMAL)
		self.txt_paths.delete('1.0', END)
		self.txt_paths.configure(state=DISABLED)

	def search_start(self):
		if self.search_running:
			pass
		elif self.file_name.get() == "":
			messagebox.showerror("⚠", "You didn't provide a filename.")
		else:
			self.search_running = True
			selected_disc = self.discs.get()
			Thread(target=self.search, args=(self.file_name.get(), [disc[1].replace(":\\", '') for disc in disk_partitions()] if selected_disc == "All disks" else [selected_disc])).start()



	def search_stop(self):
		if self.search_running:
			self.search_running = False
			messagebox.showinfo("✅", "OK.")
			return
		messagebox.showerror("⚠", "Process not running.")


	def search(self, file_name: str, discs: list):
		total_files = list()
		for disc in discs:
			if self.search_running is False:
				exit(0)
			for adress, dirs, files in walk(f'{disc}:\\'):
				for file in files:
					if self.search_running is False:
						exit(0)
					elif file_name.lower() in file.lower():
						total_files.append(f"{adress}\\{file}")
						self.write_path(f"\n{adress}\\{file}\n")
		self.search_running = False
		messagebox.showinfo("Successfully✅", f"Process completed. Found {len(total_files)} similar files.")


if __name__ == "__main__":
	prog = UI()
	prog.run()