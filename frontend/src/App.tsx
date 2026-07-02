import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import IncidentFeed from './pages/IncidentFeed';
import IncidentDetail from './pages/IncidentDetail';
import AskAIOps from './pages/AskAIOps';
import Settings from './pages/Settings';
import Login from './pages/Login';
import AdminUsers from './pages/AdminUsers';
import Navbar from './components/Navbar';

function App() {
  const isAuthenticated = true; // MVP placeholder
  const isAdmin = true;

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <Router>
      <div className="min-h-screen bg-background text-foreground flex flex-col font-sans">
        <Navbar isAdmin={isAdmin} />
        <main className="flex-1 p-6 max-w-7xl mx-auto w-full">
          <Routes>
            <Route path="/" element={<Navigate to="/incidents" />} />
            <Route path="/incidents" element={<IncidentFeed />} />
            <Route path="/incidents/:id" element={<IncidentDetail />} />
            <Route path="/ask" element={<AskAIOps />} />
            <Route path="/settings" element={<Settings />} />
            {isAdmin && <Route path="/admin/users" element={<AdminUsers />} />}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
