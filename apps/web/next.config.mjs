/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  images: {
    unoptimized: true,
  },
  async headers() {
    // Turbopack이 매 배포마다 청크 파일명을 새로 뽑는데, 브라우저가 옛 HTML을
    // 휴리스틱 캐싱으로 오래 들고 있으면 사라진 옛 청크(_next/static/chunks/<oldhash>)를
    // 참조해 404 → CSS 일부가 비어서 레이아웃이 무너짐.
    // HTML/RSC 는 매번 ETag 검증, 정적 청크는 immutable 그대로.
    return [
      {
        source: '/((?!_next/static|_next/image|api|favicon).*)',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=0, must-revalidate' },
        ],
      },
    ]
  },
}

export default nextConfig
