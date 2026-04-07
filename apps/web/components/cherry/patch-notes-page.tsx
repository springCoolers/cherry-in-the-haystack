"use client"

import { useState, useEffect } from "react"
import { cn } from "@/lib/utils"
import { Check } from "lucide-react"
import { fetchPatchNotes, markArticleRead, PatchNoteItem, PatchNotesResponse } from "@/lib/api"

/* ─────────────────────────────────────────────
   Badge styles by page
───────────────────────────────────────────── */
type BadgeKey = "cherry" | "violet" | "green" | "amber" | "muted"

const PAGE_BADGE: Record<string, BadgeKey> = {
  MODEL_UPDATES:    "cherry",
  PAPER_BENCHMARK:  "violet",
  FRAMEWORKS:       "violet",
  TOOLS:            "green",
  SHARED_RESOURCES: "green",
  CASE_STUDIES:     "green",
  REGULATIONS:      "muted",
  BIG_TECH_TRENDS:  "amber",
  THIS_WEEKS_POSTS: "amber",
}

const BADGE_STYLES: Record<BadgeKey, { bg: string; text: string; border: string }> = {
  cherry: { bg: "#FDF0F3", text: "#C94B6E", border: "#F2C4CE" },
  violet: { bg: "#F3EFFA", text: "#7B5EA7", border: "#C7B8E8" },
  green:  { bg: "#EFF7F3", text: "#2D7A5E", border: "#A8D4C0" },
  amber:  { bg: "#FDF6EE", text: "#D4854A", border: "#F0D8B0" },
  muted:  { bg: "#F2F0F7", text: "#9E97B3", border: "#E4E1EE" },
}

/* ─────────────────────────────────────────────
   Stars Component
───────────────────────────────────────────── */
function Stars({ count, color = "#C94B6E" }: { count: number; color?: string }) {
  return (
    <span className="flex items-center gap-[1px] text-[11px]" style={{ color }}>
      {Array.from({ length: 5 }).map((_, i) => (
        <span key={i} style={{ opacity: i < count ? 1 : 0.25 }}>★</span>
      ))}
    </span>
  )
}

/* ─────────────────────────────────────────────
   Timeline Item
───────────────────────────────────────────── */
function TimelineItem({
  item,
  index,
  total,
  onRead,
}: {
  item: PatchNoteItem
  index: number
  total: number
  onRead: (id: string) => void
}) {
  const badgeKey = PAGE_BADGE[item.page] ?? "muted"
  const badgeStyle = BADGE_STYLES[badgeKey]
  const FADE_START = 10
  const opacity = index < FADE_START ? 1 : Math.max(0.3, 1 - ((index - FADE_START + 1) / (total - FADE_START)) * 0.7)

  return (
    <div
      className="relative pl-6 cursor-pointer"
      style={{ opacity }}
      onClick={() => !item.isRead && onRead(item.articleStateId)}
    >
      {/* Dot */}
      <span
        className="absolute left-0 top-[7px] w-[10px] h-[10px] rounded-full border-2 border-card"
        style={{ backgroundColor: item.dotColor }}
      />

      {/* Content */}
      <div className="pb-5">
        <p className="text-[12px] text-text-muted mb-1">
          {item.date} · {item.area}
          {item.isRead && (
            <span className="ml-2 inline-flex items-center gap-0.5 text-[10px] font-semibold" style={{ color: "#C94B6E" }}>
              <Check className="w-2.5 h-2.5" /> read
            </span>
          )}
        </p>
        <p className="text-[15px] font-bold text-[#1A1626] mb-1 leading-snug">
          {item.title}
        </p>
        {item.oneLiner && (
          <p className="text-[13px] text-text-muted mb-2">{item.oneLiner}</p>
        )}
        <div className="flex items-center gap-2">
          <span
            className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold border"
            style={{
              backgroundColor: badgeStyle.bg,
              color: badgeStyle.text,
              borderColor: badgeStyle.border,
            }}
          >
            {item.area}
          </span>
          {item.sideCategory && (
            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold border"
              style={{ backgroundColor: "#EFF7F3", color: "#2D7A5E", borderColor: "#A8D4C0" }}
            >
              {item.sideCategory === "CASE_STUDY" ? "Case Study" : "Applied Research"}
            </span>
          )}
          {item.score > 0 && <Stars count={item.score} />}
        </div>
      </div>
    </div>
  )
}

/* ─────────────────────────────────────────────
   Filters
───────────────────────────────────────────── */
const FILTER_OPTIONS = ["All", "Models", "Frameworks", "Case Study", "Research", "Tools", "Big Tech", "Posts", "Regulations"]

