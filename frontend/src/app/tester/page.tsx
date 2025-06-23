"use client";

import React, { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8081";

type newsItem = {
	id: number;
	slug: string;
	title: string;
	description: string;
	published_at: string;
	created_at: string;
	kind: string;
	link: string;
};

const TestFetch = () => {
	const [news, setNews] = useState<newsItem[] | null>(null);
	const [error, setError] = useState<string | null>(null);
	const [loading, setLoading] = useState<boolean>(true);

	console.log("API_URL is:", API_URL);

	useEffect(() => {
		const fetchNews = async () => {
			try {
				const res = await fetch(`${API_URL}/api/news`);
				if (!res.ok) throw new Error("Failed to fetch");

				const data = await res.json();
				setNews(data.news);
			} catch (err: unknown) {
				if (err instanceof Error) {
					alert(err.message);
					setError(err.message);
				} else {
					setError("Unknown error");
				}
			} finally {
				setLoading(false);
			}
		};
		fetchNews();
		return () => {};
	}, []);

	return (
		<main className="p-4">
			{loading ? (
				<p>Loading...</p>
			) : (
				<div>
					<h1 className="text-xl font-bold mb-4 break-words">
						📰 News
					</h1>
					{error && (
						<p className="text-black break-words">Error: {error}</p>
					)}
					{news && (
						<div className="bg-gray-100 p-2 rounded break-words">
							<p>
								{news.map((item) => {
									return (
										<div key={item.id} className="mt-4">
											<p>News: {item.id}</p>
											<h2 className="font-bold">
												Title: {item.title}
											</h2>
											<p>
												Description: {item.description}
											</p>
										</div>
									);
								})}
							</p>
						</div>
					)}
				</div>
			)}
		</main>
	);
};

export default TestFetch;
