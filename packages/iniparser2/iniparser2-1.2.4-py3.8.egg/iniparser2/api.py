class INI:
	def __init__(self, filename, section=None, pass_section=True, trace=False, trace_verbose=1):
		'''
			Parameters:
				- filename:
					the name of file to be parsed
				- section:
					the section of the properties
				- pass_section:
					pass section
				- trace:
					print trace messages
				- trace_verbose:
					trace verbosity level
		'''
		self.filename = filename
		self.section = section
		self.pass_section = pass_section
		self.trace = trace
		self.trace_verbose = trace_verbose
		if self.section != None:
			self.pass_section = False
		if self.pass_section == False and self.section == None:
			from .err import SectionError
			raise SectionError('`section` cannot be \'NoneType\' if `pass_section` is \'False\'')
		if self.trace == True:
			from .err import TraceError
			if self.trace_verbose < 1:
				raise TraceError('`trace_verbose` cannot be lower than 1 if `trace` is True')
			elif self.trace_verbose > 2:
				raise TraceError('`trace_verbose` cannot be higher than 2')
		elif self.trace == False and trace_verbose > 0:
			self.trace_verbose=0
		if self.section != None: self.section = str(section)

	def delete_gap(self):
		lines,spc_ctr=list(),-1
		with open(self.filename,'r') as f:
			lines,spc_ctr,spcb_ctr=f.readlines(),-1,0
			for l in lines: # get spaces by line
				spc_ctr += 1
				if l.strip() == '':
					if self.trace_verbose == 2: print(f'[iniparser2][TRACE]: found gap at line: {spc_ctr}')
					lines[spc_ctr] = ''
		with open(self.filename,'w+') as f:
			for l in lines:
				f.write(l)

	def get(self):
		"""get all keys and value by section"""
		ret = dict()
		found=False
		if not self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:False')
			with open(self.filename,'r') as f:
				lines,ctr,point,anchor= f.readlines(),-1,0,0
				for l in lines: # get point
					ctr += 1
					if not l.strip().startswith('#') and len(l.strip().split('[',1)) == 2:
						if l.strip().split('[',1)[1].split(']',1)[0] == self.section:
							point,anchor,found = ctr+1,ctr+1,True
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: Found `point` at line: {point}')
							break
				if point == 0 and self.trace_verbose == 1: print(f'[iniparser2][TRACE]: `point` found at line: {point} (DEFAULT)')
				for i in range(point,len(lines)): # get anchor
					anchor += 1
					if not lines[i].strip().startswith('#') and len(lines[i].strip().split('[',1)) == 2:
						if lines[i].strip().split('[',1)[1].split(']',1)[0]:
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: Found `anchor` at line: {anchor}')
							break
				for i in range(point,anchor): # get key and value
					if lines[i].strip().startswith('[') or lines[i].strip().startswith('#'): continue
					else:
						if not lines[i].strip().startswith('#') and len(lines[i].strip().split('=',1)) == 2:
							if self.trace_verbose == 2: print(f'[iniparser2][TRACE]: Found property at line: {i}')
							ret.update({lines[i].strip().split('=',1)[0]: lines[i].strip().split('=',1)[1].split('#')[0]})
			if found: return ret
		elif self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:True')
			with open(self.filename,'r') as f:
				lines,ctr,point,anchor,found,key= f.readlines(),-1,0,0,False,None
				for l in lines: # get key and value
					ctr += 1
					if l.strip().startswith('[') or found==True:
						found=True
						if not l.strip().startswith('#') and len(l.strip().split('[',1)) == 2:
							if l.strip().split('[',1)[1].split(']',1)[0]:
								key = l.strip().split('[',1)[1].split(']',1)[0]
								point,anchor,found = ctr+1,ctr+1,True
								if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: Found `point` at line: {point}')
								for i in range(point,len(lines)): # get anchor
									anchor += 1
									if not lines[i].strip().startswith('#') and len(lines[i].strip().split('[',1)) == 2:
										if lines[i].strip().split('[',1)[1].split(']',1)[0]:
											if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: Found `anchor` at line: {anchor}')
											break
								for i in range(point,anchor): # get key and value
									if not lines[i].strip().startswith('#') and len(lines[i].strip().split('=',1)) == 2:
										if self.trace_verbose == 2: print(f'[iniparser2][TRACE]: Found property at line: {i}')
										if not key in ret:
											ret.update({key:{}})
											ret[key].update({lines[i].strip().split('=',1)[0]: lines[i].strip().split('=',1)[1].split('#',1)[0]})
										else:
											ret[key].update({lines[i].strip().split('=',1)[0]: lines[i].strip().split('=',1)[1].split('#',1)[0]})
					if found == False:
						if not l.strip().startswith('#') and len(l.strip().split('=',1)) == 2:
							if self.trace_verbose == 2: print(f'[iniparser2][TRACE]: Found property at line: {ctr}')
							ret.update({l.strip().split('=',1)[0]: l.strip().split('=',1)[1].split('#')[0]})
			return ret

	def set_section(self):
		"""set section"""
		if not self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:False')
			with open(self.filename,'r') as f:
				lines,found= f.readlines(),False
				for l in lines: # get point
					if not l.strip().startswith('#') and len(l.strip().split('[',1)) == 2:
						if l.strip().split('[',1)[1].split(']',1)[0] == self.section:
							found = True
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: Couldn\'t set section for `{self.section}`, section already exists!')
							return False
			if not found:
				lines=list()
				with open(self.filename,'r') as f:
					lines=f.readlines()
				with open(self.filename,'a+') as f:
					if len(lines) > 0:
						f.write(f'\n[{self.section}]\r')
					else: f.write(f'\n[{self.section}]\r')
					INI(self.filename,self.section).delete_gap()
					return True
		elif self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: Couldn\'t set section, pass_section:True')

	def unset_section(self):
		"""unset section, the existing keys inside the section will get removed"""
		if not self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:False')
			if INI(self.filename,self.section).isset_section():
				ctr = -1
				for k in INI(self.filename,self.section).get(): # clear keys inside the section
					ctr += 1
					if self.trace_verbose == 2: print(f'[iniparser2][TRACE]: Unset property of section {self.section}: {k} line({ctr})')
					INI(self.filename,self.section).unset(k)
				lines,ctr,found= list(),-1,False
				with open(self.filename,'r') as f:
					lines=f.readlines()
					for l in lines: # get point
						ctr += 1
						if not l.strip().startswith('#') and len(l.strip().split('[',1)) == 2:
							if l.strip().split('[',1)[1].split(']',1)[0] == self.section:
								found = True
								if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: section found at line: {ctr}')
								break
				del lines[ctr] # delete section
				with open(self.filename,'w+') as f:
					for l in lines:
						f.write(l)
				INI(self.filename,self.section).delete_gap()
				return found
		elif self.pass_section: 
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: Couldn\'t unset section, pass_section:True')
			

	def isset_section(self):
		"""check if section was set or not"""
		if not self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:False')
			with open(self.filename,'r') as f:
				lines,found,ctr= f.readlines(),False,-1
				for l in lines: # get point
					if not l.strip().startswith('#') and len(l.strip().split('[',1)) == 2:
						if l.strip().split('[',1)[1].split(']',1)[0] == self.section:
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: section found at line: {ctr}')
							found = True
				return found
		elif self.pass_section: 
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: Couldn\'t check section, pass_section:True')

	def set(self,key,value):
		"""
			set new key or update existing key

			Parameters:
				- key:
					key of the property
				- value:
					value of the property
		"""
		if self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:True')
			lines,ctr,found=list(),-1,False
			with open(self.filename,'r') as f:
				lines=f.readlines()
				for l in lines:
					ctr += 1
					if not l.strip().startswith('#') and len(l.strip().split('=',1)) == 2:
						if l.strip().split('=',1)[0] == key:
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: an existing property found at line: {ctr}')
							found = True
							break
			if found: # update existing key's value
				if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: found an existing property, update property value at line: {ctr}')
				lines[ctr] = f"{key}={value}\r"
				with open(self.filename,'w+') as f:
					for l in lines:
						f.write(l)
					return True
			elif not found: # new key
				if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: property not found, set new key at line: 0')
				lines.insert(0,f"{key}={value}\r")
				with open(self.filename,'w+') as f:
					for l in lines:
						f.write(l)
					return True
		elif not self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:False')
			lines,section_point,found=list(),0,False
			with open(self.filename,'r') as f:
				lines,ctr,point,anchor,found,section_point= f.readlines(),-1,0,0,False,0
				for l in lines: # get point
					ctr += 1
					if not l.strip().startswith('#') and len(l.strip().split('[',1)) == 2:
						if l.strip().split('[',1)[1].split(']',1)[0] == self.section:
							point,anchor,section_point= ctr+1,ctr+1,ctr
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: found section point at line: {ctr}')
							break
				for i in range(point,len(lines)): # get anchor
					anchor += 1
					if not lines[i].strip().startswith('#') and len(lines[i].strip().split('[',1)) == 2:
						if lines[i].strip().split('[',1)[1].split(']',1)[0]:
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: found section anchor at line: {anchor}')
							break
				for i in range(point,anchor): # get section pointer
					section_point += 1
					if not (lines[i].strip().startswith('[') or lines[i].strip().startswith('#')) and len(lines[i].strip().split('=',1)) == 2:
						if lines[i].strip().split('=',1)[0] == key:
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: found property at line: {i}')
							found = True
							break
			if found:
				if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: found an existing property, update property value at line: {section_point}')
				try:
					lines[section_point] = f"{key}={value}{lines[section_point].strip().split('#',1)[1]}\r"
				except: 
					lines[section_point] = f"{key}={value}\r"
				with open(self.filename,'w+') as f:
					for l in lines:
						f.write(l)
					return True
			elif not found:
				if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: property not found, set new property at line: {section_point+1}')
				lines.insert(section_point+1,f"{key}={value}\r")
				with open(self.filename,'w+') as f:
					for l in lines:
						f.write(l)
					return True

	def isset(self,key):
		"""
			check if key was set or not
			
			Parameters:
				- key:
					key of the property
		"""
		if self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:True')
			found=False
			with open(self.filename,'r') as f:
				lines=f.readlines()
				for l in lines:
					if not l.strip().startswith('#') and len(l.strip().split('=',1)) == 2:
						if l.strip().split('=',1)[0] == key:
							found = True
							break
			return found
		elif not self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:False')
			found=False
			with open(self.filename,'r') as f:
				lines,ctr,point,anchor,found= f.readlines(),-1,0,0,False
				for l in lines: # get point
					ctr += 1
					if not l.strip().startswith('#') and len(l.strip().split('[',1)) == 2:
						if l.strip().split('[',1)[1].split(']',1)[0] == self.section:
							point,anchor= ctr+1,ctr+1
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: section point found at line: {point}')
							break
				for i in range(point,len(lines)): # get anchor
					anchor += 1
					if not l.strip().startswith('#') and len(lines[i].strip().split('[',1)) == 2:
						if lines[i].strip().split('[',1)[1].split(']',1)[0]:
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: section anchor found at line: {anchor}')
							break
				for i in range(point,anchor): # get section pointer
					if not (lines[i].strip().startswith('#') or lines[i].strip().startswith('[')) and len(lines[i].strip().split('=',1)) == 2:
						if lines[i].strip().split('=',1)[0] == key:
							found = True
							break
			return found

	def unset(self,key):
		"""
			unset existing key

			Parameters:
				- key:
					key of the property
		"""
		if self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:True')
			lines,ctr,found=list(),-1,False
			with open(self.filename,'r') as f:
				lines=f.readlines()
				for l in lines:
					ctr += 1
					if not l.strip().startswith('#') and len(l.strip().split('=',1)) == 2:
						if l.strip().split('=',1)[0] == key:
							found = True
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: found property at line: {ctr}')
							break
			if found: # update existing key's value
				del lines[ctr]
				with open(self.filename,'w+') as f:
					for l in lines:
						f.write(l)
					INI(self.filename,self.section).delete_gap()
					return True

		elif not self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:False')
			lines,section_point,found=list(),0,False
			with open(self.filename,'r') as f:
				lines,ctr,point,anchor,found,section_point= f.readlines(),-1,0,0,False,0
				for l in lines: # get point
					ctr += 1
					if not l.strip().startswith('#') and len(l.strip().split('[',1)) == 2:
						if l.strip().split('[',1)[1].split(']',1)[0] == self.section:
							point,anchor,section_point= ctr+1,ctr+1,ctr
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: section point found at line: {point}')
							break
				for i in range(point,len(lines)): # get anchor
					anchor += 1
					if len(lines[i].strip().split('[',1)) == 2:
						if lines[i].strip().split('[',1)[1].split(']',1)[0]:
							if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: section anchor found at line: {anchor}')
							break
				for i in range(point,anchor): # get section pointer
					section_point += 1
					if not (lines[i].strip().startswith('[') or lines[i].strip().startswith('[')) and len(lines[i].strip().split('=',1)) == 2:
						if lines[i].strip().split('=',1)[0] == key:
							found = True
							break
			if found:
				del lines[section_point]
				with open(self.filename,'w+') as f:
					for l in lines:
						f.write(l)
					INI(self.filename,self.section).delete_gap()
					return True

	# utils

	def exists(self):
		"""check whether the file is exists or not"""
		import os
		if os.path.exists(self.filename): return True
		else: return False

	def create(self):
		"""creates new file"""
		import os
		if not os.path.exists(self.filename):
			with open(self.filename,'x') as f:
				pass
			return True
		else: return False

	def flush(self,stream=False):
		"""
			flush file
			
			Parameters:
				- stream:
					flush mode
		"""
		if not stream:
			import os
			if os.path.exists(self.filename):
				os.remove(self.filename)
				with open(self.filename,'x') as f:
					pass
				return True
			else: return False
		elif stream:
			with open(self.filename,'w') as f:
				f.write('')
			return True

	def remove(self):
		"""remove/deletes file"""
		import os
		if os.path.exists(self.filename):
			os.remove(self.filename)
			return True
		else: return False

