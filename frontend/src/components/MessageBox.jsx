const styles = {
  error: 'border-red-200 bg-red-50 text-red-800',
  success: 'border-emerald-200 bg-emerald-50 text-emerald-800',
  info: 'border-slate-200 bg-white text-slate-700',
}

function MessageBox({ type = 'info', children }) {
  if (!children) return null

  return (
    <div className={`rounded-md border px-4 py-3 text-sm ${styles[type] || styles.info}`}>
      {children}
    </div>
  )
}

export default MessageBox
