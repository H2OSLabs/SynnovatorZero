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

/**
 * Get server-side environment config
 * Only call this in server components or API routes
 */
export function getServerEnv(): EnvConfig {
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
