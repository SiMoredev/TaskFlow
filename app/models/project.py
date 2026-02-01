from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    owner = relationship("User", backref="projects")