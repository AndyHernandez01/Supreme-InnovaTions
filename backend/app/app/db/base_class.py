from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
  id
  __name__: str
  # Generates table name
  @declared_attr
  def __tablename__(cls) ->str:
    return cls.__name__.lower()