"use client"

import { useEffect, useState } from "react"
import { KaasCatalogPage } from "@/components/cherry/kaas-catalog-page"
import {
  PurchaseModal,
  type PurchaseAction,
  type PurchaseAgent,
  type PurchaseTarget,
} from "@/components/cherry/purchase-modal"
import { StartFlowNav } from "@/components/cherry/start-flow-nav"
import { fetchAgents } from "@/lib/api"
import { getAccessToken, useAuthTick } from "@/lib/auth"

// Base costs mirror kaas-catalog-page (line 380-381). Sale discount math
// already happens server-side, so we just pass the base here.
const PURCHASE_BASE = 20
const FOLLOW_BASE = 25

export default function ShopPage() {
  useAuthTick()
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])
  const token = mounted ? getAccessToken() : null

  const [agents, setAgents] = useState<PurchaseAgent[]>([])
  const [modalOpen, setModalOpen] = useState(false)
  const [action, setAction] = useState<PurchaseAction>("purchase")
  const [target, setTarget] = useState<PurchaseTarget | null>(null)

  // Load agents for the target-AI dropdown. Skip if unauth — the Buy click
  // can still prompt sign-in via the modal showing "AI 없음".
  useEffect(() => {
    if (!token) return
    fetchAgents()
      .then((data) => {
        if (!Array.isArray(data)) return
        setAgents(
          data.map((a) => ({
            id: a.id,
            name: a.name,
            icon: a.icon,
            api_key: a.api_key,
            karma_tier: a.karma_tier,
            credits: a.credits,
          })),
        )
      })
      .catch(() => setAgents([]))
  }, [token])

  function handleCatalogQuery(title: string, depth: string, conceptId?: string) {
    if (!conceptId) return
    const next: PurchaseAction = depth === "follow" ? "follow" : "purchase"
    setAction(next)
    setTarget({
      conceptId,
      conceptTitle: title,
      creditsBase: next === "follow" ? FOLLOW_BASE : PURCHASE_BASE,
    })
    setModalOpen(true)
  }

  return (
    <div>
      <header className="mb-4 flex items-start justify-between gap-4 flex-wrap">
        <div className="min-w-0">
          <h1 className="text-[22px] font-extrabold text-[#3A2A1C]">Shop</h1>
          <p className="text-[12px] text-[#9A7C55] mt-1">
            Browse the skills your AI needs.
          </p>
        </div>
        <StartFlowNav current="shop" />
      </header>

      <KaasCatalogPage onQuery={handleCatalogQuery} />

      <PurchaseModal
        open={modalOpen}
        action={action}
        target={target}
        agents={agents}
        onClose={() => setModalOpen(false)}
        onSuccess={() => {
          // Notify the catalog so it re-runs Compare (updates OWNED badges
          // + gap counts). Fires before the credit refresh so the UI updates
          // immediately on success.
          if (typeof window !== "undefined") {
            window.dispatchEvent(new CustomEvent("kaas-purchase-complete"))
          }
          // Refresh agent credits so the next modal open shows the updated
          // balance in the AI dropdown.
          if (!token) return
          fetchAgents()
            .then((data) => {
              if (!Array.isArray(data)) return
              setAgents(
                data.map((a) => ({
                  id: a.id,
                  name: a.name,
                  icon: a.icon,
                  api_key: a.api_key,
                  karma_tier: a.karma_tier,
                  credits: a.credits,
                })),
              )
            })
            .catch(() => {})
        }}
      />
    </div>
  )
}
