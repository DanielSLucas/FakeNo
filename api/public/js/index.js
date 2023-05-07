import { isArticlePage } from './utils.js';
import { modifyArticleHeader } from './view.js';

if (isArticlePage()) {
  await modifyArticleHeader();
}
