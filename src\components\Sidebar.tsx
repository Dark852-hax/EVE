import { SidebarView } from '../types';

interface SidebarProps {
  currentView: SidebarView;
  onViewChange: (view: SidebarView) => void;
}

const Sidebar = ({ currentView, onViewChange }: SidebarProps) => {
  const menuItems: { id: SidebarView; icon: string; label: string }[] = [
    { id: 'chat', icon: '💬', label: 'Chat' },
    { id: 'tools', icon: '🛠️', label: 'Tools' },
    { id: 'memory', icon: '🧠', label: 'Memory' },
    { id: 'settings', icon: '⚙️', label: 'Settings' },
  ];

  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${currentView === item.id ? 'active' : ''}`}
            onClick={() => onViewChange(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </button>
        ))}
      </nav>
      
      <div className="sidebar-footer">
        <div className="eve-status">
          <span className="status-dot"></span>
          <span className="status-text">EVE Online</span>
        </div>
      </div>

      <style>{`
        .sidebar {
          width: var(--sidebar-width);
          background: var(--bg-secondary);
          border-right: 1px solid var(--border);
          display: flex;
          flex-direction: column;
          flex-shrink: 0;
        }

        .sidebar-nav {
          flex: 1;
          padding: var(--space-md);
          display: flex;
          flex-direction: column;
          gap: var(--space-xs);
        }

        .nav-item {
          display: flex;
          align-items: center;
          gap: var(--space-md);
          padding: var(--space-sm) var(--space-md);
          border-radius: 8px;
          color: var(--text-secondary);
          transition: all var(--transition);
          text-align: left;
        }

        .nav-item:hover {
          background: var(--bg-tertiary);
          color: var(--text-primary);
        }

        .nav-item.active {
          background: rgba(0, 212, 170, 0.1);
          color: var(--accent-primary);
          box-shadow: var(--shadow-glow);
        }

        .nav-icon {
          font-size: 18px;
          width: 24px;
          text-align: center;
        }

        .nav-label {
          font-size: 14px;
          font-weight: 500;
        }

        .sidebar-footer {
          padding: var(--space-md);
          border-top: 1px solid var(--border);
        }

        .eve-status {
          display: flex;
          align-items: center;
          gap: var(--space-sm);
          padding: var(--space-sm);
          border-radius: 8px;
          background: var(--bg-tertiary);
        }

        .status-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: var(--success);
          box-shadow: 0 0 8px var(--success);
          animation: pulse 2s ease-in-out infinite;
        }

        .status-text {
          font-size: 12px;
          color: var(--text-secondary);
        }
      `}</style>
    </aside>
  );
};

export default Sidebar;
