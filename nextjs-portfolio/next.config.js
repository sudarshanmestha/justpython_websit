/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'http', hostname: '127.0.0.1', port: '8001', pathname: '/media/**' },
      { protocol: 'http', hostname: 'localhost', port: '8001', pathname: '/media/**' },
      { protocol: 'https', hostname: 'justpythonindia.pythonanywhere.com', pathname: '/media/**' },
      { protocol: 'https', hostname: '**' }, 
    ],
  },
  // REMOVED basePath and assetPrefix. 
  // Let Vercel handle the defaults. 
  trailingSlash: false,
}

module.exports = nextConfig