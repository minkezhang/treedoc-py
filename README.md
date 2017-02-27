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

## Readings

* **Attiya** *et al.*. Specification and Complexity of Collaborative Text Editing. *2016*.
* **Burckhardt**, **Gotsman**, **Yang**, and **Zawirski**. Replicated Data Types: Specification, Verification, Optimality. *2014*.
* **Letia**, **Preguica**, and **Shapiro**. Consistency Without Concurrency Control in Large, Dynamic Systems. *2010*.
* **Preguica**, **Marques**, **Shapiro**, and **Letia**. A Commutative Replicated Data Type for Coorperative Editing. *2009*.
* **Shapiro**, **Preguica**, **Baquero**, and **Zawirski**. A Comprehensive Study of Convergent and Commutative Replicated Data Types. *2011*.
* **Shapiro**, **Preguica, **Baquero**, and **Zawirski**. Conflict-free Replicated Data Types. *2011*.
