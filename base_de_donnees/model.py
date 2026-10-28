from sqlalchemy import MetaData, Table, Column, Integer, Text

metadata = MetaData()

donnees = Table(
    "donnees",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("donnee", Text, nullable=False),
)
