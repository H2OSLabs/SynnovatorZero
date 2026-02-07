/**
 * Runtime environment configuration
 *
 * This module provides a unified way to access environment variables
 * that works in both server and client contexts.
 *
 * Server-side: Reads from process.env (populated by .env files or Docker)
 * Client-side: Reads from window.__ENV__ (injected by layout.tsx)
 */

export interface EnvConfig {
  API_URL: string
}

// Default values (fallback if nothing is configured)
const defaults: EnvConfig = {
  API_URL: '/api',
}

function isAbsoluteUrl(url: string): boolean {
  return /^https?:\/\//i.test(url)
}

function resolveServerApiUrl(configured: string): string {
  if (isAbsoluteUrl(configured)) return configured
  if (process.env.INTERNAL_API_URL) return process.env.INTERNAL_API_URL

  const origin = process.env.SITE_ORIGIN || process.env.NEXT_PUBLIC_SITE_ORIGIN
  if (origin) return `${origin}${configured}`

  return `http://localhost:8000${configured}`
}

/**
 * Get server-side environment config
 * Only call this in server components or API routes
 */
export function getServerEnv(): EnvConfig {
  const configured = process.env.API_URL || defaults.API_URL
  return {
    API_URL: resolveServerApiUrl(configured),
  }
}

export function getPublicServerEnv(): EnvConfig {
  return {
    API_URL: process.env.API_URL || defaults.API_URL,
  }
}

/**
 * Get client-side environment config
 * Safe to call in client components
 */
export function getClientEnv(): EnvConfig {
  if (typeof window !== 'undefined' && window.__ENV__) {
    return window.__ENV__
  }
  // Fallback for SSR or when window.__ENV__ is not yet available
  return defaults
}

/**
 * Get environment config (auto-detects context)
 */
export function getEnv(): EnvConfig {
  if (typeof window === 'undefined') {
    return getServerEnv()
  }
  return getClientEnv()
}

// Type declaration for window.__ENV__
declare global {
  interface Window {
    __ENV__?: EnvConfig
  }
}
