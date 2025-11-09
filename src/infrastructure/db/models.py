from sqlalchemy import Integer, String, DateTime, func, Date, Float, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from datetime import datetime, date
from typing import List


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    subscriptions: Mapped[List["Subscription"]] = relationship("Subscription", back_populates="user",
                                                               cascade="all, delete-orphan")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    referrals_given: Mapped[List["Referral"]] = relationship("Referral", foreign_keys="[Referral.referrer_id]",
                                                             back_populates="referrer")
    referrals_received: Mapped[List["Referral"]] = relationship("Referral", foreign_keys="[Referral.referred_user_id]",
                                                                back_populates="referred_user")


class SubscriptionPlan(Base):
    __tablename__ = 'subscription_plans'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default='USD')
    traffic_limit_gb: Mapped[int] = mapped_column(Integer, nullable=False)
    # is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    subscriptions: Mapped[List["Subscription"]] = relationship("Subscription", back_populates="plan")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="plan")


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.tg_id', ondelete='CASCADE'), nullable=False,
                                         index=True)
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey('subscription_plans.id'), nullable=False)
    peer_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('peers.id', ondelete='SET NULL'), nullable=True)

    start_date: Mapped[date] = mapped_column(Date, nullable=False, default=func.current_date())
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    traffic_used_gb: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="subscriptions")
    plan: Mapped["SubscriptionPlan"] = relationship("SubscriptionPlan", back_populates="subscriptions")
    peer: Mapped["Peer"] = relationship("Peer", back_populates="subscriptions")


class Server(Base):
    __tablename__ = 'servers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False, unique=True, index=True)  # IPv6 support
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='active')  # active, inactive, maintenance
    max_peers: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    peers: Mapped[List["Peer"]] = relationship("Peer", back_populates="server", cascade="all, delete-orphan")


class Peer(Base):
    __tablename__ = 'peers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pub_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    server_id: Mapped[int] = mapped_column(Integer, ForeignKey('servers.id', ondelete='CASCADE'), nullable=False)
    private_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    allowed_ips: Mapped[str] = mapped_column(String(100), default='0.0.0.0/0', nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    server: Mapped["Server"] = relationship("Server", back_populates="peers")
    subscriptions: Mapped[List["Subscription"]] = relationship("Subscription", back_populates="peer")


class Order(Base):
    __tablename__ = 'orders'

    order_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False,
                                         index=True)
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey('subscription_plans.id'), nullable=False)

    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default='USD')
    status: Mapped[str] = mapped_column(String(20), nullable=False,
                                        default='pending')  # pending, completed, failed, cancelled
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="orders")
    plan: Mapped["SubscriptionPlan"] = relationship("SubscriptionPlan", back_populates="orders")
    payment: Mapped["Payment"] = relationship("Payment", back_populates="order", uselist=False)


class Payment(Base):
    __tablename__ = 'payments'

    payment_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    order_id: Mapped[str] = mapped_column(String(100), ForeignKey('orders.order_id', ondelete='CASCADE'),
                                          nullable=False, unique=True, index=True)

    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default='USD')
    status: Mapped[str] = mapped_column(String(20), nullable=False,
                                        default='pending')  # pending, completed, failed, refunded
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)  # card, crypto, etc.
    transaction_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="payment")


class Referral(Base):
    __tablename__ = 'referrals'

    referral_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    referrer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False,
                                             index=True)
    referred_user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('users.id', ondelete='SET NULL'),
                                                         nullable=True, index=True)

    referral_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    bonus_amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    referrer: Mapped["User"] = relationship("User", foreign_keys=[referrer_id], back_populates="referrals_given")
    referred_user: Mapped["User"] = relationship("User", foreign_keys=[referred_user_id],
                                                 back_populates="referrals_received")