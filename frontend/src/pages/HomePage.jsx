import { Link } from 'react-router-dom'
import PageHeader from '../components/PageHeader'
import useDocumentTitle from '../hooks/useDocumentTitle'

function HomePage() {
  useDocumentTitle('Home')

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
      <PageHeader
        title="Ask questions from your documents"
        description="Upload a document, then ask DocQue for focused answers from the backend."
      />

      <div className="grid gap-4 sm:grid-cols-2">
        <Link
          to="/upload"
          className="rounded-md border border-slate-200 p-5 transition hover:border-slate-300 hover:bg-slate-50"
        >
          <h2 className="text-lg font-semibold text-slate-950">Upload document</h2>
          <p className="mt-2 text-sm text-slate-600">
            Send a PDF, text file, or supported document to the backend.
          </p>
        </Link>

        <Link
          to="/query"
          className="rounded-md border border-slate-200 p-5 transition hover:border-slate-300 hover:bg-slate-50"
        >
          <h2 className="text-lg font-semibold text-slate-950">Ask a question</h2>
          <p className="mt-2 text-sm text-slate-600">
            Submit a question and view the answer returned by the API.
          </p>
        </Link>
      </div>
    </section>
  )
}

export default HomePage
