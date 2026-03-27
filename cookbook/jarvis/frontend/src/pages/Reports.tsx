import { useState } from 'react'
import { BarChart3, Loader2, Calendar } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { sendChatMessage } from '@/lib/api'

const WEEKLY_DATA = [
  { day: 'Seg', cimento: 1200, aco: 800, ceramica: 600, outros: 400 },
  { day: 'Ter', cimento: 900, aco: 1100, ceramica: 400, outros: 300 },
  { day: 'Qua', cimento: 1500, aco: 600, ceramica: 900, outros: 500 },
  { day: 'Qui', cimento: 800, aco: 900, ceramica: 700, outros: 600 },
  { day: 'Sex', cimento: 2100, aco: 1400, ceramica: 1100, outros: 800 },
  { day: 'Sáb', cimento: 1800, aco: 700, ceramica: 1300, outros: 700 },
]

export default function Reports() {
  const [startDate, setStartDate] = useState('2026-03-01')
  const [endDate, setEndDate] = useState('2026-03-27')
  const [report, setReport] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleGenerate() {
    setLoading(true)
    setReport('')
    try {
      const prompt = `Gere um relatório executivo de vendas do período de ${startDate} a ${endDate}. Inclua total de vendas, número de pedidos, ticket médio, top produtos e análise de tendências com recomendações para o gestor.`
      let accumulated = ''
      await sendChatMessage(prompt, 'demo', (chunk) => {
        accumulated += chunk
        setReport(accumulated)
      })
    } catch {
      setReport('Erro ao gerar relatório. Verifique se o Jarvis está rodando em localhost:7777.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Relatórios</h1>
        <p className="text-slate-400 text-sm">Análises executivas e inteligência de negócio</p>
      </div>

      {/* Date range + generate */}
      <Card className="bg-slate-800 border-slate-700">
        <CardContent className="p-4">
          <div className="flex flex-wrap items-end gap-4">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-slate-400" />
              <span className="text-sm text-slate-400">Período:</span>
            </div>
            <div>
              <label className="text-xs text-slate-500 block mb-1">De</label>
              <Input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="bg-slate-700 border-slate-600 text-white w-40"
              />
            </div>
            <div>
              <label className="text-xs text-slate-500 block mb-1">Até</label>
              <Input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="bg-slate-700 border-slate-600 text-white w-40"
              />
            </div>
            <Button
              onClick={handleGenerate}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-500 gap-2"
            >
              {loading ? (
                <><Loader2 className="w-4 h-4 animate-spin" /> Gerando...</>
              ) : (
                <><BarChart3 className="w-4 h-4" /> Gerar Relatório</>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Report output */}
      {report && (
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white text-base flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-blue-400" />
              Relatório Gerado pelo Jarvis
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-slate-200 text-sm whitespace-pre-wrap leading-relaxed max-h-[400px] overflow-y-auto">
              {report}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Chart */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white text-base">Vendas por Categoria — Última Semana</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={WEEKLY_DATA} margin={{ top: 4, right: 16, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="day" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} tickFormatter={(v) => `R$${(v/1000).toFixed(0)}k`} />
              <Tooltip
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                labelStyle={{ color: '#f1f5f9' }}
                formatter={(value: number) => [`R$ ${value.toLocaleString('pt-BR')}`, undefined]}
              />
              <Bar dataKey="cimento" name="Cimento" fill="#3b82f6" radius={[3, 3, 0, 0]} />
              <Bar dataKey="aco" name="Aço" fill="#8b5cf6" radius={[3, 3, 0, 0]} />
              <Bar dataKey="ceramica" name="Cerâmica" fill="#06b6d4" radius={[3, 3, 0, 0]} />
              <Bar dataKey="outros" name="Outros" fill="#64748b" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
