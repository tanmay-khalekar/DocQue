import { useState } from 'react'
import LoadingButton from '../components/LoadingButton'
import MessageBox from '../components/MessageBox'
import PageHeader from '../components/PageHeader'
import { getApiErrorMessage, uploadDocument } from '../services/api'
import useDocumentTitle from '../hooks/useDocumentTitle'

function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('info')

  useDocumentTitle('Upload')

  function handleFileChange(event) {
    setSelectedFile(event.target.files?.[0] || null)
    setMessage('')
  }

  async function handleSubmit(event) {
    event.preventDefault()

    if (!selectedFile) {
      setMessageType('error')
      setMessage('Please choose a document before uploading.')
      return
    }

    setIsLoading(true)
    setMessage('')

    try {
      const data = await uploadDocument(selectedFile)
      setMessageType('success')
      setMessage(data?.message || 'Document uploaded successfully.')
    } catch (error) {
      setMessageType('error')
      setMessage(getApiErrorMessage(error))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
      <PageHeader
        title="Upload document"
        description="Choose a document and send it to the backend for processing."
      />

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label htmlFor="document" className="block text-sm font-medium text-slate-700">
            Document file
          </label>
          <input
            id="document"
            name="document"
            type="file"
            onChange={handleFileChange}
            className="mt-2 block w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 file:mr-4 file:rounded-md file:border-0 file:bg-slate-100 file:px-3 file:py-2 file:text-sm file:font-medium file:text-slate-700 hover:file:bg-slate-200"
          />
          {selectedFile ? (
            <p className="mt-2 text-sm text-slate-500">Selected: {selectedFile.name}</p>
          ) : null}
        </div>

        <LoadingButton isLoading={isLoading} loadingText="Uploading...">
          Upload
        </LoadingButton>

        <MessageBox type={messageType}>{message}</MessageBox>
      </form>
    </section>
  )
}

export default UploadPage
