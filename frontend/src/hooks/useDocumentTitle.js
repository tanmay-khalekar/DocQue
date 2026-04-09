import { useEffect } from 'react'

function useDocumentTitle(title) {
  useEffect(() => {
    document.title = title ? `${title} | DocQue` : 'DocQue'
  }, [title])
}

export default useDocumentTitle
