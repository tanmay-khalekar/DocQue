import { useState } from 'react'
import LoadingButton from '../components/LoadingButton'
import MessageBox from '../components/MessageBox'
import PageHeader from '../components/PageHeader'
import { askQuestion, getApiErrorMessage } from '../services/api'
import useDocumentTitle from '../hooks/useDocumentTitle'

function formatAnswer(data) {
  if (!data) return ''
  if (typeof data === 'string') return data
  return data.answer || data.response || data.message || JSON.stringify(data, null, 2)
}

function QueryPage() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useDocumentTitle('Ask')

  async function handleSubmit(event) {
    event.preventDefault()

    if (!question.trim()) {
      setErrorMessage('Please enter a question.')
      setAnswer('')
      return
    }

    setIsLoading(true)
    setErrorMessage('')
    setAnswer('')

    try {
      const data = await askQuestion(question.trim())
      setAnswer(formatAnswer(data))
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
      <PageHeader
        title="Ask a question"
        description="Enter a question about the uploaded document and submit it to the backend."
      />

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label htmlFor="question" className="block text-sm font-medium text-slate-700">
            Question
          </label>
          <textarea
            id="question"
            name="question"
            rows="4"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="What is this document about?"
            className="mt-2 block w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-800 shadow-sm focus:border-slate-500 focus:outline-none focus:ring-2 focus:ring-slate-200"
          />
        </div>

        <LoadingButton isLoading={isLoading} loadingText="Asking...">
          Submit question
        </LoadingButton>
      </form>

      <div className="mt-6 space-y-4">
        <MessageBox type="error">{errorMessage}</MessageBox>

        {answer ? (
          <div className="rounded-md border border-slate-200 bg-slate-50 p-4">
            <h2 className="text-sm font-semibold text-slate-950">Response</h2>
            <pre className="mt-2 whitespace-pre-wrap break-words text-sm leading-6 text-slate-700">
              {answer}
            </pre>
          </div>
        ) : null}
      </div>
    </section>
  )
}

export default QueryPage
