'use client'

import * as React from 'react'
import { useRouter } from 'next/navigation'
import { UserIcon, FolderIcon, FileTextIcon } from 'lucide-react'
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from '@/components/ui/command'
import { searchAll, SearchResult } from '@/lib/search-api'

interface SearchModalProps {
  /** Default open state */
  defaultOpen?: boolean
  /** Callback when open state changes */
  onOpenChange?: (open: boolean) => void
}

export function SearchModal({ defaultOpen = false, onOpenChange }: SearchModalProps) {
  const [open, setOpen] = React.useState(defaultOpen)
  const [query, setQuery] = React.useState('')
  const [results, setResults] = React.useState<{
    users: SearchResult[]
    categories: SearchResult[]
    posts: SearchResult[]
  }>({ users: [], categories: [], posts: [] })
  const [isSearching, setIsSearching] = React.useState(false)
  const router = useRouter()
  const debounceRef = React.useRef<NodeJS.Timeout>()

  // Handle keyboard shortcut
  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen(prev => !prev)
      }
    }

    document.addEventListener('keydown', down)
    return () => document.removeEventListener('keydown', down)
  }, [])

  // Sync external open state
  React.useEffect(() => {
    if (defaultOpen !== open) {
      setOpen(defaultOpen)
    }
  }, [defaultOpen])

  // Handle open change
  const handleOpenChange = (newOpen: boolean) => {
    setOpen(newOpen)
    onOpenChange?.(newOpen)
    if (!newOpen) {
      setQuery('')
      setResults({ users: [], categories: [], posts: [] })
    }
  }

  // Debounced search
  React.useEffect(() => {
    if (debounceRef.current) {
      clearTimeout(debounceRef.current)
    }

    if (!query.trim()) {
      setResults({ users: [], categories: [], posts: [] })
      return
    }

    setIsSearching(true)
    debounceRef.current = setTimeout(async () => {
      try {
        const data = await searchAll(query)
        setResults(data)
      } catch (error) {
        console.error('Search error:', error)
        setResults({ users: [], categories: [], posts: [] })
      } finally {
        setIsSearching(false)
      }
    }, 300)

    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current)
      }
    }
  }, [query])

  const handleSelect = (result: SearchResult) => {
    router.push(result.url)
    handleOpenChange(false)
  }

  const hasResults =
    results.users.length > 0 ||
    results.categories.length > 0 ||
    results.posts.length > 0

  const getIcon = (type: SearchResult['type']) => {
    switch (type) {
      case 'user':
        return <UserIcon className="h-4 w-4 text-nf-muted" />
      case 'category':
        return <FolderIcon className="h-4 w-4 text-nf-muted" />
      case 'post':
        return <FileTextIcon className="h-4 w-4 text-nf-muted" />
    }
  }

  return (
    <CommandDialog
      open={open}
      onOpenChange={handleOpenChange}
      title="搜索"
      description="搜索用户、活动和作品"
      className="bg-nf-card-bg border-nf-dark-bg"
      showCloseButton={false}
    >
      <CommandInput
        placeholder="搜索用户、活动、作品..."
        value={query}
        onValueChange={setQuery}
        className="text-nf-white placeholder:text-nf-muted"
      />
      <CommandList className="text-nf-light-gray">
        {isSearching && (
          <div className="py-6 text-center text-sm text-nf-muted">
            搜索中...
          </div>
        )}

        {!isSearching && query && !hasResults && (
          <CommandEmpty className="text-nf-muted">
            未找到相关结果
          </CommandEmpty>
        )}

        {!isSearching && hasResults && (
          <>
            {results.users.length > 0 && (
              <CommandGroup heading="用户" className="text-nf-muted">
                {results.users.map(result => (
                  <CommandItem
                    key={`user-${result.id}`}
                    value={`user-${result.id}-${result.title}`}
                    onSelect={() => handleSelect(result)}
                    className="cursor-pointer hover:bg-nf-dark-bg data-[selected=true]:bg-nf-dark-bg data-[selected=true]:text-nf-lime"
                  >
                    {getIcon('user')}
                    <div className="flex flex-col">
                      <span>{result.title}</span>
                      {result.subtitle && (
                        <span className="text-xs text-nf-muted">{result.subtitle}</span>
                      )}
                    </div>
                  </CommandItem>
                ))}
              </CommandGroup>
            )}

            {results.users.length > 0 && results.categories.length > 0 && (
              <CommandSeparator className="bg-nf-dark-bg" />
            )}

            {results.categories.length > 0 && (
              <CommandGroup heading="活动" className="text-nf-muted">
                {results.categories.map(result => (
                  <CommandItem
                    key={`category-${result.id}`}
                    value={`category-${result.id}-${result.title}`}
                    onSelect={() => handleSelect(result)}
                    className="cursor-pointer hover:bg-nf-dark-bg data-[selected=true]:bg-nf-dark-bg data-[selected=true]:text-nf-lime"
                  >
                    {getIcon('category')}
                    <div className="flex flex-col">
                      <span>{result.title}</span>
                      {result.subtitle && (
                        <span className="text-xs text-nf-muted">{result.subtitle}</span>
                      )}
                    </div>
                  </CommandItem>
                ))}
              </CommandGroup>
            )}

            {(results.users.length > 0 || results.categories.length > 0) &&
              results.posts.length > 0 && (
              <CommandSeparator className="bg-nf-dark-bg" />
            )}

            {results.posts.length > 0 && (
              <CommandGroup heading="作品" className="text-nf-muted">
                {results.posts.map(result => (
                  <CommandItem
                    key={`post-${result.id}`}
                    value={`post-${result.id}-${result.title}`}
                    onSelect={() => handleSelect(result)}
                    className="cursor-pointer hover:bg-nf-dark-bg data-[selected=true]:bg-nf-dark-bg data-[selected=true]:text-nf-lime"
                  >
                    {getIcon('post')}
                    <div className="flex flex-col">
                      <span>{result.title}</span>
                      {result.subtitle && (
                        <span className="text-xs text-nf-muted">{result.subtitle}</span>
                      )}
                    </div>
                  </CommandItem>
                ))}
              </CommandGroup>
            )}
          </>
        )}

        {!query && (
          <div className="py-6 text-center text-sm text-nf-muted">
            输入关键词搜索用户、活动或作品
            <div className="mt-2 flex justify-center gap-2 text-xs">
              <kbd className="rounded bg-nf-dark-bg px-2 py-0.5">⌘K</kbd>
              <span>快速搜索</span>
            </div>
          </div>
        )}
      </CommandList>
    </CommandDialog>
  )
}

export default SearchModal
