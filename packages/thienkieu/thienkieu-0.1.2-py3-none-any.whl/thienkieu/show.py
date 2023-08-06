from pyfiglet import Figlet 

def thienkieutest(name=""):
	text = f"hello - {name}"
	f = Figlet("isometric2")
	print(f.renderText(text))
	print("new version 0.0.2")

if __name__ == '__main__':
	thienkieutest("test")
