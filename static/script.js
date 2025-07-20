
// const url = "https://newsapi.org/v2/everything?q=";
const BASE_API_URL = "/api/predict";

console.log("✅ script.js loaded");

document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ DOM fully loaded");

    const params = new URLSearchParams(window.location.search);
    const category = params.get('category');
    if (category) {
        onNavItemclick(category);
    } else {
        fetchnews("world");
    }

    const searchButton = document.getElementById("search-btn");
    const searchText = document.getElementById("text-search");

    if (searchButton) {
        searchButton.addEventListener("click", () => {
            const query = searchText.value.trim();
            if (!query) return;
            fetchnews(query);
            curSelectNav?.classList.remove("active");
            curSelectNav = null;
        });
    }

    const fakeDetectionBtn = document.getElementById("fakedetection");
    if (fakeDetectionBtn) {
        fakeDetectionBtn.addEventListener("click", () => {
            console.log("🔍 Navigating to SpotFake page");
            window.location.href = "/spotfake";
        });
    }

    const checkNewsBtn = document.getElementById("check-news-btn");
    if (checkNewsBtn) {
        checkNewsBtn.addEventListener("click", async () => {
            console.log("🟢 Check News button clicked");

            const inputText = document.getElementById("news-input").value.trim();
            const resultBox = document.getElementById("result-box");
            const resultText = document.getElementById("result-text");

            if (!inputText) {
                resultText.innerText = "❗ Please enter some news text.";
                resultBox.classList.remove("hidden");
                return;
            }

            resultText.innerText = "🔎 Analyzing...";
            resultBox.classList.remove("hidden");

            try {
                const response = await fetch(BASE_API_URL, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ news: inputText })
                });

                const data = await response.json();
                console.log("✅ Prediction response:", data);

                if (data.verdict === "REAL") {
                    resultText.innerText = "✅ This news appears to be REAL.";
                } else if (data.verdict === "FAKE") {
                    resultText.innerText = "⚠️ This news appears to be FAKE.";
                } else {
                    resultText.innerText = "❗ Unable to determine: " + data.verdict;
                }

            } catch (err) {
                console.error("❌ Prediction failed:", err);
                resultText.innerText = "❌ Error connecting to server.";
            }
        });
    } else {
        console.error("❌ check-news-btn not found");
    }
});

// ========== News Section Code ==========
async function fetchnews(query) {
    console.log(`🔎 Fetching news for query: ${query}`);
    try {
        const res = await fetch(`/news?q=${query}`);
        const data = await res.json();
        console.log("📰 News data:", data);
        bindData(data.articles);
    } catch (err) {  
        console.error("❌ Error fetching news:", err);
    }
}

function bindData(articles) {
    const cardscontainer = document.getElementById("card-container");
    const newscardTemplate = document.getElementById("template-news-card");

    if (!cardscontainer || !newscardTemplate) {
        console.warn("⚠️ News container or template not found");
        return;
    }

    cardscontainer.innerHTML = '';
    articles.slice(0, 15).forEach((article) => {
        if (!article.urlToImage) return;

        const newsclone = newscardTemplate.content.cloneNode(true);
        filldataincard(newsclone, article);
        cardscontainer.appendChild(newsclone);
    });
}

function filldataincard(newsclone, article) {
    const newsImg = newsclone.querySelector("#news-img");
    const newsTitle = newsclone.querySelector("#news-title");
    const newsSource = newsclone.querySelector("#news-source");
    const newsDesc = newsclone.querySelector("#news-desc");

    newsImg.src = article.urlToImage;
    newsTitle.innerHTML = article.title;
    newsDesc.innerHTML = article.description;

    const date = new Date(article.publishedAt).toLocaleString("en-US", {
        timeZone: "Asia/Kolkata",
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });

    newsSource.innerHTML = `${article.source.name} | ${date}`;

    newsclone.firstElementChild.addEventListener("click", () => {
        window.open(article.url, "_blank");
    });
}

let curSelectNav = null;

function onNavItemclick(category) {
    console.log(`📌 Category clicked: ${category}`);

    if (category === "Sports") {
        fetchnews("cricket OR football");
    } else {
        fetchnews(category);
    }

    const navItem = document.getElementById(category);
    if (navItem) {
        curSelectNav?.classList.remove("active");
        curSelectNav = navItem;
        curSelectNav.classList.add("active");
    }
}


function reload() {
    window.location.reload();
}
