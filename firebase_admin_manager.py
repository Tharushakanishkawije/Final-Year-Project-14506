import subprocess

# try to import firebase_admin
try:
	import firebase_admin
	print("Package: firebase_admin is already installed.")
except ImportError:
	print("Package: firebase_admin not found. Installing...")
	try:
		subprocess.check_call(["pip", "install", "firebase-admin"])
		print("Package: firebase_admin installed successfully.")
	except subprocess.CalledProcessError:
		print("Failed to install firebase_admin package. Please install it manually.")
