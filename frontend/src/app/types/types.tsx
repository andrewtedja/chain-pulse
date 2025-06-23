import type { SimulationNodeDatum } from "d3-force";

export type SentimentItem = {
	id: number;
	title: string;
	description?: string;
	coin_ticker: string;
	published_at: string;
	link: string;
	sentiment_score: number;
};

export type CoinSentiment = {
	ticker: string;
	name: string;
	scores: number[];
	news_count: number;
	sentiment_score: number;
};

export type BubbleNode = CoinSentiment &
	SimulationNodeDatum & {
		radius: number;
		x: number;
		y: number;
	};
