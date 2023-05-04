export function isArticlePage() {
  return document.querySelector("meta[property='og:type']")?.content === "article";
}
