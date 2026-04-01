import streamlit as st
import streamlit.components.v1 as components

# 設定網頁標題
st.title("台中市高職適性探索量表")
st.write("請根據直覺填寫 並輸入段考成績")

# 將 HTML 程式碼存入變數中
# 視覺規範已鎖定：白底 黑字 翩翩體
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
        .score-input { margin-bottom: 10px; }
        input[type="number"] {
            width: 60px;
            padding: 5px;
            border: 1px solid #000;
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
    </style>
</head>
<body>

    <div class="section">
        <h2>第一部分：學科能量指標</h2>
        <div class="score-input">理化/自然：<input type="number" id="score_science" min="0" max="100" value="0"></div>
        <div class="score-input">數學：<input type="number" id="score_math" min="0" max="100" value="0"></div>
        <div class="score-input">英文：<input type="number" id="score_eng" min="0" max="100" value="0"> (90分以上為A)</div>
        <div class="score-input">國文：<input type="number" id="score_chinese" min="0" max="100" value="0"></div>
    </div>

    <div id="quiz" class="section">
        <h2>第二部分：興趣傾向探索</h2>
    </div>

    <button onclick="calculateResult()">計算適性落點分析</button>

    <div id="result">
        <div id="result_text"></div>
    </div>

    <script>
        const questions = [
            { q: "看到壞掉的電器或玩具 你的反應是？", a: "想拆開看看哪裡壞了", b: "計算修理與買新的哪個划算", c: "覺得外殼設計得很有特色", d: "詢問身邊的人需不需要幫忙", cat: ["工業", "商管", "設計", "餐旅"] },
            { q: "在小組作業中 你最擅長？", a: "操作實驗或製作模型", b: "整理數據與分配預算", c: "美化簡報與視覺呈現", d: "協調成員情緒與準備點心", cat: ["工業", "商管", "設計", "餐旅"] },
            { q: "平時滑手機 你比較會點開？", a: "新科技開箱或科學原理影片", b: "財經趨勢或理財知識", c: "繪畫教學或創意短片", d: "美食探店或旅遊景點", cat: ["工業", "商管", "設計", "餐旅"] },
            { q: "理想的假日活動是？", a: "自己組裝模型或寫程式", b: "逛街看市集並比較價格優惠", c: "去美術館看展或拍照攝影", d: "動手做甜點或與朋友聚餐", cat: ["工業", "商管", "設計", "餐旅"] },
            { q: "面對一項新挑戰時 你最在乎？", a: "運作的邏輯是否合理", b: "執行的效率與報酬率", c: "作品是否具備獨特美感", d: "是否能讓使用者感到快樂", cat: ["工業", "商管", "設計", "餐旅"] },
            { q: "如果以後要創業 你偏向？", a: "研發新型態的精密零件", b: "經營跨國貿易公司", c: "創立個人工作室接設計案", d: "開一間有溫度的手繪咖啡廳", cat: ["工業", "商管", "設計", "餐旅"] },
            { q: "你的書桌通常呈現什麼狀態？", a: "堆滿工具與電子零組件", b: "分類整齊 帳目清楚", c: "色彩豐富 貼滿靈感圖片", d: "溫馨舒適 放著喜歡的小盆栽", cat: ["工業", "商管", "設計", "餐旅"] },
            { q: "你最喜歡哪種課程環節？", a: "理化課的動手做實驗", b: "英文課的國際時事討論", c: "美術課的自由創作時間", d: "家政課的烹飪與縫紉", cat: ["工業", "商管", "設計", "餐旅"] }
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

            const g_science = getGrade(s_science);
            const g_math = getGrade(s_math);
            const g_eng = getGrade(s_eng, true);

            let advice = `<p>潛力領域：<strong>【${myCategory}】</strong></p>`;
            advice += `<p>理化 ${g_science} 級 | 數學 ${g_math} 級 | 英文 ${g_eng} 級</p><hr>`;
            
            if (maxIndex === 0) {
                if (g_science === 'A' && g_math === 'A') advice += "頂尖戰士 鎖定台中高工 未來往電機資訊發展。";
                else if (g_science === 'C' || g_math === 'C') advice += "動手優於計算 建議選實用技能班或汽車科 避開公式。";
                else advice += "基礎穩固 建議選擇沙鹿高工 強化證照考取。";
            } else if (maxIndex === 1) {
                if (g_eng === 'A') advice += "具備國際視野 台中家商國貿或應英科非常適合你。";
                else if (g_eng === 'C') advice += "商管重英文 建議選資處科 重心放軟體與數位行銷。";
                else advice += "建議選豐原高商 培養人際溝通與數據敏感度。";
            } else if (maxIndex === 2) {
                advice += "設計最重作品 開始累積作品集 成績B可挑戰圖傳科。";
            } else {
                advice += "親和力是優勢 成績穩定選餐旅管理 喜歡實作選建教班。";
            }

            document.getElementById('result_text').innerHTML = advice;
            document.getElementById('result').style.display = 'block';
        }

        renderQuiz();
    </script>
</body>
</html>
"""

# 使用 components.html 渲染網頁代碼
components.html(html_code, height=1000, scrolling=True)
