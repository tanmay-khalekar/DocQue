import { NavLink } from 'react-router-dom'

const navItems = [
  { label: 'Home', path: '/' },
  { label: 'Upload', path: '/upload' },
  { label: 'Ask', path: '/query' },
]

function Navbar() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <nav className="mx-auto flex w-full max-w-5xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
        <NavLink to="/" className="text-xl font-semibold text-slate-950">
          DocQue
        </NavLink>

        <div className="flex flex-wrap gap-2">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                [
                  'rounded-md px-3 py-2 text-sm font-medium transition',
                  isActive
                    ? 'bg-slate-900 text-white'
                    : 'text-slate-700 hover:bg-slate-100 hover:text-slate-950',
                ].join(' ')
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>
      </nav>
    </header>
  )
}

export default Navbar
