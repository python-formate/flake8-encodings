example_source = """

import builtins, io, pathlib
import configparser

source = open("source.py")


def foo():

	result = builtins.open("source.py")
	result = io.open("source.py")
	result = open("source.py", encoding=None)


class F:

	def foo():
		result = open("source.py", encoding="utf-8")
		result = open("source.py", mode="rb")

	def read(mode: str = "r"):
		result = open("source.py", mode=mode)

class G:
	def bar():
		cfg = configparser.ConfigParser()
		cfg.read("tox.ini")

	def baz():
		from configparser import ConfigParser
		cfg = ConfigParser()
		cfg.read("tox.ini", encoding=None)
		cfg.read_dict({})

def paths_open():
	pathlib.Path("foo.txt").open()
	pathlib.Path("LICENSE").open(encoding=None)
	pathlib.Path("README.md").open(encoding="UTF-8")
	pathlib.Path("README.md").as_posix()

	pathlib.WindowsPath("foo.txt").open()
	pathlib.PosixPath("LICENSE").open(encoding=None)
	pathlib.WindowsPath("README.md").open(encoding="UTF-8")
	pathlib.PosixPath("README.md").as_posix()

	with pathlib.Path("foo.txt").open("w") as fp:
		fp.write("Hello World")

def paths_read_text():
	pathlib.Path("foo.txt").read_text()
	pathlib.Path("LICENSE").read_text(encoding=None)
	pathlib.Path("README.md").read_text(encoding="UTF-8")
	pathlib.Path("README.md").as_posix()

	print(pathlib.WindowsPath("foo.txt").read_text())
	pathlib.PosixPath("LICENSE").read_text(encoding=None)
	pathlib.WindowsPath("README.md").read_text(encoding="UTF-8")
	pathlib.PosixPath("README.md").as_posix()

def paths_write_text():
	pathlib.Path("foo.txt").write_text()
	pathlib.Path("LICENSE").write_text(encoding=None)
	pathlib.Path("README.md").write_text(encoding="UTF-8")
	pathlib.Path("README.md").as_posix()

	pathlib.WindowsPath("foo.txt").write_text()
	pathlib.PosixPath("LICENSE").write_text(encoding=None)
	pathlib.WindowsPath("README.md").write_text(encoding="locale")
	pathlib.PosixPath("README.md").as_posix()

def paths_assigned():
	pyproject_file = pathlib.Path("pyproject.toml")

	if pyproject_file.is_file():
		pyproject_file.read_text()
	else:
		pyproject_file.write_text("foo", encoding="UTF-8")

def paths_open_binary():
	with pathlib.Path("foo.txt").open("wb", encoding="UTF-8") as fp:
		fp.write(b"Hello World")
"""
