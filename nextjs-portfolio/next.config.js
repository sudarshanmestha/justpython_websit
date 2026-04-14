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
  // REMOVED basePath and assetPrefix. 
  // Vercel handles these automatically. Setting them to '' can 
  // break the internal routing manifest on the Edge Network.
  
  trailingSlash: false,
}

module.exports = nextConfig