import { Link } from 'react-router-dom'
import PageHeader from '../components/PageHeader'
import useDocumentTitle from '../hooks/useDocumentTitle'

function NotFoundPage() {
  useDocumentTitle('Not found')

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
      <PageHeader
        title="Page not found"
        description="The page you are looking for is not available in DocQue."
      />

      <Link
        to="/"
        className="inline-flex rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
      >
        Go home
      </Link>
    </section>
  )
}

export default NotFoundPage
