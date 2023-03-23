import os
import re
def deleteIfExist(e,l):
    if e in l:
        l.remove(e)
    return l
# Directory containing the NIPs
NIPS_DIR = '.'

# Regular expression to match the depends tags
DEPENDS_RE = re.compile(r'`depends:([^ `]+)`')

# Set up the graphviz graph
graph = ['digraph {']

# store dependencies relationship
nip_depends = {}
md_files = [f for f in os.listdir(NIPS_DIR) if f.endswith('.md')]
md_files.remove('README.md')
nip_nodes = list(map(lambda x: 'NIP '+x.replace(".md", ""), sorted(md_files)))
print(nip_nodes)
# Read all the NIPs and extract their dependencies
for filename in sorted(os.listdir(NIPS_DIR)):
    if not filename.endswith('.md'):
        continue

    path = os.path.join(NIPS_DIR, filename)

    with open(path, 'r') as f:
        lines = f.readlines()

    # Extract the NIP number and title from the filename

    nip_num = 'NIP '+filename.replace(".md", "")
    nip_title = lines[0].strip().replace('#', '').strip()

    # Extract the dependencies from the depends tags
    depends = []
    allText = ''.join(lines)
    match = DEPENDS_RE.findall(allText)
    if match:
        depends = [dep.strip() for dep in match]
        print(depends)
        depends = map(lambda x: 'NIP '+x, depends)
        nip_depends[filename]   = depends
    # Write the NIP node and its dependencies to the .dot file
    
    # print(len(depends))
    for dep in depends:
        deleteIfExist(dep.strip(),nip_nodes)
        deleteIfExist(nip_num,nip_nodes)
        graph += ['  "{}" -> "{}";'.format( dep.strip(),nip_num)]

for nip_num in nip_nodes:
    graph += ['  "{}" [label="{}"];'.format(nip_num, nip_num)]
graph.append('}')

# Write the .dot file
with open('scripts/tree.dot', 'w') as f:
    f.write('\n'.join(graph))


