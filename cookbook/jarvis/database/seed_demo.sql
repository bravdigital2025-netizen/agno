-- =============================================================================
-- Jarvis — Seed de dados demo para testes
-- Execute após schema.sql
-- =============================================================================

-- Fornecedores
INSERT INTO suppliers (tenant_id, name, cnpj, contact_name, phone, lead_time_days) VALUES
    ('demo', 'Votorantim Cimentos', '48.891.212/0001-00', 'Carlos Souza', '(11) 99999-0001', 5),
    ('demo', 'CSN Aços', '33.042.730/0001-04', 'Ana Lima',    '(11) 99999-0002', 7),
    ('demo', 'Cerâmica Portobello', '83.475.913/0001-91', 'João Silva',  '(48) 99999-0003', 10),
    ('demo', 'Cia de Cimento Itambé', '75.432.358/0001-30', 'Pedro Costa', '(41) 99999-0004', 5)
ON CONFLICT DO NOTHING;

-- Produtos
INSERT INTO products (tenant_id, sku, name, unit, category_id, supplier_id, cost_price, sale_price) VALUES
    ('demo', 'CIM-001', 'Cimento CP II-E-32 50kg', 'sc', 1, 1, 28.00, 36.50),
    ('demo', 'CIM-002', 'Cimento CP III 50kg',     'sc', 1, 4, 27.50, 35.90),
    ('demo', 'ARG-001', 'Argamassa ACII 20kg',      'sc', 1, 1, 14.00, 18.90),
    ('demo', 'AGR-001', 'Areia Média por m³',        'm³', 2, NULL, 80.00, 120.00),
    ('demo', 'AGR-002', 'Brita 1 por m³',            'm³', 2, NULL, 90.00, 135.00),
    ('demo', 'ALV-001', 'Tijolo Cerâmico 9x19x19 cx100', 'cx', 3, NULL, 45.00, 68.00),
    ('demo', 'ALV-002', 'Bloco de Concreto 14x19x39', 'un', 3, NULL, 3.20, 4.80),
    ('demo', 'ACO-001', 'Aço CA-50 10mm (barra 12m)', 'un', 4, 2, 38.00, 52.00),
    ('demo', 'ACO-002', 'Aço CA-50 8mm (barra 12m)',  'un', 4, 2, 24.00, 34.00),
    ('demo', 'CER-001', 'Porcelanato 60x60 Bege m²',  'm²', 5, 3, 32.00, 52.00),
    ('demo', 'CER-002', 'Cerâmica 45x45 m²',           'm²', 5, 3, 18.00, 29.90),
    ('demo', 'COB-001', 'Telha Fibrocimento 2,44m',   'un', 6, NULL, 28.00, 42.00),
    ('demo', 'TIN-001', 'Tinta Látex Branca 18L',     'gl', 7, NULL, 65.00, 98.00),
    ('demo', 'HID-001', 'Tubo PVC Esgoto 100mm 6m',   'un', 8, NULL, 32.00, 48.00)
ON CONFLICT (tenant_id, sku) DO NOTHING;

-- Estoque inicial
INSERT INTO inventory (tenant_id, product_id, current_qty, min_qty, max_qty)
SELECT
    p.tenant_id,
    p.id,
    v.current_qty,
    v.min_qty,
    v.max_qty
FROM products p
JOIN (VALUES
    ('CIM-001', 120.0, 100.0, 500.0),
    ('CIM-002',  45.0, 100.0, 400.0),   -- saldo critico
    ('ARG-001', 200.0,  80.0, 400.0),
    ('AGR-001',  15.0,  20.0, 100.0),   -- saldo critico
    ('AGR-002',  25.0,  20.0, 100.0),
    ('ALV-001',  18.0,  20.0,  80.0),   -- saldo critico
    ('ALV-002', 850.0, 500.0, 3000.0),
    ('ACO-001',  55.0,  30.0, 200.0),
    ('ACO-002',  28.0,  30.0, 200.0),   -- saldo critico
    ('CER-001', 120.0,  60.0, 400.0),
    ('CER-002', 210.0,  80.0, 500.0),
    ('COB-001',  80.0,  40.0, 300.0),
    ('TIN-001',  22.0,  20.0, 100.0),
    ('HID-001',  45.0,  30.0, 200.0)
) AS v(sku, current_qty, min_qty, max_qty) ON p.sku = v.sku AND p.tenant_id = 'demo'
ON CONFLICT (tenant_id, product_id) DO NOTHING;

-- Clientes demo
INSERT INTO customers (tenant_id, name, phone, whatsapp, customer_type, city, state) VALUES
    ('demo', 'Roberto Almeida',    '(11) 98888-0001', '5511988880001', 'empreiteiro', 'São Paulo', 'SP'),
    ('demo', 'Construtora Silva',  '(11) 98888-0002', '5511988880002', 'construtora', 'Guarulhos', 'SP'),
    ('demo', 'Maria Santos',       '(11) 98888-0003', '5511988880003', 'varejo',      'São Paulo', 'SP'),
    ('demo', 'José Pereira',       '(11) 98888-0004', '5511988880004', 'varejo',      'Osasco',    'SP'),
    ('demo', 'Reformas Rapidas ME','(11) 98888-0005', '5511988880005', 'empreiteiro', 'ABC',       'SP')
ON CONFLICT DO NOTHING;

-- Vendas dos últimos 30 dias (simuladas)
WITH inserted_orders AS (
    INSERT INTO orders (tenant_id, customer_id, order_number, status, order_date, subtotal, discount, total)
    SELECT
        'demo',
        c.id,
        'PED-' || LPAD((ROW_NUMBER() OVER ())::text, 5, '0'),
        'faturado',
        CURRENT_DATE - (random() * 30)::int,
        total_val,
        0,
        total_val
    FROM customers c
    CROSS JOIN (VALUES (850.00), (1200.00), (430.00), (2100.00), (680.00)) AS t(total_val)
    WHERE c.tenant_id = 'demo'
    ON CONFLICT DO NOTHING
    RETURNING id, customer_id, total
)
SELECT 1;  -- placeholder — itens seriam inseridos com referência aos IDs gerados
