import os
import re

# Directory containing the NIPs
NIPS_DIR = '.'

# Regular expression to match the depends tags
DEPENDS_RE = re.compile(r'`depends:([^ ]+)`')

# Set up the graphviz graph
graph = ['digraph {', 'rankdir=LR']

# store dependencies relationship
nip_depends = {}
md_files = ['NIP '+f.replace(".md", "") for f in os.listdir(NIPS_DIR) if f.endswith('.md')]
nip_nodes = list(map(lambda x: 'NIP '+x, sorted(os.listdir(NIPS_DIR))))
print(nip_nodes)
# Read all the NIPs and extract their dependencies
for filename in sorted(os.listdir(NIPS_DIR)):
    if not filename.endswith('.md'):
        continue

    path = os.path.join(NIPS_DIR, filename)

    with open(path, 'r') as f:
        lines = f.readlines()

    # Extract the NIP number and title from the filename

    nip_num = filename
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
        print(dep.strip(),'sss')
        nip_nodes.remove(dep.strip())
        nip_nodes.remove(nip_num)
        graph += ['  "{}" -> "{}";'.format(nip_num, dep.strip())]

for nip_num in nip_nodes:
    graph += ['  "{}" [label="{}"];'.format(nip_num, nip_title)]
graph.append('}')

# Write the .dot file
with open('tree.dot', 'w') as f:
    f.write('\n'.join(graph))


