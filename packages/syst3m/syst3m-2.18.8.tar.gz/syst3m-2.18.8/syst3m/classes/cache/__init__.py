#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *

# the cache object class.
class Cache(Object):
	def __init__(self, path=None):
		if path == None: path = f"{HOME}/.cache/"
		if not Files.exists(path): Files.create(path, directory=True)
		Object.__init__(self)
		self.assign({
			"path":path,
		})
		self.fp = self.file_path = FilePath(self.path)
	def set(self, data=None, group=None, id=None, format="str"):
		if id == None:
			data_path = gfp.clean(f"{self.path}/{group}")
		else:
			data_path = gfp.clean(f"{self.path}/{group}/"+id)#.replace("/", "\\")
		base = FilePath(data_path).base()
		if not gfp.exists(base): os.system(f"mkdir -p {base}")
		if format in [str, "str", "string", int, float, "int", "integer", "float", "double"]:
			Files.save(data_path, str(data), format="str")
		elif format in [dict, list, "dict", "dictionary", "list", "array", "json"]:
			Files.save(data_path, str(data), format="json")
		else:
			raise ValueError(f"Unkown format: {format}.")
		return None
	def get(self, group=None, id=None, format="str", default=None):
		if id == None:
			data_path = gfp.clean(f"{self.path}/{group}")
		else:
			data_path = gfp.clean(f"{self.path}/{group}/"+id)#.replace("/", "\\")
		base = FilePath(data_path).base()
		if not gfp.exists(base): os.system(f"mkdir -p {base}")
		def load():
			if format in [str, "str", "string"]:
				return Files.load(data_path, format="str")
			elif format in [int, "int", "integer"]:
				return int(Files.load(data_path, format="str"))
			elif format in [float, "float", "double"]:
				return float(Files.load(data_path, format="str"))
			elif format in [dict, list, "dict", "dictionary", "list", "array", "json"]:
				return Files.load(data_path, format="json")
			else:
				raise ValueError(f"Unkown format: {format}.")
		try:
			loaded = load()
		except FileNotFoundError:
			self.set(id=id, data=str(default), group=group, format=format)
			loaded = load()
		if loaded in ["None","none","null"]: loaded = None
		return loaded
	def delete(self, group=None, id=None, forced=False, sudo=False):
		if id == None:
			data_path = gfp.clean(f"{self.path}/{group}")
		else:
			data_path = gfp.clean(f"{self.path}/{group}/"+id)#.replace("/", "\\")
		Files.delete(path=data_path, sudo=sudo, forced=forced)
		return None


# the default cache.
cache = Cache()

