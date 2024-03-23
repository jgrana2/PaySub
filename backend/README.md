# Subscription Management System

This Python code provides classes for managing operations using the Appwrite backend services. The class includes methods for user registration, managing subscriptions, adding cards, and handling subscribers.

## Usage

```bash
git clone https://github.com/jgrana2/paygate_cloud.git
cd paygate_cloud
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Create an instance of the User class by providing the user's email address. For example:

```python
from CreditCard import CreditCard
from Subscription import Subscription
from User import User

user = User("test@example.com")
```
