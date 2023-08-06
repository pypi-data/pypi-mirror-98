import setuptools


list_lib = [
    "random",
    "math",
    "os",
    "sys",
    "time",
    "wget",
    "keyword",
    "zipfile",
    "pyttsx3",
    "getpass",
    "winsound",
    "pyqrcode",
    "pyfiglet",
    "jdatetime",
    "pyperclip",
    "webbrowser",
    "win10toast",
    "httplib",
    "yaml",
    "ctypes",
    "shutil",
    "tkinter",
    "pymsgbox",
    "platform",
    "wmi",
    "socket",
    "psutil",
    "turtle",
    "getpass",
    "platform",
    "wikipedia",
    "subprocess",
    "prettytable",
    
    "pylint",
    "pyinstaller",
]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name             = "mkg",
    version          = "0.0.13",
    author           = "mohamad.mk",
    description      = "The tools in this library are 100% free (Even for Americans and Saudis)",
    install_requires = list_lib,
    
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    python_requires = ">3.6",
)