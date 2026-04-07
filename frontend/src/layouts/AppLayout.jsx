import { Outlet } from 'react-router-dom'
import Navbar from '../components/Navbar'

function AppLayout() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <main className="mx-auto w-full max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
        <Outlet />
      </main>
    </div>
  )
}

export default AppLayout
