from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, String, Integer, ForeignKey, Index

class Base(DeclarativeBase):
    pass
    
user_referral = Table(
    'user_referral',
    Base.metadata,
    Column(
        'user_id',
        Integer,
        ForeignKey('users.id'),
        primary_key=True
    ),
    Column(
        'referral_id',
        Integer,
        ForeignKey('referrals.id'),
        primary_key=True
    ),
)
    
class Users(Base):
    __tablename__ = 'users'
        
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False
    )
    
    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )
    
    bonuse: Mapped[int] = mapped_column(
        nullable=False,
        default=0
    )
    
    referral: Mapped['Referrals'] = relationship(
        'Referrals',
        secondary=user_referral,
        back_populates='user',
        cascade='all'
    )
    
    __table_args__ = (
        Index(
            'email_ix', 'email'
        ),
    )
    
    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'bonuse': self.bonuse,
            'refferal': self.referral.value,
        }
    
class Referrals(Base):
    __tablename__ = 'referrals'
    
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False
    )
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )
    
    value: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    user: Mapped['Users'] = relationship(
        'Users',
        secondary=user_referral,
        back_populates='referral'
    )
    
    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user,
        }
