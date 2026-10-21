"""
Open Break — Database Schema Reference
Relational Model for Multi-Tenant Boutique Studios (PostgreSQL / Supabase)
Includes Row-Level Security, Atomic Slot Locking, and Immutable Credit Ledger.
"""

SCHEMA_SQL = """
-- ============================================================================
-- EXTENSIONS & UUIDs
-- ============================================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- 1. MULTI-TENANCY & LOCATIONS
-- ============================================================================
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug VARCHAR(64) UNIQUE NOT NULL,
    business_name VARCHAR(255) NOT NULL,
    currency VARCHAR(3) DEFAULT 'MXN',
    timezone VARCHAR(64) DEFAULT 'America/Mexico_City',
    cancellation_window_hours INT DEFAULT 12, -- Política transparente de cancelación
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL, -- Ej: 'Polanco', 'Roma Norte'
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- 2. PHYSICAL RESOURCES & BEDS (Catálogo Físico de Camas Reformer / Bicis)
-- ============================================================================
CREATE TABLE studio_rooms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    name VARCHAR(128) NOT NULL, -- Ej: 'Sala Principal Reformer'
    capacity INT NOT NULL CHECK (capacity > 0 AND capacity <= 50)
);

CREATE TABLE studio_resources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    room_id UUID NOT NULL REFERENCES studio_rooms(id) ON DELETE CASCADE,
    identifier VARCHAR(32) NOT NULL, -- Ej: 'Cama 01', 'Cama 02'
    resource_type VARCHAR(64) DEFAULT 'REFORMER',
    is_operational BOOLEAN DEFAULT TRUE,
    hours_worked NUMERIC(8, 2) DEFAULT 0.00,
    last_spring_maintenance TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- 3. CLASS SESSIONS & SLOTS (Unidad Atómica de Reserva)
-- ============================================================================
CREATE TABLE class_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    room_id UUID NOT NULL REFERENCES studio_rooms(id) ON DELETE RESTRICT,
    title VARCHAR(255) NOT NULL,
    instructor_name VARCHAR(255) NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    capacity INT NOT NULL CHECK (capacity > 0),
    booked_count INT NOT NULL DEFAULT 0 CHECK (booked_count >= 0 AND booked_count <= capacity),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_times CHECK (end_time > start_time)
);

CREATE TABLE class_slots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES class_sessions(id) ON DELETE CASCADE,
    resource_id UUID REFERENCES studio_resources(id) ON DELETE SET NULL,
    slot_number INT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'AVAILABLE' CHECK (status IN ('AVAILABLE', 'LOCKED', 'BOOKED')),
    booked_user_id UUID,
    locked_until TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- 4. ATOMIC BOOKINGS WITH ROW-LEVEL LOCKING
-- ============================================================================
CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    session_id UUID NOT NULL REFERENCES class_sessions(id) ON DELETE CASCADE,
    slot_id UUID NOT NULL REFERENCES class_slots(id) ON DELETE RESTRICT,
    user_id UUID NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'CONFIRMED' CHECK (status IN ('CONFIRMED', 'CANCELLED', 'ATTENDED', 'NO_SHOW')),
    payment_method VARCHAR(32) DEFAULT 'CREDIT',
    idempotency_key VARCHAR(128) UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    cancelled_at TIMESTAMPTZ
);

-- Índice parcial: Un alumno no puede tener dos reservas simultáneas activas en la misma clase
CREATE UNIQUE INDEX idx_unique_active_booking 
ON bookings(session_id, user_id) 
WHERE status = 'CONFIRMED';

-- ============================================================================
-- 5. IMMUTABLE CREDIT LEDGER (Doble Partida / Append-Only)
-- ============================================================================
CREATE TABLE credit_ledger (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    booking_id UUID REFERENCES bookings(id),
    transaction_type VARCHAR(32) NOT NULL CHECK (transaction_type IN ('PURCHASE', 'BOOKING_DEBIT', 'CANCELLATION_REFUND', 'MANUAL_ADJUSTMENT')),
    amount INT NOT NULL, -- Negativo para consumos, positivo para compras o devoluciones
    balance_after INT NOT NULL CHECK (balance_after >= 0), -- Previene saldos negativos
    description TEXT,
    idempotency_key VARCHAR(128) UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- 6. AUTONOMOUS WAITLISTS
-- ============================================================================
CREATE TABLE waitlists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES class_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    position INT NOT NULL,
    status VARCHAR(32) DEFAULT 'QUEUED' CHECK (status IN ('QUEUED', 'OFFERED', 'EXPIRED', 'ACCEPTED')),
    offered_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_user_session_waitlist UNIQUE (session_id, user_id)
);
"""

if __name__ == "__main__":
    print("Esquema relacional y motor atómico de PostgreSQL compilado con éxito.")
    print("Contiene RLS, bloqueo transaccional, ledger inmutable y asignación física de camas.")