class INI_TEMP:
	"""temporary parse method"""
	def __init__(self, section=None, pass_section=True, trace=False, trace_verbose=1):
		self.section = section
		self.pass_section = pass_section
		self.trace = trace
		self.trace_verbose = trace_verbose
		if self.section != None:
			self.pass_section = False
		if self.pass_section == False and self.section == None:
			from .err import SectionError
			raise SectionError('`section` cannot be \'NoneType\' if `pass_section` is \'False\'')
		if self.trace == True:
			from .err import TraceError
			if self.trace_verbose < 1:
				raise TraceError('`trace_verbose` cannot be lower than 1 if `trace` is True')
			elif self.trace_verbose > 2:
				raise TraceError('`trace_verbose` cannot be higher than 2')
		elif self.trace == False and trace_verbose > 0:
			self.trace_verbose=0
		if self.section != None: self.section = str(section)

	def parse(self,string):
		import random
		char = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m',
				'Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M',
				'1','2','3','4','5','6','7','8','9','0']
		ret_char = list()
		for i in range(8):
			ret_char.append(random.choice(char))
		token = ''.join(ret_char)
		fname = f"{token}.ini.temp"
		x = INI(fname,self.section,self.pass_section,self.trace,self.trace_verbose)
		x.create()
		with open(fname,'w') as f:
			f.write(string)
		data = x.get()
		x.remove()
		return data