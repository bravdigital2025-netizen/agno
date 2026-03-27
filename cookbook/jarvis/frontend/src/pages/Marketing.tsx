import { Plus, MessageSquare, Instagram, Facebook, Mail, Eye, Send, Edit } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

interface Campaign {
  id: string
  name: string
  channel: 'whatsapp' | 'instagram' | 'facebook' | 'email'
  status: 'rascunho' | 'agendada' | 'em_execucao' | 'concluida'
  scheduledDate: string
  contacts: number
  delivered?: number
  read?: number
}

const CAMPAIGNS: Campaign[] = [
  { id: '1', name: 'Promoção Cimento — Maio', channel: 'whatsapp', status: 'agendada', scheduledDate: '15/04/2026', contacts: 234 },
  { id: '2', name: 'Semana do Empreiteiro', channel: 'whatsapp', status: 'concluida', scheduledDate: '08/04/2026', contacts: 89, delivered: 81, read: 64 },
  { id: '3', name: 'Black Friday Antecipada', channel: 'instagram', status: 'rascunho', scheduledDate: '—', contacts: 0 },
  { id: '4', name: 'Reativação Clientes Inativos', channel: 'whatsapp', status: 'em_execucao', scheduledDate: '27/03/2026', contacts: 156, delivered: 98 },
  { id: '5', name: 'Newsletter Abril', channel: 'email', status: 'agendada', scheduledDate: '01/04/2026', contacts: 420 },
]

const STATUS_STYLE: Record<Campaign['status'], string> = {
  rascunho: 'bg-slate-500/20 text-slate-400 border-slate-500/30',
  agendada: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  em_execucao: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  concluida: 'bg-green-500/20 text-green-400 border-green-500/30',
}

const STATUS_LABEL: Record<Campaign['status'], string> = {
  rascunho: 'Rascunho',
  agendada: 'Agendada',
  em_execucao: 'Em execução',
  concluida: 'Concluída',
}

const CHANNEL_ICON: Record<Campaign['channel'], React.ElementType> = {
  whatsapp: MessageSquare,
  instagram: Instagram,
  facebook: Facebook,
  email: Mail,
}

const CHANNEL_COLOR: Record<Campaign['channel'], string> = {
  whatsapp: 'text-green-400',
  instagram: 'text-pink-400',
  facebook: 'text-blue-400',
  email: 'text-yellow-400',
}

export default function Marketing() {
  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Marketing e Campanhas</h1>
          <p className="text-slate-400 text-sm">Gerencie campanhas e comunicações com clientes</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-500 gap-2">
          <Plus className="w-4 h-4" />
          Nova Campanha
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Total de campanhas', value: '5', color: 'text-white' },
          { label: 'Ativas agora', value: '1', color: 'text-yellow-400' },
          { label: 'Agendadas', value: '2', color: 'text-blue-400' },
          { label: 'Concluídas este mês', value: '1', color: 'text-green-400' },
        ].map((s) => (
          <Card key={s.label} className="bg-slate-800 border-slate-700">
            <CardContent className="p-4">
              <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
              <p className="text-xs text-slate-400 mt-1">{s.label}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Campaigns list */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white text-base">Todas as campanhas</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-left px-4 py-3 text-slate-400 font-medium">Campanha</th>
                  <th className="text-center px-4 py-3 text-slate-400 font-medium">Canal</th>
                  <th className="text-center px-4 py-3 text-slate-400 font-medium">Status</th>
                  <th className="text-center px-4 py-3 text-slate-400 font-medium">Data</th>
                  <th className="text-right px-4 py-3 text-slate-400 font-medium">Contatos</th>
                  <th className="text-right px-4 py-3 text-slate-400 font-medium">Entregues</th>
                  <th className="text-right px-4 py-3 text-slate-400 font-medium">Lidos</th>
                  <th className="px-4 py-3" />
                </tr>
              </thead>
              <tbody>
                {CAMPAIGNS.map((c) => {
                  const Icon = CHANNEL_ICON[c.channel]
                  return (
                    <tr key={c.id} className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors">
                      <td className="px-4 py-3 text-white font-medium">{c.name}</td>
                      <td className="px-4 py-3 text-center">
                        <Icon className={`w-4 h-4 mx-auto ${CHANNEL_COLOR[c.channel]}`} />
                      </td>
                      <td className="px-4 py-3 text-center">
                        <Badge variant="outline" className={STATUS_STYLE[c.status]}>
                          {STATUS_LABEL[c.status]}
                        </Badge>
                      </td>
                      <td className="px-4 py-3 text-center text-slate-400">{c.scheduledDate}</td>
                      <td className="px-4 py-3 text-right text-white">{c.contacts > 0 ? c.contacts : '—'}</td>
                      <td className="px-4 py-3 text-right text-slate-400">
                        {c.delivered != null ? `${Math.round((c.delivered / c.contacts) * 100)}%` : '—'}
                      </td>
                      <td className="px-4 py-3 text-right text-slate-400">
                        {c.read != null ? `${Math.round((c.read / c.contacts) * 100)}%` : '—'}
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-1 justify-end">
                          <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-slate-400 hover:text-white">
                            <Edit className="w-3.5 h-3.5" />
                          </Button>
                          {c.status === 'agendada' && (
                            <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-slate-400 hover:text-green-400">
                              <Send className="w-3.5 h-3.5" />
                            </Button>
                          )}
                          {c.status === 'concluida' && (
                            <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-slate-400 hover:text-blue-400">
                              <Eye className="w-3.5 h-3.5" />
                            </Button>
                          )}
                        </div>
                      </td>
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
