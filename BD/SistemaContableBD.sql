-- Tabla principal de cuentas contables
CREATE TABLE plan_cuentas (
    id_cuenta BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('ACTIVO','PASIVO','PATRIMONIO','INGRESO','COSTO','GASTO')),
    naturaleza VARCHAR(10) NOT NULL CHECK (naturaleza IN ('DEUDORA','ACREEDORA')),
    nivel INT NOT NULL,
    id_padre BIGINT NULL,
    estado BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_plan_cuentas_padre
        FOREIGN KEY (id_padre)
        REFERENCES plan_cuentas (id_cuenta)
);

-- Balance inicial (un registro por cuenta)
CREATE TABLE balance_inicial (
    id_balance BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cuenta BIGINT NOT NULL UNIQUE,
    saldo NUMERIC(15,2) NOT NULL,
    debe_haber VARCHAR(5) NOT NULL CHECK (debe_haber IN ('DEBE','HABER')),
    fecha_registro TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_balance_cuenta
        FOREIGN KEY (id_cuenta)
        REFERENCES plan_cuentas (id_cuenta)
);

-- Asientos contables (cabecera)
CREATE TABLE asientos (
    id_asiento BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha DATE NOT NULL,
    glosa TEXT NOT NULL,
    folio VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Detalle de cada asiento (varias líneas)
CREATE TABLE detalle_asientos (
    id_detalle BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_asiento BIGINT NOT NULL,
    id_cuenta BIGINT NOT NULL,
    debe_haber VARCHAR(5) NOT NULL CHECK (debe_haber IN ('DEBE','HABER')),
    monto NUMERIC(15,2) NOT NULL,
    CONSTRAINT fk_detalle_asiento
        FOREIGN KEY (id_asiento)
        REFERENCES asientos (id_asiento) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_cuenta
        FOREIGN KEY (id_cuenta)
        REFERENCES plan_cuentas (id_cuenta)
);