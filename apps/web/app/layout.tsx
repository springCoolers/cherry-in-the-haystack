import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Plus_Jakarta_Sans } from 'next/font/google'
import './globals.css'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const plusJakartaSans = Plus_Jakarta_Sans({
  subsets: ['latin'],
  variable: '--font-rounded',
  display: 'swap',
  weight: ['500', '600', '700', '800'],
})

export const metadata: Metadata = {
  title: 'Cherry — Knowledge Platform for AI Engineers',
  description: 'Curated intelligence for LLM practitioners. Weekly digests, concept guides, and cutting-edge research — distilled for builders.',
  generator: 'v0.app',
}

// Tailwind v4 가 청크로 분리한 CSS 가 어떤 이유로든 미적용될 때 디자인이
// 0px spacing 으로 무너지는 걸 막는 백업. :where() 로 specificity 0 →
// Tailwind 가 정상 로드되면 무조건 그쪽이 이김 (디자인 변화 0).
// var(--spacing) 의존 없이 직접 px 값을 박기 때문에 청크 일부 누락 시에도 작동.
const FALLBACK_CSS = `
:where(.flex){display:flex}
:where(.inline-flex){display:inline-flex}
:where(.grid){display:grid}
:where(.block){display:block}
:where(.inline-block){display:inline-block}
:where(.hidden){display:none}
:where(.flex-col){flex-direction:column}
:where(.flex-row){flex-direction:row}
:where(.flex-wrap){flex-wrap:wrap}
:where(.flex-1){flex:1 1 0%}
:where(.flex-shrink-0),:where(.shrink-0){flex-shrink:0}
:where(.items-center){align-items:center}
:where(.items-start){align-items:flex-start}
:where(.items-end){align-items:flex-end}
:where(.justify-center){justify-content:center}
:where(.justify-between){justify-content:space-between}
:where(.justify-end){justify-content:flex-end}
:where(.justify-start){justify-content:flex-start}
:where(.text-left){text-align:left}
:where(.text-center){text-align:center}
:where(.text-right){text-align:right}
:where(.w-full){width:100%}
:where(.h-full){height:100%}
:where(.min-w-0){min-width:0}
:where(.min-h-0){min-height:0}
:where(.relative){position:relative}
:where(.absolute){position:absolute}
:where(.fixed){position:fixed}
:where(.sticky){position:sticky}
:where(.overflow-hidden){overflow:hidden}
:where(.overflow-auto){overflow:auto}
:where(.overflow-y-auto){overflow-y:auto}
:where(.overflow-x-auto){overflow-x:auto}
:where(.cursor-pointer){cursor:pointer}
:where(.whitespace-nowrap){white-space:nowrap}
:where(.truncate){overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
:where(.gap-0){gap:0}
:where(.gap-0\\.5){gap:2px}
:where(.gap-1){gap:4px}
:where(.gap-1\\.5){gap:6px}
:where(.gap-2){gap:8px}
:where(.gap-2\\.5){gap:10px}
:where(.gap-3){gap:12px}
:where(.gap-4){gap:16px}
:where(.gap-5){gap:20px}
:where(.gap-6){gap:24px}
:where(.gap-8){gap:32px}
:where(.p-0){padding:0}
:where(.p-1){padding:4px}
:where(.p-2){padding:8px}
:where(.p-3){padding:12px}
:where(.p-4){padding:16px}
:where(.p-5){padding:20px}
:where(.p-6){padding:24px}
:where(.p-8){padding:32px}
:where(.px-1){padding-left:4px;padding-right:4px}
:where(.px-1\\.5){padding-left:6px;padding-right:6px}
:where(.px-2){padding-left:8px;padding-right:8px}
:where(.px-2\\.5){padding-left:10px;padding-right:10px}
:where(.px-3){padding-left:12px;padding-right:12px}
:where(.px-4){padding-left:16px;padding-right:16px}
:where(.px-5){padding-left:20px;padding-right:20px}
:where(.px-6){padding-left:24px;padding-right:24px}
:where(.px-8){padding-left:32px;padding-right:32px}
:where(.px-10){padding-left:40px;padding-right:40px}
:where(.py-0\\.5){padding-top:2px;padding-bottom:2px}
:where(.py-1){padding-top:4px;padding-bottom:4px}
:where(.py-1\\.5){padding-top:6px;padding-bottom:6px}
:where(.py-2){padding-top:8px;padding-bottom:8px}
:where(.py-2\\.5){padding-top:10px;padding-bottom:10px}
:where(.py-3){padding-top:12px;padding-bottom:12px}
:where(.py-4){padding-top:16px;padding-bottom:16px}
:where(.py-5){padding-top:20px;padding-bottom:20px}
:where(.py-6){padding-top:24px;padding-bottom:24px}
:where(.py-8){padding-top:32px;padding-bottom:32px}
:where(.py-12){padding-top:48px;padding-bottom:48px}
:where(.pt-1){padding-top:4px}
:where(.pt-2){padding-top:8px}
:where(.pt-3){padding-top:12px}
:where(.pt-4){padding-top:16px}
:where(.pt-5){padding-top:20px}
:where(.pb-0){padding-bottom:0}
:where(.pb-1){padding-bottom:4px}
:where(.pb-2){padding-bottom:8px}
:where(.pb-3){padding-bottom:12px}
:where(.pb-4){padding-bottom:16px}
:where(.pb-6){padding-bottom:24px}
:where(.pl-2){padding-left:8px}
:where(.pl-3){padding-left:12px}
:where(.pl-5){padding-left:20px}
:where(.pl-8){padding-left:32px}
:where(.pr-2){padding-right:8px}
:where(.pr-3){padding-right:12px}
:where(.pr-6){padding-right:24px}
:where(.m-0){margin:0}
:where(.mb-0\\.5){margin-bottom:2px}
:where(.mb-1){margin-bottom:4px}
:where(.mb-1\\.5){margin-bottom:6px}
:where(.mb-2){margin-bottom:8px}
:where(.mb-2\\.5){margin-bottom:10px}
:where(.mb-3){margin-bottom:12px}
:where(.mb-4){margin-bottom:16px}
:where(.mb-5){margin-bottom:20px}
:where(.mb-6){margin-bottom:24px}
:where(.mb-10){margin-bottom:40px}
:where(.mt-0\\.5){margin-top:2px}
:where(.mt-1){margin-top:4px}
:where(.mt-1\\.5){margin-top:6px}
:where(.mt-2){margin-top:8px}
:where(.mt-3){margin-top:12px}
:where(.mt-4){margin-top:16px}
:where(.mt-5){margin-top:20px}
:where(.mt-6){margin-top:24px}
:where(.ml-1){margin-left:4px}
:where(.ml-1\\.5){margin-left:6px}
:where(.ml-2){margin-left:8px}
:where(.ml-4){margin-left:16px}
:where(.ml-5){margin-left:20px}
:where(.space-y-1>*+*){margin-top:4px}
:where(.space-y-1\\.5>*+*){margin-top:6px}
:where(.space-y-3>*+*){margin-top:12px}
:where(.space-y-4>*+*){margin-top:16px}
:where(.bg-white){background-color:#ffffff}
:where(.bg-transparent){background-color:transparent}
:where(.border){border-width:1px;border-style:solid;border-color:#E4E1EE}
:where(.border-t){border-top-width:1px;border-top-style:solid}
:where(.border-b){border-bottom-width:1px;border-bottom-style:solid}
:where(.border-b-2){border-bottom-width:2px;border-bottom-style:solid}
:where(.border-r){border-right-width:1px;border-right-style:solid}
:where(.border-l){border-left-width:1px;border-left-style:solid}
:where(.rounded){border-radius:4px}
:where(.rounded-md){border-radius:6px}
:where(.rounded-lg){border-radius:8px}
:where(.rounded-xl){border-radius:12px}
:where(.rounded-2xl){border-radius:16px}
:where(.rounded-full){border-radius:9999px}
@media (min-width:1024px){
:where(.lg\\:flex){display:flex}
:where(.lg\\:flex-row){flex-direction:row}
:where(.lg\\:flex-col){flex-direction:column}
:where(.lg\\:items-end){align-items:flex-end}
:where(.lg\\:items-start){align-items:flex-start}
:where(.lg\\:items-center){align-items:center}
:where(.lg\\:gap-3){gap:12px}
:where(.lg\\:gap-4){gap:16px}
:where(.lg\\:gap-5){gap:20px}
:where(.lg\\:p-5){padding:20px}
:where(.lg\\:p-6){padding:24px}
:where(.lg\\:p-8){padding:32px}
:where(.lg\\:px-4){padding-left:16px;padding-right:16px}
:where(.lg\\:px-6){padding-left:24px;padding-right:24px}
:where(.lg\\:py-2\\.5){padding-top:10px;padding-bottom:10px}
:where(.lg\\:py-5){padding-top:20px;padding-bottom:20px}
:where(.lg\\:pt-5){padding-top:20px}
:where(.lg\\:pb-0){padding-bottom:0}
:where(.lg\\:mb-3){margin-bottom:12px}
:where(.lg\\:h-full){height:100%}
:where(.lg\\:w-\\[420px\\]){width:420px}
:where(.lg\\:max-h-none){max-height:none}
}
@media (max-width:1023px){
:where(.hidden.lg\\:flex){display:none}
}
`
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${plusJakartaSans.variable}`} suppressHydrationWarning>
      <head>
        <style dangerouslySetInnerHTML={{ __html: FALLBACK_CSS }} />
      </head>
      <body className="font-sans antialiased" suppressHydrationWarning>
        {children}
      </body>
    </html>
  )
}