# the webserver cache object class.
class WebServer(objects.Thread):
	def __init__(self,
		id="webserver",
		host="127.0.0.1",
		port=52379,
		path=None, # only used for tokens, rest is stored in python memory only.
		default={},
		# do not use.
		serialized={},
	):
		objects.Thread.__init__(self)
		self.__cache__ = Cache(path=path) # only used for tokens, rest is stored in python memory only.
		self.default = dict(default)
		self.assign({
			"sleeptime":3,
			"id":id,
			"host":host,
			"port":port,
			"cache":default,
		})
		self.assign(serialized, keys=["sleeptime", "id", "host", "port", "cache"], safe=True)
		self.id = id.replace(" ","-")
		self.tag = self.id.replace(" ","_")
		try: self.log_level
		except: self.log_level = 0
	# cache functions.
	def set(self, group=None, id=None, data=None, timeout=3):
		encoded = urllib.parse.urlencode({
			"group":group.replace(" ","_"),
			"id":id.replace(" ","_"),
			"data":data,
			"token":self.token,
			"cache":self.__cache__.path,
			"cache_id":self.id,
		})
		try:
			response = requests.get(f'http://{self.host}:{self.port}/set?{encoded}', timeout=timeout)
		except Exception as e:
			return Response.error(f"Failed to connect with {self.host}:{self.port}, error: {e}")
		try:
			response = self.__serialize__(response.json())
		except:
			return Response.error(f"Failed to serialize {response}: {response.text}")
		return Response.response(response)
	def get(self, group=None, id=None, timeout=3):
		encoded = urllib.parse.urlencode({
			"group":group.replace(" ","_"),
			"id":id.replace(" ","_"),
			"token":self.token,
			"cache":self.__cache__.path,
			"cache_id":self.id,
		})
		try:
			response = requests.get(f'http://{self.host}:{self.port}/get?{encoded}', timeout=timeout)
		except Exception as e:
			return Response.error(f"Failed to connect with {self.host}:{self.port}, error: {e}")
		try:
			response = self.__serialize__(response.json())
		except:
			return Response.error(f"Failed to serialize {response}: {response.text}")
		return Response.response(response,)
	# flask app.
	def app(self):
		app = flask.Flask(__name__)
		cli = sys.modules['flask.cli']
		cli.show_server_banner = lambda *x: None
		@app.route('/get')
		def get():
			token = flask.request.args.get('token')
			if token != Cache(path=flask.request.args.get('cache')).get(flask.request.args.get('cache_id'), id="token"):
				return Response.error(f"Provided an invalid token {token}.").json()
			group = flask.request.args.get('group')
			id = flask.request.args.get('id')
			if id in ["none", "null", "None"]: id = None
			try:
				if id == None:
					tag = f"{group}"
					value = self.cache[group]
				else:
					tag = f"{group}:{id}"
					value = self.cache[group][id]
			except KeyError:
				return Response.error(f"There is no data cached for {tag}.").json()
			return Response.success(f"Successfully retrieved {tag}.", {
				"group":group,
				"id":id,
				"data":value,
			}).json()
		@app.route('/set')
		def set():
			token = flask.request.args.get('token')
			if token != Cache(path=flask.request.args.get('cache')).get(flask.request.args.get('cache_id'), id="token"):
				return Response.error(f"Provided an invalid token {token}.").json()
			group = flask.request.args.get('group')
			id = flask.request.args.get('id')
			if id in ["none", "null", "None"]: id = None
			value = flask.request.args.get('data')
			if id == None:
				tag = f"{group}"
				self.cache[group] = value
			else:
				tag = f"{group}:{id}"
				try: self.cache[group]
				except KeyError: self.cache[group] = {}
				self.cache[group][id] = value
			return Response.success(f"Successfully cached {tag}.").json()
		@app.route('/active')
		def active():
			token = flask.request.args.get('token')
			if token != Cache(path=flask.request.args.get('cache')).get(flask.request.args.get('cache_id'), id="token"):
				return Response.error(f"Provided an invalid token {token}.").json()
			return Response.success(f"Active.").json()
		#def run__(self, app, host, port):
		#	app.run(host=host, port=port)
		#self.process = multiprocessing.Process(target=app.run, args=(self, app, self.host,self.port,))
		#self.process.start()
		app.run(host=self.host, port=self.port)
	# control functions.
	def run(self):
		self.__cache__.set(group=self.id, id="daemon", data="*running*")
		self.__cache__.set(group=self.id, id="token", data=String().generate(length=64, digits=True, capitalize=True))
		self.app()
		self.__cache__.set(group=self.id, id="daemon", data="*stopped*")
	def fork(self, timeout=15, sleeptime=1):
		if self.running:
			return Response.error(f"The {self.id} is already running.")
		if self.log_level <= 0:
			print(f"Starting the {self.id}.")
		serialized = self.dict()
		serialized["path"] = self.__cache__.path
		for i in ["__cache__","cache","_stder", "_traceback_", "_name", "_daemonic", "_ident", "_native_id", "_tstate_lock", "_started", "_stderr", "_initialized", "_invoke_excepthook", "__status__", "__running__", "__response__", "_is_stopped", "_args", "_kwargs", "_target", "_raw_traceback_",]:
			try: del serialized[i]
			except: a=1
		serialized = f"{serialized}"
		command = [str(Defaults.vars.executable), f"{SOURCE_PATH}classes/cache/fork.py", "--serialized", f"'{serialized}'", "--syst3m-webserver-tag", self.tag]
		if self.log_level < 0:
			command += [ "2>", "/dev/null"]
		p = subprocess.Popen(command)
		success = False
		for i in range(int(timeout/sleeptime)):
			if self.running:
				success = True
				break
			time.sleep(sleeptime)
		if success:
			return Response.success(f"Successfully started the {self.id}.")
		else:
			return Response.error(f"The {self.id} is already running.")
	def stop(self):
		if not self.running: 
			return Response.error(f"{self.__traceback__(function='stop')}: The {self.id} is not running.")
		processes = Defaults.processes(includes=f"--syst3m-webserver-tag {self.tag}")
		if not processes.success: return response
		if len(processes.processes) <= 1:
			return Response.error(f"Unable to find the pid of the {self.id}.")
		for pid, info in processes.processes.items():
			if info["process"] not in ["grep"]:
				response = Defaults.kill(pid=pid)
				if not response.success: return response
		return Response.error(f"Successfully stopped the {self.id}.")
	# threading functions.
	def start_thread(self, thread, group="daemons", id=None):
		response = self.set(group=group, id=id, data=thread)
		if not response.success: return response
		response = thread.start()
		if response != None:
			try: success = bool(response["success"])
			except: success = True
			if not success: return response
		try:
			id = thread.id
		except:
			id = str(thread)
		return Response.success(f"Successfully started [{id}].")
	def get_thread(self, group="daemos", id=None):
		response = self.get(group=group, id=id)
		if not response.success: 
			if "There is no data cached for" in response.error:
				return Response.error(f"There is no thread cached for (group: {group}), (id: {id}).")
			else: return response
		thread = response.data
		return Response.success(f"Successfully retrieved thread [{thread}].", {
			"thread":thread,
		})
	# properties.
	@property
	def token(self):
		if random.randrange(1, 100) <= 5: 
			self.__cache__.set(group=self.id, id="token", data=String().generate(length=64, digits=True, capitalize=True))
		return self.__cache__.get(group=self.id, id="token")
	@property
	def running(self):
		return self.__running__()
	def __running__(self, timeout=3):
		encoded = urllib.parse.urlencode({
			"token":self.token,
			"cache":self.__cache__.path,
			"cache_id":self.id,
		})
		try:
			requests.get(f'http://{self.host}:{self.port}/active?{encoded}', timeout=timeout)
			return True
		except requests.exceptions.ConnectionError:
			return False
	# system functions.
	def __serialize__(self, dictionary, safe=False):
		if isinstance(dictionary, (Dictionary, dict)):
			new = {}
			for key, value in dictionary.items():
				if value in ["False", "false"]: new[key] = False
				elif value in ["True", "true"]: new[key] = True
				elif value in ["None", "none", "null", "nan"]: new[key] = None
				elif isinstance(value, (dict, Dictionary, list, Array)):
					new[key] = self.__serialize__(value, safe=safe)
				elif isinstance(value, object):
					if not safe:
						new[key] = value
				else:
					try: 
						int(value)
						new[key] = int(value)
					except: 
						new[key] = value
			return new
		if isinstance(dictionary, (Dictionary, dict)):
			new = []
			for value in dictionary:
				if value in ["False", "false"]: new.append(False)
				elif value in ["True", "true"]: new.append(True)
				elif value in ["None", "none", "null", "nan"]: new.append(None)
				elif isinstance(value, (dict, Dictionary)):
					new.append(self.__serialize__(value, safe=safe))
				elif isinstance(value, object):
					if not safe:
						new.append(value)
				else:
					try: 
						int(value)
						new.append(int(value))
					except: 
						new.append(value)
			return new
		else: raise ValueError(f"Parameter [dictionary] requires to be a [dict, Dictionary, list, Array], not [{dictionary.__class__.__name__}].")
	#def stop(self):
	#	self.process.terminate()
	#	self.process.join()
