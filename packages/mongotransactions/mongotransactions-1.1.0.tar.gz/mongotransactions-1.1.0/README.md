# mongotransactions
wrapper around mongoDB transactions and other pymongo operations


### basic commands

```python
from mongotransactions import Database
database = Database('mongodb+srv://username:password@host')

# by default the class will use the first database the uri has access to you can change it with
database.set_database('db_name')

# grab a collection

my_collection = database.get_collection('my_collection')

# then you can do your normal operations
for doc in my_collection.find():
  print(doc)

first = my_collection.find_one()

# a list of collections is avalilble 

print(database.list_collections()) # ['my_collection']

```

### Transactions

package also contains a wrapper around mongo transactions and bulkwrite so that
multiple saves/updates/removes across multiple collections to be batch wrote
to the server and it will all roll back if any one operation fails.

in MongoDB 4.2 and earlier, you cannot create collections in transactions.


The class takes the database class example above


```python

from mongotransactions import Database, Transaction
database = Database('mongodb+srv://username:password@host')

database.set_database('db_name')

transaction = Transaction(database)


# insert operations return a named tuple with _id that will be used and the current transactions
insert = transaction.insert('my_collection', { 'name': 'test'})
transaction.insert('events', { 'details': 'new document added', 'doc_id': insert.id})


print(transaction.transactions)
"""
{'my_collection': [InsertOne({'name': 'test', '_id': ObjectId('5f85b1b908820781dc16fe9d')})], 
'events': [InsertOne({'details': ' new document added', 'doc_id': ObjectId('5f85b1b908820781dc16fe9d'), '_id': ObjectID('5f85b1b908820781dc16fe9e')})]}
"""

# then finally commit 

transaction.run()
```

