function PageHeader({ title, description }) {
  return (
    <div className="mb-6">
      <h1 className="text-3xl font-semibold text-slate-950">{title}</h1>
      {description ? (
        <p className="mt-2 max-w-2xl text-slate-600">{description}</p>
      ) : null}
    </div>
  )
}

export default PageHeader
