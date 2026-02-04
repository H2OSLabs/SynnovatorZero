'use client'

import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { login as apiLogin, logout as apiLogout } from '@/lib/api-client'

export interface AuthUser {
  user_id: number
  username: string
  role: 'participant' | 'organizer' | 'admin'
}

interface AuthContextType {
  user: AuthUser | null
  isLoading: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
  isOrganizer: boolean
  isParticipant: boolean
  isAdmin: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

const STORAGE_KEY = 'synnovator_user'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Load user from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      try {
        setUser(JSON.parse(stored))
      } catch {
        localStorage.removeItem(STORAGE_KEY)
      }
    }
    setIsLoading(false)
  }, [])

  const login = async (username: string, password: string) => {
    const result = await apiLogin(username, password)
    const authUser: AuthUser = {
      user_id: result.user_id,
      username: result.username,
      role: result.role as AuthUser['role'],
    }
    setUser(authUser)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(authUser))
  }

  const logout = async () => {
    if (user) {
      try {
        await apiLogout(user.user_id)
      } catch {
        // Ignore logout errors
      }
    }
    setUser(null)
    localStorage.removeItem(STORAGE_KEY)
  }

  const value: AuthContextType = {
    user,
    isLoading,
    login,
    logout,
    isOrganizer: user?.role === 'organizer',
    isParticipant: user?.role === 'participant',
    isAdmin: user?.role === 'admin',
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
