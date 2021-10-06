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
	  method_role_mapping: Dict[HTTPMethod, Set[str]]
	  children: List[TrieNode]
	}
	"""
	def __init__(self, regex: str):
		"""
		Initializes TrieNode Object with assigning default values to attributes
		Parameters:
			regex: str - regular expression for the route segment
		Returns:
			TrieNode object
		"""
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
		"""
		Adds role to the particular route and method
		Parameters:
			http_method: HTTPMethod - request's http method
			role: str - role to be added to the endpoint
		Returns:
			None
		"""
		self.method_role_mapping[http_method].add(role)
	def remove_role(self, http_method: HTTPMethod, role: str):
		"""
		Removes role from the particular route and method
		Parameters:
			http_method: HTTPMethod - request's http method
			role: str - role to be added to the endpoint
		Returns:
			None
		"""
		role in self.method_role_mapping and self.method_role_mapping[http_method].remove(role)
	def add_child(self, child_node):
		"""
		Adds child TrieNode to the Present TrieNode
		Parameters:
			child_node: TrieNode - child TrieNode to be added
		Returns:
			None
		"""
		self.children.append(child_node)
	def remove_child(self, regex: str):
		"""
		Removes child TrieNode from the Present TrieNode if present
		Parameters:
			child_node: TrieNode - child TrieNode to be added
		Returns:
			None
		"""
		self.children = [child_node for child_node in self.children if child_node.regex != regex]
	def is_endpoint(self) -> bool:
		"""
		Returns weather the TrieNode is the end of an endpoint.
		Parameters:
			None
		Returns:
			bool
		"""
		return self.endpoint
	def make_endpoint(self):
		"""
		Makes the TrieNode the end of an endpoint.
		Parameters:
			None
		Returns:
			None
		"""
		self.endpoint = True
	def remove_endpoint(self):
		"""
		Makes the TrieNode non-end of any endpoint.
		Parameters:
			None
		Returns:
			None
		"""
		self.endpoint = False
	def match(self, segment: str) -> bool:
		"""
		Returns weather the segment matches the TrieNode regex
		Parameters:
			segment: str - the segment of queried route
		Returns:
			bool
		"""
		return True if self.regex == '*' or self.regex == segment else False
	def __str__(self):
		return f"{(self.regex, self.endpoint)}: {[child_node for child_node in self.children]}"
	def __repr__(self):
		return f"{self.regex}"

### Trie
class Trie():
	def __init__(self):
		"""
		Initializes the Trie with a root TrieNode
		Parameters:
			None
		Returns:
			Trie object
		"""
		self.root_node = TrieNode('')
	def add_route(self, route: str, http_method: HTTPMethod, roles: Set[str]):
		"""
		Adds routes to the Trie
		Parameters:
			route: str - the route string
			http_method: HTTPMethod - Method of the expected request
			roles: Set[str] - Set of roles needs to be assigned to the endpoint
		Returns:
			None
		"""
		route = route.rstrip("/")
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
		"""
		Gets the route's method and role mapping
		Parameters:
			route: str - the route string
		Returns:
			Dict[HTTPMethod, Set[str]]
		"""
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
	def traverse(self, source_node: TrieNode = None):
		if not source_node:
			source_node = self.root_node
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