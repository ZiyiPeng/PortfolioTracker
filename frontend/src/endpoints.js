export const Action = {
    Login: '/api/login',
    Register: '/api/register',
}

export const getUrl = (action) => {
    const base_url = 'http://localhost:5000'
    return `${base_url}${action}`
}