import type { ElementType } from 'react'
import {
  TrendingUp,
  TrendingDown,
  ShoppingCart,
  AlertTriangle,
  Receipt,
  AlertCircle,
  Calendar,
  CheckCircle,
} from 'lucide-react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const salesData = [
  { dia: 'Seg', vendas: 3200 },
  { dia: 'Ter', vendas: 4100 },
  { dia: 'Qua', vendas: 2800 },
  { dia: 'Qui', vendas: 5300 },
  { dia: 'Sex', vendas: 4700 },
  { dia: 'Sáb', vendas: 6200 },
  { dia: 'Dom', vendas: 4820 },
]

interface MetricCardProps {
  title: string
  value: string
  change: string
  changeType: 'positive' | 'negative' | 'neutral'
  icon: ElementType
  iconColor: string
}

function MetricCard({
  title,
  value,
  change,
  changeType,
  icon: Icon,
  iconColor,
}: MetricCardProps) {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm text-slate-400 font-medium">{title}</p>
            <p className="text-2xl font-bold text-white mt-1">{value}</p>
            <div className="flex items-center gap-1 mt-2">
              {changeType === 'positive' && (
                <TrendingUp className="w-4 h-4 text-green-400" />
              )}
              {changeType === 'negative' && (
                <TrendingDown className="w-4 h-4 text-red-400" />
              )}
              <span
                className={
                  changeType === 'positive'
                    ? 'text-green-400 text-sm'
                    : changeType === 'negative'
                      ? 'text-red-400 text-sm'
                      : 'text-slate-400 text-sm'
                }
              >
                {change}
              </span>
            </div>
          </div>
          <div
            className={`flex items-center justify-center w-12 h-12 rounded-lg ${iconColor}`}
          >
            <Icon className="w-6 h-6 text-white" />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

interface Alert {
  id: number
  title: string
  description: string
  type: 'danger' | 'warning' | 'success'
  icon: ElementType
  time: string
}

const alerts: Alert[] = [
  {
    id: 1,
    title: 'Estoque Crítico',
    description: 'Cimento CP II abaixo do mínimo — apenas 12 sacos restantes.',
    type: 'danger',
    icon: AlertTriangle,
    time: '10 min atrás',
  },
  {
    id: 2,
    title: 'Campanha Agendada',
    description: 'Promoção de Cimento programada para disparar hoje às 14h.',
    type: 'warning',
    icon: Calendar,
    time: '2 h atrás',
  },
  {
    id: 3,
    title: 'Pedido Confirmado',
    description: 'Pedido #2847 de R$ 1.240 confirmado — Empreiteira Santos.',
    type: 'success',
    icon: CheckCircle,
    time: '3 h atrás',
  },
  {
    id: 4,
    title: 'Atenção ao Estoque',
    description: 'Brita Graduada #1 próxima do mínimo — 8 m³ disponíveis.',
    type: 'warning',
    icon: AlertCircle,
    time: '5 h atrás',
  },
]

const alertVariantMap = {
  danger: 'danger' as const,
  warning: 'warning' as const,
  success: 'success' as const,
}

const alertLabelMap = {
  danger: 'Crítico',
  warning: 'Atenção',
  success: 'OK',
}

interface CustomTooltipProps {
  active?: boolean
  payload?: Array<{ value: number }>
  label?: string
}

function CustomTooltip({ active, payload, label }: CustomTooltipProps) {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-700 border border-slate-600 rounded-lg px-3 py-2">
        <p className="text-slate-300 text-xs">{label}</p>
        <p className="text-white font-semibold text-sm">
          R$ {payload[0].value.toLocaleString('pt-BR')}
        </p>
      </div>
    )
  }
  return null
}

export default function Dashboard() {
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-slate-400 text-sm mt-1">
          Visão geral do dia — {new Date().toLocaleDateString('pt-BR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </p>
      </div>

      {/* Metric cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <MetricCard
          title="Vendas Hoje"
          value="R$ 4.820"
          change="+12% vs ontem"
          changeType="positive"
          icon={TrendingUp}
          iconColor="bg-green-600"
        />
        <MetricCard
          title="Pedidos Hoje"
          value="23"
          change="+3 vs ontem"
          changeType="positive"
          icon={ShoppingCart}
          iconColor="bg-blue-600"
        />
        <MetricCard
          title="Estoque Crítico"
          value="4 produtos"
          change="Requer atenção"
          changeType="negative"
          icon={AlertTriangle}
          iconColor="bg-red-600"
        />
        <MetricCard
          title="Ticket Médio"
          value="R$ 209"
          change="+5% vs ontem"
          changeType="positive"
          icon={Receipt}
          iconColor="bg-purple-600"
        />
      </div>

      {/* Alerts and chart */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Alerts */}
        <Card>
          <CardHeader className="pb-4">
            <CardTitle className="text-white text-base">
              Alertas Jarvis
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {alerts.map((alert) => {
              const Icon = alert.icon
              return (
                <div
                  key={alert.id}
                  className="flex items-start gap-3 p-3 rounded-lg bg-slate-900/60 border border-slate-700"
                >
                  <div
                    className={`flex-shrink-0 mt-0.5 ${
                      alert.type === 'danger'
                        ? 'text-red-400'
                        : alert.type === 'warning'
                          ? 'text-yellow-400'
                          : 'text-green-400'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <p className="text-sm font-medium text-white">
                        {alert.title}
                      </p>
                      <Badge variant={alertVariantMap[alert.type]}>
                        {alertLabelMap[alert.type]}
                      </Badge>
                    </div>
                    <p className="text-xs text-slate-400 mt-0.5 leading-relaxed">
                      {alert.description}
                    </p>
                    <p className="text-xs text-slate-600 mt-1">{alert.time}</p>
                  </div>
                </div>
              )
            })}
          </CardContent>
        </Card>

        {/* Sales chart */}
        <Card>
          <CardHeader className="pb-4">
            <CardTitle className="text-white text-base">
              Vendas dos últimos 7 dias
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={salesData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#334155"
                  vertical={false}
                />
                <XAxis
                  dataKey="dia"
                  tick={{ fill: '#94a3b8', fontSize: 12 }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fill: '#94a3b8', fontSize: 12 }}
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={(v) => `R$${(v / 1000).toFixed(0)}k`}
                />
                <Tooltip content={<CustomTooltip />} />
                <Line
                  type="monotone"
                  dataKey="vendas"
                  stroke="#3b82f6"
                  strokeWidth={2.5}
                  dot={{ fill: '#3b82f6', r: 4, strokeWidth: 0 }}
                  activeDot={{ r: 6, fill: '#60a5fa' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
