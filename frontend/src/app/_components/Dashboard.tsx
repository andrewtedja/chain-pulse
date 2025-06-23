"use client";

import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";
import { SentimentItem, CoinSentiment, BubbleNode } from "../types/types";

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8081";

const Dashboard = () => {
	const svgRef = useRef<SVGSVGElement | null>(null);
	const [sentimentData, setSentimentData] = useState<SentimentItem[] | null>(
		null
	);
	const [isLoading, setIsLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);
	const [isRefreshing, setIsRefreshing] = useState(false);
	const [processedData, setProcessedData] = useState<CoinSentiment[]>([]);

	const [currentPage, setCurrentPage] = useState(1);
	const itemsPerPage = 10;

	useEffect(() => {
		const fetchSentimentData = async () => {
			try {
				setIsLoading(true);
				const res = await fetch(`${API_URL}/api/news`);
				const data = await res.json();
				setSentimentData(data.news.reverse());
			} catch (err: unknown) {
				if (err instanceof Error) {
					setError(err.message);
				}
			} finally {
				setIsLoading(false);
			}
		};
		fetchSentimentData();
	}, []);

	async function handleRefresh() {
		try {
			setIsRefreshing(true);
			await fetch(`${API_URL}/api/refresh-news`, {
				method: "POST",
			});
			const res = await fetch(`${API_URL}/api/news`);
			const data = await res.json();
			setSentimentData(data.news.reverse());
		} catch (err) {
			console.error("Refresh failed:", err);
		} finally {
			setIsRefreshing(false);
		}
	}

	const processSentimentData = (
		newsData: SentimentItem[]
	): CoinSentiment[] => {
		const coinSentiments: Record<
			string,
			Omit<CoinSentiment, "sentiment_score">
		> = {};

		newsData.forEach((news) => {
			const ticker = news.coin_ticker;
			if (!coinSentiments[ticker]) {
				coinSentiments[ticker] = {
					ticker,
					name: ticker,
					scores: [],
					news_count: 0,
				};
			}
			coinSentiments[ticker].scores.push(news.sentiment_score);
			coinSentiments[ticker].news_count++;
		});

		return Object.values(coinSentiments).map((coin) => ({
			...coin,
			sentiment_score:
				coin.scores.length > 0
					? coin.scores.reduce((a, b) => a + b, 0) /
					  coin.scores.length
					: 0,
		}));
	};

	useEffect(() => {
		if (sentimentData) {
			const processed = processSentimentData(sentimentData);
			setProcessedData(processed);
		}
	}, [sentimentData]);

	// D3 Bubble Chart
	useEffect(() => {
		if (!processedData.length) return;

		const svg = d3.select(svgRef.current);
		svg.selectAll("*").remove(); // Clear previous chart

		// Responsive dimensions
		const containerWidth = 800;
		const width = Math.min(containerWidth, window.innerWidth - 100);
		const height = 500;

		svg.attr("width", width).attr("height", height);

		// Color scale based on sentiment score (-1 to 1)
		const colorScale = d3
			.scaleLinear<string>()
			.domain([-1, 0, 1])
			.range(["#ff4444", "#666666", "#00ff88"]);

		// Size scale based on news count
		const extent = d3.extent(processedData, (d) => d.news_count);

		if (!extent[0] === undefined || !extent[1] === undefined) return;

		const sizeScale = d3
			.scaleSqrt()
			.domain(extent as [number, number])
			.range([20, 80]);

		// Prepare nodes for force simulation
		const nodes: BubbleNode[] = processedData.map((d) => ({
			...d,
			radius: sizeScale(d.news_count),
			x: Math.random() * width,
			y: Math.random() * height,
		}));

		// Force simulation
		const simulation = d3
			.forceSimulation<BubbleNode>(nodes)
			.force("charge", d3.forceManyBody().strength(-300))
			.force("center", d3.forceCenter(width / 2, height / 2))
			.force(
				"collision",
				d3.forceCollide().radius((d) => (d as BubbleNode).radius + 3)
			)
			.force("x", d3.forceX(width / 2).strength(0.1))
			.force("y", d3.forceY(height / 2).strength(0.1));

		// Create tooltip
		const tooltip = d3
			.select("body")
			.append("div")
			.attr("class", "bubble-tooltip")
			.style("position", "absolute")
			.style("background", "rgba(0, 0, 0, 0.95)")
			.style("color", "white")
			.style("padding", "12px")
			.style("border-radius", "8px")
			.style("font-size", "13px")
			.style("border", "1px solid #333")
			.style("pointer-events", "none")
			.style("opacity", 0)
			.style("z-index", 1000);

		// Create bubble groups
		const bubbles = svg
			.selectAll(".bubble")
			.data(nodes)
			.enter()
			.append("g")
			.attr("class", "bubble")
			.style("cursor", "pointer");

		// Add circles
		bubbles
			.append("circle")
			.attr("r", (d: BubbleNode) => d.radius)
			.attr("fill", (d: BubbleNode) => colorScale(d.sentiment_score))
			.attr("stroke", "#333")
			.attr("stroke-width", 2)
			.style("opacity", 0.85);

		// Add ticker text
		bubbles
			.append("text")
			.attr("text-anchor", "middle")
			.attr("dominant-baseline", "middle")
			.attr("fill", "white")
			.attr("font-weight", "bold")
			.attr("font-size", (d: BubbleNode) => Math.min(d.radius / 2.2, 14))
			.text((d: BubbleNode) => d.ticker)
			.style("pointer-events", "none");

		// Add sentiment score text
		bubbles
			.append("text")
			.attr("text-anchor", "middle")
			.attr("dominant-baseline", "middle")
			.attr("dy", (d: BubbleNode) => d.radius / 3.5)
			.attr("fill", (d: BubbleNode) =>
				d.sentiment_score > 0
					? "#00ff88"
					: d.sentiment_score < 0
					? "#ff4444"
					: "#888"
			)
			.attr("font-size", (d: BubbleNode) => Math.min(d.radius / 3.5, 10))
			.text((d: BubbleNode) =>
				d.sentiment_score > 0
					? `+${d.sentiment_score.toFixed(2)}`
					: d.sentiment_score.toFixed(2)
			)
			.style("pointer-events", "none");

		// Add hover effects
		bubbles
			.on(
				"mouseover",
				function (this: SVGGElement, event: MouseEvent, d: BubbleNode) {
					d3.select(this)
						.select("circle")
						.transition()
						.duration(200)
						.attr("r", d.radius * 1.15)
						.style("opacity", 1);

					tooltip
						.style("opacity", 1)
						.html(
							`
						<strong>${d.name} (${d.ticker})</strong><br>
						Sentiment Score: ${d.sentiment_score.toFixed(3)}<br>
						News Articles: ${d.news_count}<br>
						Sentiment: ${
							d.sentiment_score > 0.1
								? "Bullish 🚀"
								: d.sentiment_score < -0.1
								? "Bearish 📉"
								: "Neutral ⚖️"
						}
					`
						)
						.style("left", event.pageX + 15 + "px")
						.style("top", event.pageY - 15 + "px");
				}
			)
			.on(
				"mouseout",
				function (this: SVGGElement, event: MouseEvent, d: BubbleNode) {
					d3.select(this)
						.select("circle")
						.transition()
						.duration(200)
						.attr("r", d.radius)
						.style("opacity", 0.85);

					tooltip.style("opacity", 0);
				}
			)
			.on(
				"click",
				function (this: SVGGElement, event: MouseEvent, d: BubbleNode) {
					// Click animation
					d3.select(this)
						.select("circle")
						.transition()
						.duration(100)
						.attr("r", d.radius * 0.9)
						.transition()
						.duration(100)
						.attr("r", d.radius);

					console.log(
						"Clicked on:",
						d.ticker,
						"Sentiment:",
						d.sentiment_score
					);
				}
			);

		// Update positions on simulation tick
		simulation.on("tick", () => {
			bubbles.attr(
				"transform",
				(d: BubbleNode) => `translate(${d.x}, ${d.y})`
			);
		});

		// Cleanup function
		return () => {
			tooltip.remove();
		};
	}, [processedData]);

	// Pagination logic
	const totalPages = sentimentData
		? Math.ceil(sentimentData.length / itemsPerPage)
		: 0;
	const startIndex = (currentPage - 1) * itemsPerPage;
	const currentNews = sentimentData
		? sentimentData.slice(startIndex, startIndex + itemsPerPage)
		: [];

	const formatDate = (dateString: string) => {
		return new Date(dateString).toLocaleString();
	};

	const getSentimentLabel = (score: number) => {
		if (score > 0.1)
			return { label: "Bullish", emoji: "🚀", color: "text-green-400" };
		if (score < -0.1)
			return { label: "Bearish", emoji: "📉", color: "text-red-400" };
		return { label: "Neutral", emoji: "⚖️", color: "text-gray-400" };
	};

	if (error) {
		return (
			<div className="flex items-center justify-center min-h-screen bg-black text-white">
				<div className="text-center">
					<p className="text-red-400 mb-4">⚠️ {error}</p>
					<button
						onClick={() => window.location.reload()}
						className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded"
					>
						Retry
					</button>
				</div>
			</div>
		);
	}

	return (
		<div className="min-h-screen bg-black text-white">
			{/* Header */}
			<div className="px-6 py-4 border-b border-gray-800">
				<div className="flex justify-between items-center">
					<div>
						<h1 className="text-3xl font-bold">
							🎭 Crypto Sentiment Dashboard
						</h1>
						<p className="text-gray-400 mt-2">
							Real-time sentiment analysis from crypto news
						</p>
					</div>
					<button
						onClick={handleRefresh}
						disabled={isRefreshing || isLoading}
						className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded-lg transition-colors"
					>
						{isRefreshing ? "🔄 Refreshing..." : "🔄 Refresh Data"}
					</button>
				</div>
			</div>

			{/* Main Content - Split Layout */}
			<div className="flex flex-col lg:flex-row h-full">
				{/* Left Section - Bubble Chart */}
				<div className="lg:w-3/5 p-6">
					<div className="mb-4">
						<h2 className="text-2xl font-bold mb-2">
							Sentiment Bubbles
						</h2>

						{/* Legend */}
						<div className="flex flex-wrap items-center justify-center lg:justify-start mb-4 space-x-6">
							<div className="flex items-center space-x-2">
								<div className="w-4 h-4 bg-green-500 rounded-full"></div>
								<span className="text-sm">Bullish</span>
							</div>
							<div className="flex items-center space-x-2">
								<div className="w-4 h-4 bg-gray-500 rounded-full"></div>
								<span className="text-sm">Neutral</span>
							</div>
							<div className="flex items-center space-x-2">
								<div className="w-4 h-4 bg-red-500 rounded-full"></div>
								<span className="text-sm">Bearish</span>
							</div>
							<div className="text-sm text-gray-400">
								💡 Size = News volume
							</div>
						</div>
					</div>

					{/* Chart Container */}
					<div className="flex justify-center">
						<div className="relative bg-gray-900 rounded-lg p-4 shadow-xl">
							{isLoading && (
								<div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 rounded-lg z-10">
									<div className="text-white text-center">
										<div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mb-2 mx-auto"></div>
										<p>Loading sentiment data...</p>
									</div>
								</div>
							)}
							<svg ref={svgRef} className="drop-shadow-lg"></svg>
						</div>
					</div>

					{/* Stats */}
					{sentimentData && sentimentData.length > 0 && (
						<div className="mt-6 grid grid-cols-3 gap-4">
							<div className="bg-gray-800 p-4 rounded-lg text-center">
								<div className="text-xl font-bold text-green-400">
									{
										sentimentData.filter(
											(d) => d.sentiment_score > 0.1
										).length
									}
								</div>
								<div className="text-xs text-gray-400">
									Bullish Articles
								</div>
							</div>
							<div className="bg-gray-800 p-4 rounded-lg text-center">
								<div className="text-xl font-bold text-red-400">
									{
										sentimentData.filter(
											(d) => d.sentiment_score < -0.1
										).length
									}
								</div>
								<div className="text-xs text-gray-400">
									Bearish Articles
								</div>
							</div>
							<div className="bg-gray-800 p-4 rounded-lg text-center">
								<div className="text-xl font-bold text-blue-400">
									{sentimentData.length}
								</div>
								<div className="text-xs text-gray-400">
									Total Articles
								</div>
							</div>
						</div>
					)}
				</div>

				{/* Right Section - News Feed */}
				<div className="lg:w-2/5 border-l border-gray-800 p-6">
					<div className="mb-4">
						<h2 className="text-2xl font-bold mb-2">Latest News</h2>
						<p className="text-gray-400 text-sm">
							Page {currentPage} of {totalPages} (
							{sentimentData?.length || 0} total articles)
						</p>
					</div>

					{/* News List */}
					<div className="space-y-4 mb-6">
						{currentNews.map((news) => {
							const sentiment = getSentimentLabel(
								news.sentiment_score
							);
							return (
								<div
									key={news.id}
									className="bg-gray-900 rounded-lg p-4 hover:bg-gray-800 transition-colors"
								>
									<div className="flex justify-between items-start mb-2">
										<span className="bg-blue-600 text-xs px-2 py-1 rounded">
											{news.coin_ticker}
										</span>
										<span
											className={`text-xs ${sentiment.color} flex items-center gap-1`}
										>
											{sentiment.emoji} {sentiment.label}
										</span>
									</div>

									<h3 className="font-semibold text-sm mb-2 line-clamp-2">
										{news.title}
									</h3>

									{news.description && (
										<p className="text-gray-400 text-xs mb-2 line-clamp-2">
											{news.description}
										</p>
									)}

									<div className="flex justify-between items-center text-xs text-gray-500">
										<span>
											{formatDate(news.published_at)}
										</span>
										<span
											className={`font-mono ${
												news.sentiment_score > 0
													? "text-green-400"
													: news.sentiment_score < 0
													? "text-red-400"
													: "text-gray-400"
											}`}
										>
											{news.sentiment_score > 0
												? "+"
												: ""}
											{news.sentiment_score.toFixed(3)}
										</span>
									</div>

									{news.link && (
										<a
											href={news.link}
											target="_blank"
											rel="noopener noreferrer"
											className="text-blue-400 hover:text-blue-300 text-xs mt-2 inline-block"
										>
											Read more →
										</a>
									)}
								</div>
							);
						})}
					</div>

					{/* Pagination */}
					{totalPages > 1 && (
						<div className="flex justify-center items-center space-x-2">
							<button
								onClick={() =>
									setCurrentPage((prev) =>
										Math.max(1, prev - 1)
									)
								}
								disabled={currentPage === 1}
								className="px-3 py-1 bg-gray-700 hover:bg-gray-600 disabled:bg-gray-800 disabled:text-gray-500 rounded text-sm"
							>
								← Prev
							</button>

							<div className="flex space-x-1">
								{Array.from(
									{ length: Math.min(5, totalPages) },
									(_, i) => {
										let pageNum;
										if (totalPages <= 5) {
											pageNum = i + 1;
										} else if (currentPage <= 3) {
											pageNum = i + 1;
										} else if (
											currentPage >=
											totalPages - 2
										) {
											pageNum = totalPages - 4 + i;
										} else {
											pageNum = currentPage - 2 + i;
										}

										return (
											<button
												key={pageNum}
												onClick={() =>
													setCurrentPage(pageNum)
												}
												className={`px-2 py-1 text-sm rounded ${
													currentPage === pageNum
														? "bg-blue-600 text-white"
														: "bg-gray-700 hover:bg-gray-600"
												}`}
											>
												{pageNum}
											</button>
										);
									}
								)}
							</div>

							<button
								onClick={() =>
									setCurrentPage((prev) =>
										Math.min(totalPages, prev + 1)
									)
								}
								disabled={currentPage === totalPages}
								className="px-3 py-1 bg-gray-700 hover:bg-gray-600 disabled:bg-gray-800 disabled:text-gray-500 rounded text-sm"
							>
								Next →
							</button>
						</div>
					)}

					{/* No data message */}
					{!isLoading &&
						(!currentNews || currentNews.length === 0) && (
							<div className="text-center text-gray-400 py-8">
								<p>No news articles available</p>
							</div>
						)}
				</div>
			</div>
		</div>
	);
};

export default Dashboard;
