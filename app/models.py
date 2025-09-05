from sqlalchemy import (
    Column, BigInteger, Integer, String, Boolean, DateTime, Text,
    Numeric, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import INET, CIDR
from datetime import datetime
from typing import Optional, List
from app.session import Base



class User(Base):
    __tablename__ = 'users'

    # id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False, primary_key=True)
    username = Column(String(32), nullable=True)
    first_name = Column(String(64), nullable=False)
    is_active = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    subscription_end_date = Column(DateTime(timezone=True), nullable=True)     # Дата и время окончания подписки - NULL означает отсутствие подписки
    created_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_activity = Column(DateTime(timezone=True), nullable=True)

    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    peers = relationship("Peer", back_populates="user", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")

    @property
    def is_subscription_active(self) -> bool:
        if not self.subscription_end_date:
            return False
        return datetime.now() < self.subscription_end_date


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, ForeignKey('users.tg_id', ondelete='CASCADE'), nullable=False)
    amount = Column(Integer, nullable=False)
    number_of_months = Column(Integer, nullable=False)
    payment_screenshot = Column(Text, nullable=True)
    status = Column(String(28), default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="payments")

    __table_args__ = (
        CheckConstraint("status IN ('pending','confirmed','rejected','refunded')", name='check_status'),
        CheckConstraint("amount > 0", name='check_amount_positive')
    )
    def __repe__(self):
        return f"<Payment(id={self.id}, user_id={self.user_id}, amount={self.amount}, status={self.status}>"


class Peer(Base):
    __tablename__ = "peers"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, ForeignKey('users.tg_id', ondelete='CASCADE'), nullable=False)
    vpn_ip_address = Column(INET, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    last_handshake = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # update_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="peers")
    traffic_stats = relationship("TrafficStat", back_populates="peer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Peer(id={self.id}, user_id={self.user_id}, vpn_ip='{self.vpn_ip_address}')>"


class TrafficStat(Base):
    __tablename__ = 'traffic_stats'

    id = Column(Integer, primary_key=True)
    peer_id = Column(Integer, ForeignKey('peers.id', onupdate='CASCADE'), nullable=False)
    bytes_sent = Column(BigInteger, default=0)
    bytes_received = Column(BigInteger, default=0)
    packets_sent = Column(BigInteger, default=0)
    packets_received = Column(BigInteger, default=0)
    session_start = Column(DateTime(timezone=True), nullable=False)
    session_end = Column(DateTime(timezone=True), nullable=True)
    client_ip = Column(INET, nullable=True)

    peer = relationship("Peer", back_populates="traffic_stats")

    __table_args__ = (
        CheckConstraint('bytes_sent >= 0', name='check_bytes_sent_non_negative'),
        CheckConstraint('bytes_received >= 0', name='check_bytes_received_non_negative'),
    )

    def __repr__(self):
        return f"<TrafficStat(id={self.id}, peer_id={self.peer_id}, total_bytes={self.total_bytes})>"

    @property
    def total_bytes(self):
        return self.bytes_sent + self.bytes_received

    def is_active_session(self) -> bool:
        return self.session_end is None


class ActivityLog(Base):
    __tablename__ = 'activity_logs'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, ForeignKey("users.tg_id", ondelete='CASCADE'), nullable=True)
    action = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    ip_address = Column(INET, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship('User', back_populates="activity_logs")

    def __repr__(self):
        return f"<ActivityLog(id={self.id}, action='{self.action}', user_id={self.user_id})>"


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, ForeignKey('users.tg_id', ondelete='CASCADE'), nullable=False)
    type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    massage = Column(Text, nullable=False)
    is_read = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates='notifications')

    def __repr__(self):
        return f"<Notification(id={self.id}, type='{self.type}', user_id={self.user_id})>"



# Константы для enum-значений
class PaymentStatus:
    PENDING = 'Ожидает подтверждения'
    CONFIRMED = 'Подтвержден администратором'
    REJECTED = 'Отклонен администратором'
    REFUNDED = 'Возвращен пользователю'


class NotificationType:
    PAYMENT_REMINDER = 'payment_reminder'        # Напоминание об оплате
    SUBSCRIPTION_EXPIRED = 'subscription_expired' # Подписка истекла
    CONFIG_GENERATED = 'config_generated'        # Конфиг создан
    ACCOUNT_BLOCKED = 'account_blocked'          # Аккаунт заблокирован


class ActivityAction:
    USER_REGISTERED = 'user_registered'           # Пользователь зарегистрировался
    PAYMENT_CREATED = 'payment_created'           # Создан платеж
    PAYMENT_CONFIRMED = 'payment_confirmed'       # Платеж подтвержден
    CONFIG_GENERATED = 'config_generated'         # Создан VPN конфиг
    SUBSCRIPTION_EXTENDED = 'subscription_extended' # Подписка продлена
    USER_BLOCKED = 'user_blocked'                 # Пользователь заблокирован
    LOGIN = 'login'                              # Вход в систему

