function LoadingButton({ isLoading, loadingText = 'Working...', children, ...props }) {
  return (
    <button
      {...props}
      disabled={isLoading || props.disabled}
      className={[
        'inline-flex items-center justify-center rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition',
        'hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2',
        'disabled:cursor-not-allowed disabled:bg-slate-400',
        props.className || '',
      ].join(' ')}
    >
      {isLoading ? loadingText : children}
    </button>
  )
}

export default LoadingButton
