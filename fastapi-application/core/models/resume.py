from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Text,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from .base import Base
from .user import User
from .mixin.int_id_pk import IdIntPkMix


class Resume(Base, IdIntPkMix):

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    owner = relationship("User", back_populates="resumes")
