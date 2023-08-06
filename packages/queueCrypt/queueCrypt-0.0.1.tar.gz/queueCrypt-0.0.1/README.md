# queueCrypt.
"queueCrypt" is a library that is library that creates a queue and secures it better.
Basically this library encrypts the data that is been added to the queue and saves the data 
securely and safely.

## Libraries Needed:
`pip install cryptography`

this library is needed to encrypt the data. Without this
library the library won't work!

## How To Call The Library?
```python
from queueCrypt import Queue
```

### To Call The Errors Exceptions Use:
```python
from queueCrypt import ErrorQueueSizeNotValid, ErrorRequestedHigherThanExpected
#----OR----#
from queueCrypt.errors import *
```

### To Call The Encryption Handler Use:
```python
from queueCrypt.ext import Encryption
#----OR----#
from queueCrypt.ext import *
```

## First Thing That Needed Before Using...
```python
from queueCrypt import *

q = Queue(5)
```
Every time that you create the Queue function you MUST use `Queue(number)`. By setting a number, 
you set the queue length, that can be changed if you need by using `q.change_queue_length(number)`.

## Examples:
* Let's create a secret input from the user that takes passwords
and encrypts them. The user will type the passwords until he will type `"quit"`. After adding them
to the queue, print the encrypted list, and the decrypted list.
```python
from queueCrypt import *

q = Queue(5)
counter = 0

while True:
    counter += 1
    user = input("Type passwords: ")
    if user == "quit":
        break
    try:
        # When putting the user data you need to convert it to bytes!
        q.put(bytes(user, 'utf8'))
    except ErrorRequestedHigherThanExpected:
        # change queue length.
        q.change_queue_length(counter)
        
# returns in bytes form.
print(q.get_queue_encrypted())
print(q.get_queue_decrypted())
```

* Now let's say that you want to encrypt the data again
but after printing the inputted data, you return the encrypted data and delete it.
```python
from queueCrypt import *

q = Queue(5)
counter = 0

while True:
    counter += 1
    user = input("Type passwords: ")
    if user == "quit":
        break
    try:
        # When putting the user data you need to convert it to bytes!
        q.put(bytes(user, 'utf8'))
        # takes the first element and decodes it.
        print(q.get_queue_encrypted()[0].decode())
        # destroys the first element in the queue list with timeout of 0.1.
        q.next_and_destroy(0.1)
    except ErrorRequestedHigherThanExpected:
        # change queue length.
        q.change_queue_length(counter)
```
