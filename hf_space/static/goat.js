// Group Goat, CO3133 Assignment 02: preprocessing and baseline maths for the web demo.
// Same rules as notebook cell 10 and the same computation as scikit-learn's TfidfVectorizer +
// LogisticRegression, so the page gives the predictions of the saved checkpoints.

// text_min (DistilBERT): NFC, lowercase, trim, collapse whitespace
export function cleanMin(text) {
    return text.normalize("NFC").toLowerCase().trim().replace(/\s+/g, " ");
}

// b = baseline.json written by export_web.py
export function makeBaseline(b) {
    const index = new Map(b.terms.map((term, i) => [term, i]));
    const stop = new Set(b.stop_words);

    // text_aggr (baseline): text_min, keep only letters/digits/spaces, drop stopwords (negations kept)
    function cleanAggr(text) {
        return cleanMin(text).replace(/[^a-z0-9\s]/g, " ").split(/\s+/)
            .filter((w) => w && !stop.has(w)).join(" ");
    }

    function predict(text) {
        const textAggr = cleanAggr(text);
        // sklearn token_pattern \b\w\w+\b, then unigrams + bigrams
        const tokens = textAggr.match(/\b\w\w+\b/g) || [];
        const grams = tokens.slice();
        for (let i = 0; i + 1 < tokens.length; i++) grams.push(tokens[i] + " " + tokens[i + 1]);

        // term count x idf, then L2 normalisation (n-grams not seen in training are ignored)
        const counts = new Map();
        for (const g of grams) {
            const j = index.get(g);
            if (j !== undefined) counts.set(j, (counts.get(j) || 0) + 1);
        }
        const weights = [];
        let norm = 0;
        for (const [j, c] of counts) {
            const v = c * b.idf[j];
            weights.push([j, v]);
            norm += v * v;
        }
        norm = Math.sqrt(norm) || 1;

        // Logistic Regression: one score per class, softmax into probabilities
        const logits = b.intercept.map((c0, k) =>
            weights.reduce((s, [j, v]) => s + (v / norm) * b.coef[k][j], c0));
        const top = Math.max(...logits);
        const exps = logits.map((x) => Math.exp(x - top));
        const total = exps.reduce((a, x) => a + x, 0);
        return {
            textAggr,
            known: counts.size,
            probs: b.labels.map((label, k) => ({ label, score: exps[k] / total })),
        };
    }

    return { cleanAggr, predict };
}
