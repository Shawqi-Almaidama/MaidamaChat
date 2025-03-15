require("dotenv").config();
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const axios = require("axios");
const path = require("path");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "public")));

app.post("/chat", async (req, res) => {
    try {
        const userMessage = req.body.message;

        const response = await axios.post(
            `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,
            {
                contents: [{ parts: [{ text: userMessage }] }],
            },
            { headers: { "Content-Type": "application/json" } }
        );

        res.json({ response: response.data.candidates[0].content.parts[0].text });
    } catch (error) {
        console.error("خطأ في API:", error);
        res.status(500).json({ error: "حدث خطأ في استجابة الذكاء الاصطناعي" });
    }
});

app.listen(PORT, () => console.log(`الخادم يعمل على http://localhost:${PORT}`));

