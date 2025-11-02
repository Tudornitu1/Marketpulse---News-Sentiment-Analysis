"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart3, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { NewsItem } from "@/components/news-item"

export default function Home() {
  const [loading, setLoading] = useState(true)
  const [newsData, setNewsData] = useState<any[]>([])
  const [error, setError] = useState<string | null>(null)

  const fetchNews = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch("/api/news")
      if (!response.ok) throw new Error("Failed to fetch news")
      const data = await response.json()
      setNewsData(data)
    } catch (error) {
      console.error("Failed to fetch news:", error)
      setError("Failed to load news data")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchNews()
  }, [])

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BarChart3 className="h-6 w-6 text-primary" />
            <h1 className="text-xl font-semibold text-foreground">Stock Sentiment Analyzer</h1>
          </div>
          <Button variant="outline" size="sm" onClick={fetchNews} disabled={loading}>
            <RefreshCw className={`h-4 w-4 mr-2 ${loading ? "animate-spin" : ""}`} />
            Refresh
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>News Sentiment Analysis</CardTitle>
            <CardDescription>Real-time sentiment analysis of stock market news from your database</CardDescription>
          </CardHeader>
        </Card>

        {error && (
          <Card className="mb-6 border-destructive">
            <CardContent className="pt-6">
              <p className="text-destructive">{error}</p>
            </CardContent>
          </Card>
        )}

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <RefreshCw className="h-8 w-8 animate-spin text-muted-foreground" />
          </div>
        ) : (
          <div className="space-y-4">
            {newsData.length === 0 ? (
              <Card>
                <CardContent className="pt-6 text-center text-muted-foreground">No news data available</CardContent>
              </Card>
            ) : (
              newsData.map((news, index) => <NewsItem key={index} news={news} />)
            )}
          </div>
        )}
      </main>
    </div>
  )
}
