/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      // LOCAL DEV
      { protocol: 'http', hostname: '127.0.0.1', port: '8001', pathname: '/media/**' },
      { protocol: 'http', hostname: 'localhost', port: '8001', pathname: '/media/**' },
      
      // PRODUCTION (PythonAnywhere)
      { protocol: 'https', hostname: 'justpythonindia.pythonanywhere.com', pathname: '/media/**' },
      
      // VERCEL PREVIEW & PRODUCTION
      { protocol: 'https', hostname: '**' }, 
    ],
  },
  // REMOVE: basePath and assetPrefix. 
  // Vercel handles these automatically. If you leave them as '', 
  // it can cause the 404: NOT_FOUND error on your homepage.

  trailingSlash: false,
}

module.exports = nextConfig