import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, TrendingDown, Minus, Calendar } from "lucide-react"
import { cn } from "@/lib/utils"

interface NewsItemProps {
  news: {
    ticker: string
    title: string
    content?: string
    date?: string
    sentiment: "positive" | "negative" | "neutral"
    score: number
    confidence?: number
    source?: string
  }
}

export function NewsItem({ news }: NewsItemProps) {
  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return "text-chart-4"
      case "negative":
        return "text-destructive"
      default:
        return "text-muted-foreground"
    }
  }

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return <TrendingUp className="h-5 w-5" />
      case "negative":
        return <TrendingDown className="h-5 w-5" />
      default:
        return <Minus className="h-5 w-5" />
    }
  }

  const getSentimentBg = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return "bg-chart-4/10 border-chart-4/30"
      case "negative":
        return "bg-destructive/10 border-destructive/30"
      default:
        return "bg-muted border-border"
    }
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="px-2 py-1 bg-primary/10 text-primary text-xs font-semibold rounded">{news.ticker}</span>
              {news.date && (
                <span className="flex items-center gap-1 text-xs text-muted-foreground">
                  <Calendar className="h-3 w-3" />
                  {new Date(news.date).toLocaleDateString()}
                </span>
              )}
              {news.source && <span className="text-xs text-muted-foreground">{news.source}</span>}
            </div>
            <CardTitle className="text-lg leading-tight">{news.title}</CardTitle>
          </div>
          <div
            className={cn(
              "flex items-center gap-2 px-3 py-2 rounded-lg border shrink-0",
              getSentimentBg(news.sentiment),
            )}
          >
            <span className={cn("font-semibold capitalize text-sm", getSentimentColor(news.sentiment))}>
              {news.sentiment}
            </span>
            <span className={getSentimentColor(news.sentiment)}>{getSentimentIcon(news.sentiment)}</span>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {news.content && <p className="text-sm text-muted-foreground mb-4 line-clamp-3">{news.content}</p>}
        <div className="flex items-center gap-4 text-sm">
          <div>
            <span className="text-muted-foreground">Score: </span>
            <span className={cn("font-semibold", getSentimentColor(news.sentiment))}>
              {news.score > 0 ? "+" : ""}
              {(news.score * 100).toFixed(1)}%
            </span>
          </div>
          {news.confidence !== undefined && (
            <div>
              <span className="text-muted-foreground">Confidence: </span>
              <span className="font-semibold text-foreground">{(news.confidence * 100).toFixed(1)}%</span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
