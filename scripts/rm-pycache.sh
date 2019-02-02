PROJECT_DIR=$( dirname $( dirname $( realpath $0 ) ) )

paths=( $( python -c "\
from pathlib import Path

PROJECT_DIR = Path('${PROJECT_DIR}')
SRC_DIR = PROJECT_DIR / 'src'
TEST_DIR = PROJECT_DIR / 'test'

def extend_queue(queue, dirpath):
    queue.extend(
        path
        for path in dirpath.iterdir()
        if path.is_dir()
    )

queue = []
paths = []

extend_queue(queue, SRC_DIR)
extend_queue(queue, TEST_DIR)

while queue:
    path = queue.pop(0)
    if path.name == '__pycache__':
        paths.append(path)
    
    elif path.is_dir():
        extend_queue(queue, path)

print(' '.join(str(p) for p in paths))
# print(list(str(p) for p in paths))
" ) )

for path in "${paths[@]}"; do
    rm -r $path
done
