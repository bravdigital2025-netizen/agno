-- =============================================================================
-- Jarvis — Esquema do banco de dados
-- Multi-tenant: cada loja é um tenant isolado por tenant_id
-- =============================================================================

-- ---------------------------------------------------------------------------
-- TENANTS
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS tenants (
    id              TEXT        PRIMARY KEY,
    store_name      TEXT        NOT NULL,
    cnpj            TEXT        UNIQUE,
    phone           TEXT,
    address         TEXT,
    city            TEXT,
    state           CHAR(2),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- FORNECEDORES (Suppliers)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS suppliers (
    id              SERIAL      PRIMARY KEY,
    tenant_id       TEXT        NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name            TEXT        NOT NULL,
    cnpj            TEXT,
    contact_name    TEXT,
    phone           TEXT,
    email           TEXT,
    lead_time_days  INTEGER     NOT NULL DEFAULT 7,
    active          BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_suppliers_tenant ON suppliers(tenant_id);

-- ---------------------------------------------------------------------------
-- CATEGORIAS DE PRODUTO
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS product_categories (
    id              SERIAL      PRIMARY KEY,
    tenant_id       TEXT        NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name            TEXT        NOT NULL,
    description     TEXT
);

CREATE INDEX IF NOT EXISTS idx_product_categories_tenant ON product_categories(tenant_id);

-- ---------------------------------------------------------------------------
-- PRODUTOS
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS products (
    id              SERIAL      PRIMARY KEY,
    tenant_id       TEXT        NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    sku             TEXT        NOT NULL,
    name            TEXT        NOT NULL,
    description     TEXT,
    unit            TEXT        NOT NULL DEFAULT 'un',   -- un, sc, m², m³, kg, l, cx
    category_id     INTEGER     REFERENCES product_categories(id),
    supplier_id     INTEGER     REFERENCES suppliers(id),
    cost_price      NUMERIC(12,2),
    sale_price      NUMERIC(12,2) NOT NULL,
    active          BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(tenant_id, sku)
);

CREATE INDEX IF NOT EXISTS idx_products_tenant ON products(tenant_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_supplier ON products(supplier_id);

-- ---------------------------------------------------------------------------
-- ESTOQUE (Inventory)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS inventory (
    id              SERIAL      PRIMARY KEY,
    tenant_id       TEXT        NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    product_id      INTEGER     NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    current_qty     NUMERIC(12,3) NOT NULL DEFAULT 0,
    min_qty         NUMERIC(12,3) NOT NULL DEFAULT 0,   -- estoque mínimo (ponto de pedido)
    max_qty         NUMERIC(12,3),                       -- estoque máximo
    location        TEXT,                                -- posição no depósito
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(tenant_id, product_id)
);

CREATE INDEX IF NOT EXISTS idx_inventory_tenant ON inventory(tenant_id);
CREATE INDEX IF NOT EXISTS idx_inventory_product ON inventory(product_id);

-- View: produtos com saldo crítico (abaixo do mínimo)
CREATE OR REPLACE VIEW vw_critical_stock AS
SELECT
    p.tenant_id,
    p.id            AS product_id,
    p.sku,
    p.name          AS product_name,
    p.unit,
    i.current_qty,
    i.min_qty,
    i.max_qty,
    (i.min_qty - i.current_qty) AS qty_to_reorder,
    s.name          AS supplier_name,
    s.lead_time_days,
    p.cost_price,
    p.sale_price
FROM inventory i
JOIN products p  ON p.id = i.product_id
LEFT JOIN suppliers s ON s.id = p.supplier_id
WHERE i.current_qty <= i.min_qty
  AND p.active = TRUE;

-- ---------------------------------------------------------------------------
-- MOVIMENTAÇÕES DE ESTOQUE
-- ---------------------------------------------------------------------------

CREATE TYPE stock_movement_type AS ENUM ('entrada', 'saida', 'ajuste', 'devolucao');

CREATE TABLE IF NOT EXISTS stock_movements (
    id              SERIAL              PRIMARY KEY,
    tenant_id       TEXT                NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    product_id      INTEGER             NOT NULL REFERENCES products(id),
    movement_type   stock_movement_type NOT NULL,
    qty             NUMERIC(12,3)       NOT NULL,
    unit_cost       NUMERIC(12,2),
    reference_id    TEXT,               -- NF, pedido, ajuste manual
    notes           TEXT,
    created_at      TIMESTAMPTZ         NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stock_movements_tenant   ON stock_movements(tenant_id);
CREATE INDEX IF NOT EXISTS idx_stock_movements_product  ON stock_movements(product_id, created_at DESC);

-- ---------------------------------------------------------------------------
-- CLIENTES (Customers)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS customers (
    id              SERIAL      PRIMARY KEY,
    tenant_id       TEXT        NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name            TEXT        NOT NULL,
    cpf_cnpj        TEXT,
    phone           TEXT,
    whatsapp        TEXT,
    email           TEXT,
    address         TEXT,
    city            TEXT,
    state           CHAR(2),
    customer_type   TEXT        NOT NULL DEFAULT 'varejo',  -- varejo, empreiteiro, construtora
    active          BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_customers_tenant  ON customers(tenant_id);
CREATE INDEX IF NOT EXISTS idx_customers_phone   ON customers(tenant_id, phone);
CREATE INDEX IF NOT EXISTS idx_customers_whatsapp ON customers(tenant_id, whatsapp);

-- ---------------------------------------------------------------------------
-- PEDIDOS / VENDAS (Orders / Sales)
-- ---------------------------------------------------------------------------

CREATE TYPE order_status AS ENUM ('orcamento', 'confirmado', 'faturado', 'entregue', 'cancelado');

CREATE TABLE IF NOT EXISTS orders (
    id              SERIAL          PRIMARY KEY,
    tenant_id       TEXT            NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    customer_id     INTEGER         REFERENCES customers(id),
    order_number    TEXT            NOT NULL,
    status          order_status    NOT NULL DEFAULT 'orcamento',
    order_date      DATE            NOT NULL DEFAULT CURRENT_DATE,
    delivery_date   DATE,
    subtotal        NUMERIC(14,2)   NOT NULL DEFAULT 0,
    discount        NUMERIC(14,2)   NOT NULL DEFAULT 0,
    total           NUMERIC(14,2)   NOT NULL DEFAULT 0,
    notes           TEXT,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    UNIQUE(tenant_id, order_number)
);

CREATE INDEX IF NOT EXISTS idx_orders_tenant    ON orders(tenant_id);
CREATE INDEX IF NOT EXISTS idx_orders_customer  ON orders(tenant_id, customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_date      ON orders(tenant_id, order_date DESC);
CREATE INDEX IF NOT EXISTS idx_orders_status    ON orders(tenant_id, status);

-- ---------------------------------------------------------------------------
-- ITENS DO PEDIDO
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS order_items (
    id              SERIAL      PRIMARY KEY,
    order_id        INTEGER     NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id      INTEGER     NOT NULL REFERENCES products(id),
    qty             NUMERIC(12,3) NOT NULL,
    unit_price      NUMERIC(12,2) NOT NULL,
    discount        NUMERIC(12,2) NOT NULL DEFAULT 0,
    subtotal        NUMERIC(14,2) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_order_items_order   ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);

-- ---------------------------------------------------------------------------
-- CAMPANHAS DE MARKETING
-- ---------------------------------------------------------------------------

CREATE TYPE campaign_status AS ENUM ('rascunho', 'agendada', 'em_execucao', 'concluida', 'cancelada');
CREATE TYPE campaign_channel AS ENUM ('whatsapp', 'instagram', 'facebook', 'email', 'sms');

CREATE TABLE IF NOT EXISTS campaigns (
    id              SERIAL          PRIMARY KEY,
    tenant_id       TEXT            NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name            TEXT            NOT NULL,
    description     TEXT,
    channel         campaign_channel NOT NULL DEFAULT 'whatsapp',
    status          campaign_status  NOT NULL DEFAULT 'rascunho',
    message_template TEXT,
    target_segment  TEXT,           -- JSON or text describing the target audience
    scheduled_at    TIMESTAMPTZ,
    sent_count      INTEGER         NOT NULL DEFAULT 0,
    delivered_count INTEGER         NOT NULL DEFAULT 0,
    read_count      INTEGER         NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_campaigns_tenant ON campaigns(tenant_id);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(tenant_id, status);

-- ---------------------------------------------------------------------------
-- CONVERSAS WHATSAPP
-- ---------------------------------------------------------------------------

CREATE TYPE message_direction AS ENUM ('inbound', 'outbound');

CREATE TABLE IF NOT EXISTS whatsapp_conversations (
    id              SERIAL      PRIMARY KEY,
    tenant_id       TEXT        NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    customer_id     INTEGER     REFERENCES customers(id),
    phone           TEXT        NOT NULL,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_message_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved        BOOLEAN     NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_conv_tenant ON whatsapp_conversations(tenant_id);
CREATE INDEX IF NOT EXISTS idx_whatsapp_conv_phone  ON whatsapp_conversations(tenant_id, phone);

CREATE TABLE IF NOT EXISTS whatsapp_messages (
    id              SERIAL              PRIMARY KEY,
    conversation_id INTEGER             NOT NULL REFERENCES whatsapp_conversations(id) ON DELETE CASCADE,
    direction       message_direction   NOT NULL,
    content         TEXT                NOT NULL,
    wamid           TEXT,               -- WhatsApp message ID
    created_at      TIMESTAMPTZ         NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_messages_conv ON whatsapp_messages(conversation_id, created_at DESC);

-- ---------------------------------------------------------------------------
-- PROJETOS / ORÇAMENTOS DE OBRA
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS projects (
    id              SERIAL      PRIMARY KEY,
    tenant_id       TEXT        NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    customer_id     INTEGER     REFERENCES customers(id),
    name            TEXT        NOT NULL,
    description     TEXT,
    area_m2         NUMERIC(10,2),
    quote_data      JSONB,      -- ProjectQuote JSON from projects_agent
    total_estimate  NUMERIC(14,2),
    status          TEXT        NOT NULL DEFAULT 'rascunho',  -- rascunho, enviado, aprovado, perdido
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_projects_tenant   ON projects(tenant_id);
CREATE INDEX IF NOT EXISTS idx_projects_customer ON projects(tenant_id, customer_id);

-- ---------------------------------------------------------------------------
-- VIEWS ANALÍTICAS
-- ---------------------------------------------------------------------------

-- Resumo de vendas por dia
CREATE OR REPLACE VIEW vw_daily_sales AS
SELECT
    tenant_id,
    order_date,
    COUNT(*)                AS total_orders,
    SUM(total)              AS total_revenue,
    AVG(total)              AS avg_ticket,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM orders
WHERE status IN ('faturado', 'entregue')
GROUP BY tenant_id, order_date;

-- Top produtos mais vendidos (últimos 30 dias)
CREATE OR REPLACE VIEW vw_top_products_30d AS
SELECT
    o.tenant_id,
    p.id            AS product_id,
    p.sku,
    p.name          AS product_name,
    p.unit,
    SUM(oi.qty)     AS total_qty_sold,
    SUM(oi.subtotal) AS total_revenue
FROM order_items oi
JOIN orders o   ON o.id = oi.order_id
JOIN products p ON p.id = oi.product_id
WHERE o.status IN ('faturado', 'entregue')
  AND o.order_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY o.tenant_id, p.id, p.sku, p.name, p.unit
ORDER BY total_qty_sold DESC;

-- ---------------------------------------------------------------------------
-- SEED DATA — Tenant demo
-- ---------------------------------------------------------------------------

INSERT INTO tenants (id, store_name, cnpj, city, state)
VALUES ('demo', 'Construmais Demo', '00.000.000/0001-00', 'São Paulo', 'SP')
ON CONFLICT (id) DO NOTHING;

INSERT INTO product_categories (tenant_id, name, description) VALUES
    ('demo', 'Cimento e Argamassa', 'Cimentos, argamassas e similares'),
    ('demo', 'Agregados', 'Areia, brita e pedra'),
    ('demo', 'Alvenaria', 'Tijolos, blocos e cobogos'),
    ('demo', 'Aço e Metais', 'Aços para construção civil'),
    ('demo', 'Cerâmica e Revestimento', 'Porcelanatos, cerâmicas e argamassas colantes'),
    ('demo', 'Cobertura', 'Telhas, calhas e rufos'),
    ('demo', 'Tintas e Impermeabilizantes', 'Tintas, seladores e impermeabilizantes'),
    ('demo', 'Hidráulica', 'Tubos, conexões e registros')
ON CONFLICT DO NOTHING;
