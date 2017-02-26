# treedoc-py

## TODO

* Add PrevNodeOp
* Clear NextNode, PrevNode when invoking AddNodeOp
* Add DeleteNodeOp
* Add ReadDataOp (take into consideration Node.is_deleted)
* Add WriteDataOp (insert data into tree in a balanced manner)
* Add GarbageCollectOp (delete nodes)
* Add RebalanceOp (consolidate nodes)
* Add ExplodeNodeOp (explode nodes)
* Add SelectNodeOp (per-client basis, call ExplodeNodeOp)

## Installation

```
git clone https://github.com/cripplet/treedoc-py
cd treedoc-py
virtualenv v
. ./v/bin/activate
pip install -r requirements.txt
```

## Testing

```
nosetests --cover-erase --with-coverage --cover-branches \
    --cover-html --cover-html-dir=coverage --cover-package=src
```
