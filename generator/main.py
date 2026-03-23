from builder import generateHome, generatePosts
from shutil import copytree, rmtree
from os import rmdir, makedirs

rmtree("build")
makedirs("build/posts")

generateHome()
generatePosts()

copytree("public", "build/public")

