-- AutomateCash MVP SQL migrations (PostgreSQL)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- If TimescaleDB is available, enable it
-- CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE,
  phone VARCHAR(30),
  password_hash TEXT,
  full_name VARCHAR(255),
  role VARCHAR(50) DEFAULT 'user',
  kyc_level INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS wallets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  currency CHAR(3) NOT NULL,
  balance NUMERIC(28,8) DEFAULT 0,
  locked_balance NUMERIC(28,8) DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE(user_id, currency)
);

CREATE TABLE IF NOT EXISTS transactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  wallet_id UUID REFERENCES wallets(id),
  type VARCHAR(50),
  amount NUMERIC(28,8),
  currency CHAR(3),
  status VARCHAR(50),
  ref_id VARCHAR(255),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS orders (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  pair VARCHAR(20),
  side VARCHAR(4),
  type VARCHAR(20),
  quantity NUMERIC(28,8),
  price NUMERIC(28,8),
  status VARCHAR(20) DEFAULT 'OPEN',
  leverage INT DEFAULT 1,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS positions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id UUID REFERENCES orders(id),
  user_id UUID REFERENCES users(id),
  pair VARCHAR(20),
  entry_price NUMERIC(28,8),
  size NUMERIC(28,8),
  side VARCHAR(4),
  current_price NUMERIC(28,8),
  pnl NUMERIC(28,8) DEFAULT 0,
  margin NUMERIC(28,8) DEFAULT 0,
  status VARCHAR(20) DEFAULT 'OPEN',
  opened_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  closed_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS market_ticks (
  time TIMESTAMP WITH TIME ZONE NOT NULL,
  pair VARCHAR(20) NOT NULL,
  bid NUMERIC(28,8),
  ask NUMERIC(28,8),
  PRIMARY KEY (time, pair)
);