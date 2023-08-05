#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import exceptions

# the database class.
class Database(Traceback):
	def __init__(self, firestore=None, path=None):
		
		# traceback.
		Traceback.__init__(self, traceback="w3bsite.Website.database")

		# checks.
		if firestore == None and path == None: raise exceptions.InvalidUsage(self.__traceback__()+" Both parameters firestore & path are None.")

		# attributes.
		self.mode = "firestore"
		self.firestore = firestore
		self.path = gfp.clean(path)
		self.file_path = self.fp = FilePath(self.path)
		if not self.fp.exists():
			Response.log(f"&ORANGE&Root permission&END& required to create database [{self.path}].")
			os.system(f"sudo mkdir {self.path}")
			Files.chmod(path=self.path, permission=700, sudo=True)
			Files.chown(path=self.path, owner=Defaults.vars.user, group=Defaults.vars.group, sudo=True)
		if firestore == None:
			self.mode = "cache"

		#

	# functions.
	def load(self, path=None):
		if path == None: return Response.error(self.__traceback__(function="load")+" Define parameter: [path].")
		if self.mode == "firestore":
			return self.firestore.load(path)
		elif self.mode == "cache":
			path = gfp.clean(f"{self.path}/{path}")
			try:
				data = Files.load(path=path, format="json")
			except Exception as e: return Response.error(str(e))
			return Response.success(f"Successfully loaded [{path}].", {
				"data":data,
			})
		else: raise exceptions.InvalidUsage(self.__traceback__(function="load")+f" Unknown mode [{self.mode}].")
	def save(self, path=None, data=None, overwrite=False):
		if path == None: return Response.error(self.__traceback__(function="save")+" Define parameter: [path].")
		if data == None: return Response.error(self.__traceback__(function="save")+" Define parameter: [data].")
		if self.mode == "firestore":
			return self.firestore.save(path, data)
		elif self.mode == "cache":
			path = gfp.clean(f"{self.path}/{path}")
			try:
				if not Files.exists(path=gfp.base(path)): Files.create(path=gfp.base(path), directory=True)
			except ValueError: a=1
			if not overwrite:
				def insert(old, new):
					for key,value in new.items():
						if isinstance(value, (dict, Dictionary)):
							if key in old:
								old[key] = insert(old[key], value)
							else:
								old[key] = value
						elif isinstance(value, (list, Array)):
							if key in old:
								for i in value:
									if i not in old[key]: old[key].append(i)
							else:
								old[key] = value
						else:
							old[key] = value
					return old
				try: old_data = Files.load(path=path, format="json")
				except: old_data = {}
				data = insert(old_data, data)
			try:
				Files.save(path=path, data=data, format="json")
			except Exception as e: return Response.error(str(e))
			return Response.success(f"Successfully saved [{path}].")
		else: raise exceptions.InvalidUsage(self.__traceback__(function="save")+f" Unknown mode [{self.mode}].")
	def delete(self, path=None, data=None):
		if path == None: return Response.error(self.__traceback__(function="delete")+" Define parameter: [path].")
		if self.mode == "firestore":
			return self.firestore.delete(path)
		elif self.mode == "cache":
			path = gfp.clean(f"{self.path}/{path}")
			try:
				Files.delete(path=path)
			except Exception as e: return Response.error(str(e))
			if Files.exists(path): return Response.error(f"Failed to delete [{path}].")
			return Response.success(f"Successfully deleted [{path}].")
		else: raise exceptions.InvalidUsage(self.__traceback__(function="delete")+f" Unknown mode [{self.mode}].")

	# join.
	def join(self, path):
		return gfp.clean(f"{self.path}/{path}")

	# get names.
	def names(self,
		# the sub path (leave None to use the root path)
		path=None,
	):

		# vars.
		names = []

		# firestore.
		if self.mode == "firestore":
			response = self.firestore.load_collection(path)
			raise ValueError(f"Still to check the response of load_collection (for names iteration): [{response}].")

		# cache.
		elif self.mode == "cache":
			for i in Directory(path=self.join(path)).paths(): names.append(gfp.name(i))

		# handler.
		return names

		#

	# representation.
	def __str__(self):
		return str(self.fp.path)
	def __repr__(self):
		return str(self)

	#

	
			