/* ─────────────────────────────────────────────
   Main Page
───────────────────────────────────────────── */
export function PatchNotesPage() {
  const [data, setData] = useState<PatchNotesResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeFilter, setActiveFilter] = useState("All")

  useEffect(() => {
    fetchPatchNotes()
      .then(setData)
      .finally(() => setLoading(false))
  }, [])

  const handleRead = async (articleStateId: string) => {
    await markArticleRead(articleStateId)
    setData((prev) =>
      prev
        ? {
            ...prev,
            items: prev.items.map((item) =>
              item.articleStateId === articleStateId ? { ...item, isRead: true } : item
            ),
          }
        : prev
    )
  }

  const filteredItems = (data?.items ?? []).filter((item) =>
    activeFilter === "All" ? true : item.area === activeFilter
  )

  const unreadCount = (data?.items ?? []).filter((i) => !i.isRead).length
  const isAllRead = unreadCount === 0

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-text-muted text-[14px]">Loading patch notes...</p>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-text-muted text-[14px]">Failed to load patch notes.</p>
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1
          className="font-extrabold text-[#1A1626] leading-none mb-2.5 text-[22px] lg:text-[30px]"
          style={{ letterSpacing: "-0.5px" }}
        >
          Patch Notes
        </h1>
        <p className="text-[15px] text-text-muted leading-relaxed">
          {data.period.from} → {data.period.to} &nbsp;·&nbsp; Weekly changelog
        </p>
      </div>

      {/* Two-column layout */}
      <div className="flex flex-col lg:flex-row gap-6">
        {/* LEFT: Timeline */}
        <div className="w-full lg:flex-[0_0_65%] min-w-0">
          <p className="text-[10px] font-bold uppercase tracking-[0.8px] text-text-muted mb-4">
            {data.stats.totalUpdates} UPDATES · {data.areas} AREAS
            {unreadCount > 0 && ` · ${unreadCount} UNREAD`}
          </p>

          <div className="relative">
            {/* Vertical line */}
            <div
              className="absolute left-[4px] top-2 bottom-0 w-px"
              style={{ backgroundColor: "#E4E1EE" }}
            />

            {filteredItems.length === 0 ? (
              <div className="pl-6 text-[13px] text-text-muted py-8">No items in this area.</div>
            ) : (
              filteredItems.map((item, index) => (
                <TimelineItem key={item.id} item={item} index={index} total={filteredItems.length} onRead={handleRead} />
              ))
            )}

            {/* End card */}
            <div className="relative pl-6 pt-2">
              <div
                className="bg-card border border-border rounded-[16px] p-7 text-center"
                style={{ boxShadow: "0 1px 3px rgba(0,0,0,0.06)" }}
              >
                <div
                  className="mx-auto w-12 h-12 rounded-full flex items-center justify-center mb-3"
                  style={{ backgroundColor: isAllRead ? "#FDF0F3" : "#F3EFFA" }}
                >
                  <Check className="w-6 h-6" style={{ color: isAllRead ? "#C94B6E" : "#7B5EA7" }} />
                </div>
                <p className="text-[18px] font-extrabold mb-1" style={{ color: isAllRead ? "#C94B6E" : "#7B5EA7" }}>
                  {isAllRead ? "You're caught up" : `${unreadCount} left to read`}
                </p>
                <p className="text-[13px] text-text-muted mb-4">
                  {data.period.from} → {data.period.to} · {isAllRead ? "All read" : `${data.stats.totalUpdates - unreadCount} / ${data.stats.totalUpdates} read`}
                </p>
                <div className="flex items-center justify-center gap-6">
                  {[
                    { label: `${data.stats.totalUpdates} updates`, color: "#1A1626" },
                    { label: `${data.areas} areas`, color: "#1A1626" },
                    { label: isAllRead ? "Current" : "In progress", color: isAllRead ? "#C94B6E" : "#7B5EA7" },
                  ].map((stat) => (
                    <div key={stat.label} className="text-[12px] font-semibold" style={{ color: stat.color }}>
                      {stat.label}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT: Filter + Stats */}
        <div className="w-full lg:flex-[0_0_35%] min-w-0 space-y-3">
          {/* Filter card */}
          <div className="bg-card border border-border rounded-[12px] p-4">
            <p className="text-[10px] font-bold uppercase tracking-[0.8px] text-text-muted mb-3">
              Filter by Area
            </p>
            <div className="flex flex-wrap gap-2">
              {FILTER_OPTIONS.map((f) => {
                const isActive = activeFilter === f
                return (
                  <button
                    key={f}
                    onClick={() => setActiveFilter(f)}
                    className={cn(
                      "px-3 py-1.5 rounded-full text-[11px] font-semibold border transition-all cursor-pointer",
                      isActive
                        ? "bg-cherry-soft text-cherry border-cherry-border"
                        : "bg-card text-text-muted border-border hover:border-text-muted"
                    )}
                  >
                    {f}
                  </button>
                )
              })}
            </div>
          </div>

          {/* Stats card */}
          <div className="bg-card border border-border rounded-[12px] p-4">
            <p className="text-[10px] font-bold uppercase tracking-[0.8px] text-text-muted mb-3">
              This Period
            </p>
            <div className="space-y-2">
              {[
                { label: "Total updates",  value: String(data.stats.totalUpdates), color: "#1A1626" },
                { label: "Score 5 items",  value: String(data.stats.score5Items),  color: "#C94B6E" },
                { label: "New frameworks", value: String(data.stats.newFrameworks), color: "#1A1626" },
                { label: "Regulatory",     value: String(data.stats.regulatory),   color: "#1A1626" },
              ].map((stat) => (
                <div key={stat.label} className="flex items-center justify-between text-[13px]">
                  <span className="text-text-secondary">{stat.label}</span>
                  <span className="font-bold" style={{ color: stat.color }}>{stat.value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Guide card */}
          <div
            className="rounded-[12px] p-4 border"
            style={{ backgroundColor: "#F3EFFA", borderColor: "#C7B8E8" }}
          >
            <p className="text-[13px] font-bold mb-2 flex items-center gap-1.5" style={{ color: "#7B5EA7" }}>
              <span>💡</span>
              How to read Patch Notes
            </p>
            <p className="text-[12px] text-text-muted leading-relaxed">
              Items are sorted newest first. Click any item to mark as read. Faded items are already read.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
