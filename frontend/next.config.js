/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",
    async rewrites() {
        const internalApiUrl = process.env.INTERNAL_API_URL || "http://localhost:8000/api"
        const base = internalApiUrl.replace(/\/$/, "")
        return [
            {
                source: '/api/:path*',
                destination: `${base}/:path*`,
            },
        ];
    },
};

module.exports = nextConfig;
