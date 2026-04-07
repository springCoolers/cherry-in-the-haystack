"use client"

import { useEffect, useState } from "react"
import {
  fetchCaseStudies,
  CaseStudiesCategoryGroup,
  CaseStudyItem,
} from "@/lib/api"

/* ─────────────────────────────────────────────
   Category color map (by code)
───────────────────────────────────────────── */
const CATEGORY_COLORS: Record<string, { dot: string; label: string }> = {
  "cs-openai":    { dot: "#4B78F0", label: "OpenAI" },
  "cs-google":    { dot: "#7B5EA7", label: "Google" },
  "cs-anthropic": { dot: "#C94B6E", label: "Anthropic" },
  "cs-microsoft": { dot: "#0194E2", label: "Microsoft" },
}

const SIDE_CAT_STYLES: Record<string, { bg: string; color: string; border: string }> = {
  "CASE_STUDY":       { bg: "#EFF7F3", color: "#2D7A5E", border: "#A8D4BF" },
  "APPLIED_RESEARCH": { bg: "#F3EFFA", color: "#7B5EA7", border: "#C7B8E8" },
}
const DEFAULT_SIDE_STYLE = { bg: "#F2F0F7", color: "#9E97B3", border: "#E4E1EE" }

/* ─────────────────────────────────────────────
   Stars
───────────────────────────────────────────── */
function Stars({ count }: { count: number }) {
  return (
    <span className="text-[12px] tracking-tight" style={{ color: "#C94B6E" }}>
      {Array.from({ length: 5 }, (_, i) => (i < count ? "★" : "☆")).join("")}
    </span>
  )
}

/* ─────────────────────────────────────────────
   Side Category Tag
───────────────────────────────────────────── */
function SideTag({ code, name }: { code: string | null; name: string | null }) {
  if (!name) return null
  const s = (code && SIDE_CAT_STYLES[code]) ?? DEFAULT_SIDE_STYLE
  return (
    <span
      className="inline-flex px-2 py-0.5 rounded-[8px] text-[10px] font-bold uppercase"
      style={{ backgroundColor: s.bg, color: s.color, border: `1px solid ${s.border}` }}
    >
      {name}
    </span>
  )
}

/* ─────────────────────────────────────────────
   Article Card
───────────────────────────────────────────── */
function ArticleCard({ item }: { item: CaseStudyItem }) {
  return (
    <div
      className="bg-white rounded-[10px] p-4 mb-2.5 cursor-pointer transition-all duration-150 hover:bg-[#FAFAFA]"
      style={{ border: "1px solid #E4E1EE", boxShadow: "0 1px 3px rgba(0,0,0,0.06)" }}
      onMouseEnter={(e) => { e.currentTarget.style.borderColor = "#7B5EA7" }}
      onMouseLeave={(e) => { e.currentTarget.style.borderColor = "#E4E1EE" }}
    >
      <h3 className="text-[15px] font-semibold text-[#1A1626] leading-[1.4] mb-1.5">
        {item.title}
      </h3>
      <p className="text-[13px] text-[#9E97B3] leading-[1.55] mb-2.5 line-clamp-2">
        {item.oneLiner}
      </p>
      <div className="flex items-center gap-2 flex-wrap">
        <SideTag code={item.sideCategoryCode} name={item.sideCategory} />
        <Stars count={item.score} />
        <span
          className="px-2 py-0.5 rounded-[8px] text-[11px] text-[#9E97B3]"
          style={{ border: "1px solid #E4E1EE" }}
        >
          {item.entityName}
        </span>
        <span className="text-[10px] text-[#9E97B3]">{item.date}</span>
      </div>
    </div>
  )
}

/* ─────────────────────────────────────────────
   Category Group
───────────────────────────────────────────── */
function CategoryGroup({ group }: { group: CaseStudiesCategoryGroup }) {
  const meta = CATEGORY_COLORS[group.code] ?? { dot: "#9E97B3", label: group.name }
  return (
    <div className="mb-8">
      <div
        className="flex items-center gap-2.5 pb-2 mb-3"
        style={{ borderBottom: "1px solid #E4E1EE" }}
      >
        <span className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: meta.dot }} />
        <span className="text-[13px] font-bold uppercase tracking-[0.5px] text-[#1A1626]">
          {group.name}
        </span>
        <span className="text-[11px] text-[#9E97B3] ml-auto">{group.items.length} items</span>
      </div>
      {group.items.map((item) => (
        <ArticleCard key={item.id} item={item} />
      ))}
    </div>
  )
}

/* ─────────────────────────────────────────────
   Main Page
───────────────────────────────────────────── */
export function NDCaseStudiesPage() {
  const [groups, setGroups] = useState<CaseStudiesCategoryGroup[]>([])
  const [total, setTotal] = useState(0)
  const [period, setPeriod] = useState<{ from: string; to: string } | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCaseStudies()
      .then((data) => {
        setGroups(data.groups)
        setTotal(data.total)
        setPeriod(data.period)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const periodLabel = period?.from
    ? `${period.from} – ${period.to}`
    : ""

  return (
    <div className="flex h-full">
      <div style={{ padding: "28px 32px", maxWidth: 900, width: "100%" }}>
        {/* Header */}
        <div className="flex items-end justify-between flex-wrap gap-3 mb-6">
          <div>
            <h1
              className="font-extrabold text-[#1A1626] leading-tight"
              style={{ fontSize: "26px", letterSpacing: "-0.3px" }}
            >
              Case Studies
            </h1>
            <p className="text-[13px] text-[#9E97B3] mt-1.5">
              {loading ? "Loading…" : `${total} items · ${groups.length} sources · ${periodLabel}`}
            </p>
          </div>
          <span
            className="px-4 py-1.5 rounded-[6px] text-[12px] font-semibold"
            style={{ backgroundColor: "#EFF7F3", color: "#2D7A5E", border: "1px solid #A8D4BF" }}
          >
            Case Studies
          </span>
        </div>

        {loading ? (
          <div className="text-[13px] text-[#9E97B3] py-12 text-center">Loading…</div>
        ) : groups.length === 0 ? (
          <div className="text-[13px] text-[#9E97B3] py-12 text-center">No case studies found</div>
        ) : (
          groups.map((g) => <CategoryGroup key={g.id} group={g} />)
        )}
      </div>
    </div>
  )
}
