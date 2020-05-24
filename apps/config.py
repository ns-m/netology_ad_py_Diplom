from dataclasses import dataclass, field

database = {"dbname": "netology", "user": "postgres", "password": "postgres", "host": "localhost", "port": "5432"}

@dataclass
class Config:
    id: str = "171691064"
    access_token: str = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"
    data: dict = field(default_factory=database)
