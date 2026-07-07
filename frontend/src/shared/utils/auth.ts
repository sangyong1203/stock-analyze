const AUTH_STORAGE_KEY = 'stock-analyze-authenticated'

export function isAuthenticated() {
  return localStorage.getItem(AUTH_STORAGE_KEY) === 'true'
}

export function setAuthenticated(value: boolean) {
  if (value) {
    localStorage.setItem(AUTH_STORAGE_KEY, 'true')
    return
  }

  localStorage.removeItem(AUTH_STORAGE_KEY)
}

export function clearAuthenticated() {
  localStorage.removeItem(AUTH_STORAGE_KEY)
}
