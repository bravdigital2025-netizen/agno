import { useState } from 'react'
import { FileText, Upload, Loader2, CheckCircle, Clock } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { sendChatMessage } from '@/lib/api'

interface RecentProject {
  id: string
  name: string
  date: string
  estimatedValue: number
  status: 'aprovado' | 'enviado' | 'rascunho'
}

const RECENT: RecentProject[] = [
  { id: '1', name: 'Casa Térrea 80m² — João Silva', date: '24/03/2026', estimatedValue: 48200, status: 'aprovado' },
  { id: '2', name: 'Reforma Banheiro — Maria Costa', date: '20/03/2026', estimatedValue: 6800, status: 'enviado' },
  { id: '3', name: 'Muro e Calçada — Roberto Almeida', date: '18/03/2026', estimatedValue: 12400, status: 'rascunho' },
]

const STATUS_STYLE = {
  aprovado: 'bg-green-500/20 text-green-400 border-green-500/30',
  enviado: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  rascunho: 'bg-slate-500/20 text-slate-400 border-slate-500/30',
}

export default function Projects() {
  const [projectName, setProjectName] = useState('')
  const [description, setDescription] = useState('')
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleGenerate() {
    if (!description.trim()) return
    setLoading(true)
    setResult('')
    try {
      const prompt = `Analise este projeto e gere um orçamento detalhado de materiais de construção.\n\nNome do projeto: ${projectName || 'Projeto sem nome'}\n\nDescrição:\n${description}`
      let accumulated = ''
      await sendChatMessage(prompt, 'demo', (chunk) => {
        accumulated += chunk
        setResult(accumulated)
      })
    } catch {
      setResult('Erro ao gerar orçamento. Verifique se o Jarvis está rodando em localhost:7777.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Projetos e Orçamentos</h1>
        <p className="text-slate-400 text-sm">Gere orçamentos de materiais a partir de plantas ou descrições</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* New Quote */}
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white text-base flex items-center gap-2">
              <FileText className="w-4 h-4 text-blue-400" />
              Novo Orçamento
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-xs text-slate-400 mb-1 block">Nome do projeto</label>
              <Input
                placeholder="Ex: Casa Térrea 80m²"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-500"
              />
            </div>

            <div>
              <label className="text-xs text-slate-400 mb-1 block">Descrição do projeto</label>
              <Textarea
                placeholder="Descreva o projeto: tipo de obra, área, cômodos, localização..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-500 min-h-[100px]"
              />
            </div>

            {/* File upload area (visual only) */}
            <div className="border-2 border-dashed border-slate-600 rounded-lg p-6 text-center hover:border-blue-500/50 transition-colors cursor-pointer">
              <Upload className="w-6 h-6 text-slate-400 mx-auto mb-2" />
              <p className="text-sm text-slate-400">Arraste uma planta baixa ou foto</p>
              <p className="text-xs text-slate-500 mt-1">JPG, PNG ou PDF — máx. 10MB</p>
            </div>

            <Button
              onClick={handleGenerate}
              disabled={!description.trim() || loading}
              className="w-full bg-blue-600 hover:bg-blue-500"
            >
              {loading ? (
                <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Gerando orçamento...</>
              ) : (
                'Gerar Orçamento via Jarvis'
              )}
            </Button>

            {result && (
              <div className="bg-slate-700/50 rounded-lg p-4 text-sm text-slate-200 whitespace-pre-wrap max-h-[300px] overflow-y-auto">
                {result}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Recent projects */}
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white text-base flex items-center gap-2">
              <Clock className="w-4 h-4 text-blue-400" />
              Orçamentos Recentes
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {RECENT.map((p) => (
              <div key={p.id} className="bg-slate-700/50 rounded-lg p-4 flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <p className="text-white text-sm font-medium truncate">{p.name}</p>
                  <p className="text-slate-400 text-xs mt-1">{p.date}</p>
                  <p className="text-blue-400 text-sm font-semibold mt-1">
                    R$ {p.estimatedValue.toLocaleString('pt-BR')}
                  </p>
                </div>
                <Badge variant="outline" className={STATUS_STYLE[p.status]}>
                  {p.status}
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
