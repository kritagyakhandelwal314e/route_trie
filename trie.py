from enum import Enum
from typing import Set
from pprint import pprint
from json import load

class INVALID_ROUTE_EXCEPTION(Exception):
	pass

class HTTPMethod(Enum):
  GET = 'GET'
  POST = 'POST'
  PUT = 'PUT'
  PATCH = 'PATCH'
  DELETE = 'DELETE'
  HEAD = 'HEAD'
  CONNECT = 'CONNECT'
  OPTIONS = 'OPTIONS'
  TRACE = 'TRACE'

### TrieNode
class TrieNode():
	"""
	TrieNode: {
	  regex: str
	  endpoint: Bool
	  http_method: HTTPMethod
	  children: List[TrieNode]
	}
	"""
	def __init__(self, regex: str):
		self.regex = regex
		self.method_role_mapping = {
		    'GET': set(),
		    'POST': set(),
		    'PUT': set(),
		    'PATCH': set(),
		    'DELETE': set(),
		    'HEAD': set(),
		    'CONNECT': set(),
		    'OPTIONS': set(),
		    'TRACE': set()
		}
		self.endpoint = False
		self.children = []
	def add_role(self, http_method: HTTPMethod, role: str):
		self.method_role_mapping[http_method].add(role)
	def remove_role(self, http_method: HTTPMethod, role: str):
		role in self.method_role_mapping and self.method_role_mapping[http_method].remove(role)
	def add_child(self, child_node):
		self.children.append(child_node)
	def remove_child(self, regex: str):
		self.children = [child_node for child_node in self.children if child_node.regex != regex]
	def is_endpoint(self):
		return self.endpoint
	def make_endpoint(self):
		self.endpoint = True
	def remove_endpoint(self):
		self.endpoint = False
	def match(self, segment: str):
		if self.regex == '*':
			return True
		if self.regex == segment:
			return True
		return False
	def __str__(self):
		return f"{(self.regex, self.endpoint)}: {[child_node for child_node in self.children]}"
	def __repr__(self):
		return f"{self.regex}"

### Trie
class Trie():
	def __init__(self):
		self.root_node = TrieNode('')
	def add_route(self, route: str, http_method: HTTPMethod, roles: Set[str]):
		route = route.rstrip("/")
		# print(route)
		route_segments = route.split("/")
		current_node: TrieNode = self.root_node
		for segment in route_segments:
			found: bool = False
			for child_node in current_node.children:
				if child_node.regex == segment:
					current_node = child_node
					found = True
					break
			if not found:
				new_node: TrieNode = TrieNode(regex=segment)
				current_node.add_child(new_node)
				current_node = new_node
		current_node.make_endpoint()
		for role in roles:
			current_node.add_role(http_method=http_method, role=role)
	def get_route_method_role_mapping(self, route: str):
		route = route.rstrip("/")
		route_segments = route.split("/")
		current_node: TrieNode = self.root_node
		for segment in route_segments:
			found: bool = False
			for child_node in current_node.children:
				if child_node.match(segment=segment):
					current_node = child_node
					found = True
					break
			if not found:
				raise INVALID_ROUTE_EXCEPTION
		if not current_node.is_endpoint():
			raise INVALID_ROUTE_EXCEPTION
		return current_node.method_role_mapping
	def get_root(self):
		return self.root_node
	def traverse(self, source_node: TrieNode = None):
		if not source_node:
			source_node = self.get_root()
		print(str(source_node))
		for child_node in source_node.children:
			self.traverse(source_node=child_node)

### MAIN
def main():
	with open('route_role.json') as file:
		records = load(file)
	pprint(records)
	trie: Trie = Trie()
	for record in records:
		trie.add_route(route=record['route'], http_method=record['method'], roles=set(record['roles']))

	mapping = trie.get_route_method_role_mapping(route='api/product/12234/details')
	pprint(mapping)
	mapping = trie.get_route_method_role_mapping(route='api/organiser/12234/preview')
	pprint(mapping)
	trie.traverse()

### Runner
if __name__ == "__main__":
	main()