import type { ElementType } from 'react'
import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  MessageSquare,
  Package,
  FileText,
  Megaphone,
  BarChart3,
  Building2,
  User,
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface NavItem {
  label: string
  icon: ElementType
  to: string
}

const navItems: NavItem[] = [
  { label: 'Dashboard', icon: LayoutDashboard, to: '/' },
  { label: 'Chat', icon: MessageSquare, to: '/chat' },
  { label: 'Estoque', icon: Package, to: '/inventory' },
  { label: 'Projetos', icon: FileText, to: '/projects' },
  { label: 'Marketing', icon: Megaphone, to: '/marketing' },
  { label: 'Relatórios', icon: BarChart3, to: '/reports' },
]

interface SidebarProps {
  open: boolean
  onClose: () => void
}

export default function Sidebar({ open, onClose }: SidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {open && (
        <div
          className="fixed inset-0 z-20 bg-black/60 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed top-0 left-0 z-30 h-full w-64 flex flex-col bg-[#0f172a] border-r border-slate-800 transition-transform duration-300',
          'lg:static lg:z-auto lg:translate-x-0',
          open ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        {/* Brand */}
        <div className="flex items-center gap-3 px-6 py-6 border-b border-slate-800">
          <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-blue-600">
            <Building2 className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="text-white font-bold text-lg leading-none tracking-widest">
              JARVIS
            </p>
            <p className="text-slate-400 text-xs mt-0.5">
              Construção Intelligence
            </p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              onClick={onClose}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-blue-600/20 text-blue-400 border border-blue-600/30'
                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                )
              }
            >
              {({ isActive }) => (
                <>
                  <item.icon
                    className={cn(
                      'w-5 h-5 flex-shrink-0',
                      isActive ? 'text-blue-400' : 'text-slate-500'
                    )}
                  />
                  {item.label}
                </>
              )}
            </NavLink>
          ))}
        </nav>

        {/* Tenant info */}
        <div className="px-4 py-4 border-t border-slate-800">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-slate-700">
              <User className="w-4 h-4 text-slate-300" />
            </div>
            <div className="min-w-0">
              <p className="text-sm text-white font-medium truncate">
                Loja Demo
              </p>
              <p className="text-xs text-slate-500 truncate">tenant: demo</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
