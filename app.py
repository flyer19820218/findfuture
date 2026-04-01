import streamlit as st
import streamlit.components.v1 as components

# 設定網頁標題
st.title("台中市高職適性探索與科系落點分析")
st.write("結合段考成績與性向測驗 找出最適合你的賽道")

# 將 HTML 程式碼存入變數中
# 視覺規範：白底 黑字 翩翩體 color-scheme: light
html_code = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="color-scheme" content="light">
    <style>
        body {
            background-color: #ffffff;
            color: #000000;
            font-family: 'HanziPen SC', '翩翩體', sans-serif;
            line-height: 1.6;
            padding: 10px;
        }
        .section {
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #000;
            border-radius: 8px;
        }
        .options label { display: block; margin: 5px 0; cursor: pointer; }
        .score-input { margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; max-width: 300px;}
        input[type="number"] {
            width: 70px;
            padding: 5px;
            border: 1px solid #000;
            text-align: center;
        }
        button {
            display: block;
            width: 100%;
            padding: 15px;
            background-color: #000;
            color: #fff;
            border: none;
            border-radius: 5px;
            font-size: 1.2rem;
            cursor: pointer;
            font-family: inherit;
        }
        #result {
            margin-top: 20px;
            padding: 20px;
            border: 2px solid #000;
            display: none;
        }
        .dept-list { margin-top: 15px; font-size: 1.1rem;}
        .highlight { background-color: #f4f4f4; padding: 10px; border-left: 5px solid #000; margin-bottom: 10px;}
        h3 { border-bottom: 1px solid #000; padding-bottom: 5px; }
    </style>
</head>
<body>

    <div class="section">
        <h2>第一部分：學科能量 (段考平均)</h2>
        <div class="score-input"><span>理化/自然：</span><input type="number" id="score_science" min="0" max="100" value="0"></div>
        <div class="score-input"><span>數學：</span><input type="number" id="score_math" min="0" max="100" value="0"></div>
        <div class="score-input"><span>英文 (90分以上A)：</span><input type="number" id="score_eng" min="0" max="100" value="0"></div>
    </div>

    <div class="section">
        <h2>第二部分：性向測驗 (請填 PR 值 1~99)</h2>
        <div class="score-input"><span>語文推理 PR：</span><input type="number" id="pr_verbal" min="1" max="99" value="50"></div>
        <div class="score-input"><span>數理推理 PR：</span><input type="number" id="pr_math" min="1" max="99" value="50"></div>
        <div class="score-input"><span>空間關係 PR：</span><input type="number" id="pr_spatial" min="1" max="99" value="50"></div>
        <div class="score-input"><span>機械推理 PR：</span><input type="number" id="pr_mech" min="1" max="99" value="50"></div>
    </div>

    <div id="quiz" class="section">
        <h2>第三部分：興趣傾向探索</h2>
    </div>

    <button onclick="calculateResult()">啟動分段配速解說 (計算結果)</button>

    <div id="result">
        <div id="result_text"></div>
    </div>

    <script>
        const questions = [
            { q: "看到壞掉的電器或玩具 你的反應是？", a: "想拆開看看哪裡壞了", b: "計算修理與買新的哪個划算", c: "覺得外殼設計得很有特色", d: "詢問身邊的人需不需要幫忙", cat: ["工業", "商管", "設計", "餐旅"] },
            { q: "在小組作業中 你最擅長？", a: "操作實驗或製作模型", b: "整理數據與分配預算", c: "美化簡報與視覺呈現", d: "協調成員情緒與準備點心", cat: ["工業", "商管", "設計", "餐旅"] },
            { q: "平時滑手機 你比較會點開？", a: "新科技開箱或科學原理", b: "財經趨勢或理財知識", c: "繪畫教學或創意短片", d: "美食探店或旅遊景點", cat: ["工業", "商管", "設計", "餐旅"] },
            { q: "面對一項新挑戰時 你最在乎？", a: "運作的邏輯是否合理", b: "執行的效率與報酬率", c: "作品是否具備獨特美感", d: "是否能讓使用者感到快樂", cat: ["工業", "商管", "設計", "餐旅"] }
        ];

        function renderQuiz() {
            let html = "";
            questions.forEach((item, index) => {
                html += `<div style="margin-bottom: 15px;">
                    <p><strong>${index + 1}. ${item.q}</strong></p>
                    <div class="options">
                        <label><input type="radio" name="q${index}" value="0"> ${item.a}</label>
                        <label><input type="radio" name="q${index}" value="1"> ${item.b}</label>
                        <label><input type="radio" name="q${index}" value="2"> ${item.c}</label>
                        <label><input type="radio" name="q${index}" value="3"> ${item.d}</label>
                    </div>
                </div>`;
            });
            document.getElementById('quiz').innerHTML += html;
        }

        function getGrade(score, isEnglish = false) {
            if (isEnglish) {
                if (score >= 90) return 'A';
                if (score >= 50) return 'B';
                return 'C';
            } else {
                if (score >= 85) return 'A';
                if (score >= 50) return 'B';
                return 'C';
            }
        }

        function calculateResult() {
            const counts = [0, 0, 0, 0];
            for (let i = 0; i < questions.length; i++) {
                const selected = document.querySelector(`input[name="q${i}"]:checked`);
                if (selected) counts[selected.value]++;
            }

            const maxIndex = counts.indexOf(Math.max(...counts));
            const categoryNames = ["工業與科技類", "商業與管理類", "設計與藝術類", "家政與餐旅類"];
            const myCategory = categoryNames[maxIndex];

            const s_science = parseInt(document.getElementById('score_science').value);
            const s_math = parseInt(document.getElementById('score_math').value);
            const s_eng = parseInt(document.getElementById('score_eng').value);

            const pr_verbal = parseInt(document.getElementById('pr_verbal').value);
            const pr_math = parseInt(document.getElementById('pr_math').value);
            const pr_spatial = parseInt(document.getElementById('pr_spatial').value);
            const pr_mech = parseInt(document.getElementById('pr_mech').value);

            const g_science = getGrade(s_science);
            const g_math = getGrade(s_math);
            const g_eng = getGrade(s_eng, true);

            let advice = `<h2>探索分析報告</h2>`;
            advice += `<p>核心潛力領域：<strong>【${myCategory}】</strong></p>`;
            advice += `<p>學科防護罩：理化 ${g_science} 級 | 數學 ${g_math} 級 | 英文 ${g_eng} 級</p>`;
            
            advice += `<h3>曉臻老師的科系導航清單</h3><div class="dept-list">`;
            
            if (maxIndex === 0) {
                advice += `<p><strong>⚙️ 該領域全科系總覽：</strong><br>電機科、資訊科、機械科、汽車科、化工科、土木科、建築科。</p>`;
                if (pr_math >= 70 && g_math !== 'C') {
                    advice += `<div class="highlight">✨ <strong>強烈推薦：電機科、資訊科。</strong><br>你的數理推理(PR ${pr_math})與學科成績亮眼，邏輯運算與程式設計是你的絕佳賽道！</div>`;
                }
                if (pr_mech >= 70) {
                    advice += `<div class="highlight">✨ <strong>強烈推薦：機械科、汽車修護科。</strong><br>你的機械推理極佳(PR ${pr_mech})，比起紙上談兵，你更適合把理論化為實體的機械運作。</div>`;
                }
                if (pr_spatial >= 70) {
                    advice += `<div class="highlight">✨ <strong>強烈推薦：建築科、土木科。</strong><br>優異的空間關係(PR ${pr_spatial})讓你在識圖、製圖與立體結構理解上具有強大優勢。</div>`;
                }
                if (g_science === 'C' && g_math === 'C' && pr_mech >= 50) {
                    advice += `<div class="highlight">🔧 <strong>配速建議：實用技能學程。</strong><br>避開重度計算，直接切入實作，從「做中學」累積成就感。</div>`;
                }
            } else if (maxIndex === 1) {
                advice += `<p><strong>💼 該領域全科系總覽：</strong><br>商業經營科、國際貿易科、資料處理科、電子商務科、應用外語科。</p>`;
                if (pr_verbal >= 70 || g_eng === 'A') {
                    advice += `<div class="highlight">✨ <strong>強烈推薦：國際貿易科、應用外語科。</strong><br>你的語文能力(PR ${pr_verbal} / 英文 ${g_eng}級)是跨國商務的最強武器！</div>`;
                }
                if (pr_math >= 60) {
                    advice += `<div class="highlight">✨ <strong>強烈推薦：商業經營科、資料處理科。</strong><br>數據敏感度高，未來的會計報表與大數據分析難不倒你。</div>`;
                }
            } else if (maxIndex === 2) {
                advice += `<p><strong>🎨 該領域全科系總覽：</strong><br>廣告設計科、多媒體設計科、室內設計科、美工科、圖文傳播科。</p>`;
                if (pr_spatial >= 70) {
                    advice += `<div class="highlight">✨ <strong>強烈推薦：室內設計科、圖文傳播科。</strong><br>空間關係(PR ${pr_spatial})優異，你能輕鬆將腦中畫面轉化為立體與平面的傑作。</div>`;
                }
                advice += `<div class="highlight">🖌️ <strong>配速建議：</strong>設計最重作品集，請現在就開始累積你的手繪或電繪作品！</div>`;
            } else {
                advice += `<p><strong>🍳 該領域全科系總覽：</strong><br>餐飲管理科、觀光事業科、美容科、幼兒保育科。</p>`;
                if (pr_verbal >= 60) {
                    advice += `<div class="highlight">✨ <strong>強烈推薦：觀光事業科、餐旅管理科。</strong><br>你的語文理解佳，能精準掌握客戶需求，具備高階服務業潛力。</div>`;
                }
                advice += `<div class="highlight">🤝 <strong>配速建議：</strong>若學科成績為C，強烈建議選擇「建教合作班」，提早進入職場磨練技術。</div>`;
            }

            advice += `</div><p><em>*請將這份報告複製，老師可以進一步幫你規劃適合的高職學校與升學藍圖！</em></p>`;

            document.getElementById('result_text').innerHTML = advice;
            document.getElementById('result').style.display = 'block';
        }

        renderQuiz();
    </script>
</body>
</html>
"""

# 使用 components.html 渲染網頁代碼
components.html(html_code, height=1200, scrolling=True)
