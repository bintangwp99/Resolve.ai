import { Link, useLocation } from 'react-router-dom';
import { Activity, MessageSquare, Settings, Users, LogOut } from 'lucide-react';

export default function Navbar({ isAdmin }: { isAdmin: boolean }) {
  const location = useLocation();

  const navItems = [
    { name: 'Incidents', path: '/incidents', icon: Activity },
    { name: 'Ask Resolve.ai', path: '/ask', icon: MessageSquare },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  if (isAdmin) {
    navItems.push({ name: 'Users', path: '/admin/users', icon: Users });
  }

  return (
    <nav className="border-b border-border bg-card shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-8">
            <div className="flex-shrink-0 font-bold text-xl text-primary flex items-center gap-2">
              <Activity className="h-6 w-6" /> Resolve.ai
            </div>
            <div className="hidden md:block">
              <div className="flex items-baseline space-x-4">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  const isActive = location.pathname.startsWith(item.path);
                  return (
                    <Link
                      key={item.name}
                      to={item.path}
                      className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-all ${
                        isActive
                          ? 'bg-primary/10 text-primary'
                          : 'text-muted-foreground hover:bg-secondary hover:text-foreground'
                      }`}
                    >
                      <Icon className="h-4 w-4" />
                      {item.name}
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>
          <div className="flex items-center">
            <button className="flex items-center gap-2 text-muted-foreground hover:text-destructive px-3 py-2 rounded-md text-sm font-medium transition-colors">
              <LogOut className="h-4 w-4" />
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
