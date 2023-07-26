from dataclasses import dataclass
import hashlib, time, random

@dataclass
class User:
    username: str
    password: str
    user_id: str = None

    def __post_init__(self):
        if self.user_id is None:
            self.user_id = self.create_user_id()

    def hash_password(self):
        password_bytes = self.password.encode('utf-8')
        hash_object = hashlib.sha256()
        hash_object.update(password_bytes)
        return hash_object.hexdigest()
    
    def create_user_id(self):
        timestamp = int(time.time())
        rand = random.randint(1, 1000)
        user_id = '%d-%d' % (timestamp, rand)
        return user_id