export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:4000"

export interface PatchNoteItem {
  id: string
  articleStateId: string
  date: string
  page: string
  area: string
  dotColor: string
  entityName: string
  title: string
  oneLiner: string
  score: number
  isRead: boolean
  sideCategory: string | null
}

export interface PatchNotesResponse {
  items: PatchNoteItem[]
  stats: {
    totalUpdates: number
    score5Items: number
    newFrameworks: number
    regulatory: number
  }
  areas: number
  period: { from: string; to: string }
}

export async function fetchPatchNotes(): Promise<PatchNotesResponse> {
  const res = await fetch(`${API_URL}/api/patch-notes`, { cache: "no-store" })
  if (!res.ok) throw new Error("Failed to fetch patch notes")
  return res.json()
}

export async function markArticleRead(articleStateId: string): Promise<void> {
  await fetch(`${API_URL}/api/patch-notes/${articleStateId}/read`, {
    method: "PATCH",
  })
}
