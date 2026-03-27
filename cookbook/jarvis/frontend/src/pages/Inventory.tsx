import { useState } from 'react'
import { Search, Package, AlertTriangle, TrendingDown } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'

interface Product {
  sku: string
  name: string
  unit: string
  currentQty: number
  minQty: number
  supplier: string
}

const PRODUCTS: Product[] = [
  { sku: 'CIM-001', name: 'Cimento CP II-E-32 50kg', unit: 'sc', currentQty: 120, minQty: 100, supplier: 'Votorantim' },
  { sku: 'CIM-002', name: 'Cimento CP III 50kg', unit: 'sc', currentQty: 45, minQty: 100, supplier: 'Itambé' },
  { sku: 'ARG-001', name: 'Argamassa ACII 20kg', unit: 'sc', currentQty: 200, minQty: 80, supplier: 'Votorantim' },
  { sku: 'AGR-001', name: 'Areia Média', unit: 'm³', currentQty: 15, minQty: 20, supplier: '-' },
  { sku: 'AGR-002', name: 'Brita 1', unit: 'm³', currentQty: 25, minQty: 20, supplier: '-' },
  { sku: 'ALV-001', name: 'Tijolo Cerâmico 9x19x19 cx100', unit: 'cx', currentQty: 18, minQty: 20, supplier: '-' },
  { sku: 'ALV-002', name: 'Bloco de Concreto 14x19x39', unit: 'un', currentQty: 850, minQty: 500, supplier: '-' },
  { sku: 'ACO-001', name: 'Aço CA-50 10mm barra 12m', unit: 'un', currentQty: 55, minQty: 30, supplier: 'CSN' },
  { sku: 'ACO-002', name: 'Aço CA-50 8mm barra 12m', unit: 'un', currentQty: 28, minQty: 30, supplier: 'CSN' },
  { sku: 'CER-001', name: 'Porcelanato 60x60 Bege', unit: 'm²', currentQty: 120, minQty: 60, supplier: 'Portobello' },
  { sku: 'CER-002', name: 'Cerâmica 45x45', unit: 'm²', currentQty: 210, minQty: 80, supplier: 'Portobello' },
  { sku: 'COB-001', name: 'Telha Fibrocimento 2,44m', unit: 'un', currentQty: 80, minQty: 40, supplier: '-' },
  { sku: 'TIN-001', name: 'Tinta Látex Branca 18L', unit: 'gl', currentQty: 22, minQty: 20, supplier: '-' },
  { sku: 'HID-001', name: 'Tubo PVC Esgoto 100mm 6m', unit: 'un', currentQty: 45, minQty: 30, supplier: '-' },
]

function getStatus(current: number, min: number): 'critical' | 'warning' | 'ok' {
  if (current <= min) return 'critical'
  if (current <= min * 1.3) return 'warning'
  return 'ok'
}

const STATUS_CONFIG = {
  critical: { label: 'Crítico', className: 'bg-red-500/20 text-red-400 border-red-500/30' },
  warning: { label: 'Atenção', className: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30' },
  ok: { label: 'OK', className: 'bg-green-500/20 text-green-400 border-green-500/30' },
}

export default function Inventory() {
  const [search, setSearch] = useState('')

  const filtered = PRODUCTS.filter(
    (p) =>
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      p.sku.toLowerCase().includes(search.toLowerCase())
  )

  const critical = PRODUCTS.filter((p) => getStatus(p.currentQty, p.minQty) === 'critical').length
  const totalValue = PRODUCTS.reduce((sum, p) => sum + p.currentQty * 36.5, 0)

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Controle de Estoque</h1>
        <p className="text-slate-400 text-sm">Monitoramento em tempo real dos produtos</p>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-3 gap-4">
        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="p-4 flex items-center gap-3">
            <Package className="w-8 h-8 text-blue-400" />
            <div>
              <p className="text-2xl font-bold text-white">{PRODUCTS.length}</p>
              <p className="text-xs text-slate-400">Total de SKUs</p>
            </div>
          </CardContent>
        </Card>
        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="p-4 flex items-center gap-3">
            <AlertTriangle className="w-8 h-8 text-red-400" />
            <div>
              <p className="text-2xl font-bold text-red-400">{critical}</p>
              <p className="text-xs text-slate-400">Em estado crítico</p>
            </div>
          </CardContent>
        </Card>
        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="p-4 flex items-center gap-3">
            <TrendingDown className="w-8 h-8 text-green-400" />
            <div>
              <p className="text-2xl font-bold text-white">
                R$ {(totalValue / 1000).toFixed(0)}k
              </p>
              <p className="text-xs text-slate-400">Valor em estoque</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
        <Input
          placeholder="Buscar produto ou SKU..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="pl-9 bg-slate-800 border-slate-700 text-white placeholder:text-slate-500"
        />
      </div>

      {/* Table */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader className="pb-2">
          <CardTitle className="text-white text-base">{filtered.length} produtos</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-left px-4 py-3 text-slate-400 font-medium">SKU</th>
                  <th className="text-left px-4 py-3 text-slate-400 font-medium">Produto</th>
                  <th className="text-center px-4 py-3 text-slate-400 font-medium">Un.</th>
                  <th className="text-right px-4 py-3 text-slate-400 font-medium">Qtd Atual</th>
                  <th className="text-right px-4 py-3 text-slate-400 font-medium">Mínimo</th>
                  <th className="text-center px-4 py-3 text-slate-400 font-medium">Status</th>
                  <th className="text-left px-4 py-3 text-slate-400 font-medium">Fornecedor</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((p) => {
                  const status = getStatus(p.currentQty, p.minQty)
                  const cfg = STATUS_CONFIG[status]
                  return (
                    <tr key={p.sku} className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors">
                      <td className="px-4 py-3 text-slate-400 font-mono text-xs">{p.sku}</td>
                      <td className="px-4 py-3 text-white">{p.name}</td>
                      <td className="px-4 py-3 text-slate-400 text-center">{p.unit}</td>
                      <td className={`px-4 py-3 text-right font-medium ${status === 'critical' ? 'text-red-400' : 'text-white'}`}>
                        {p.currentQty.toLocaleString('pt-BR')}
                      </td>
                      <td className="px-4 py-3 text-right text-slate-400">{p.minQty.toLocaleString('pt-BR')}</td>
                      <td className="px-4 py-3 text-center">
                        <Badge variant="outline" className={cfg.className}>{cfg.label}</Badge>
                      </td>
                      <td className="px-4 py-3 text-slate-400">{p.supplier}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
