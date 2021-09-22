# IMPLEMENTATION OF TRIE TO GET ROUTE'S OBJECT

### supporting DS

```
HTTPMethod(Enum):
  GET = 'GET'
  POST = 'POST'
  PUT = 'PUT'
  PATCH = 'PATCH'
  DELETE = 'DELETE'
  HEAD = 'HEAD'
  CONNECT = 'CONNECT'
  OPTIONS = 'OPTIONS'
  TRACE = 'TRACE'
```
```
ROLE: Str
```

## TRIE NODE:
```
TrieNode: {
  regex: r'{Str}'
  is_endpoint: Bool
  http_method: {
    GET: List[Role]
    POST: List[Role]
    PUT: List[Role]
    PATCH: List[Role]
    DELETE: List[Role]
    HEAD: List[Role]
    CONNECT: List[Role]
    OPTIONS: List[Role]
    TRACE: List[Role]
  }
  children: List[TrieNode]
}
```

## Supported Functions:
- build_trie_from_mapping(file: JSONFile) -> TrieNode
- add_route_to_mapping(url: str, method: HTTPMethod, roles: List[Role]) -> None
- remove_route_from_mapping(url: str, method: HTTPMethod, roles: List[Role]) -> None
- get_valid_roles_for_route(url: str, method: HTTPMethod) -> List[Role]
- authorize_user_for_route(url: str, method: HTTPMethod, roles: List[Role]) -> Bool

## Mapping File (JSON)
ROUTE | METHOD | ROLES
--- | --- | ---
str | HTTPMethod | List[Role]
... | ... | ...
... | ... | ...