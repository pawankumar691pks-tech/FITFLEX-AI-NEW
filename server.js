require("dotenv").config();

const express = require("express");
const cors = require("cors");
const Groq = require("groq-sdk").default;

const app = express();

app.use(cors());
app.use(express.json());

const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY,
});

app.post("/chat", async (req, res) => {

  try {

    const userMessage = req.body.message;

    const completion =
    await groq.chat.completions.create({

      model: "llama-3.1-8b-instant",

      messages: [

        {
          role: "system",

          content:
`You are FitFlex AI, a professional fitness coach.

Rules:

1. Reply in simple Hindi-English.
2. Give detailed answers.
3. If user asks workout, provide workout plan.
4. If user asks diet, provide diet plan.
5. If user asks weight loss, provide weight loss strategy.
6. If user asks muscle gain, provide muscle gain strategy.
7. Always motivate the user.
8. Use emojis.
9. Format answers neatly.
10. Act like a real fitness trainer and AI coach.`
        },

        {
          role: "user",

          content: userMessage,
        },
      ],
    });

    res.json({
      reply:
      completion.choices[0].message.content,
    });

  } catch (error) {

    console.log(error);

    res.json({
      reply:
      "⚠️ FitFlex AI temporarily busy. Please try again in a few seconds."
    });
  }
});

app.listen(5000, () => {

  console.log(
    "Server running on port 5000"
  );
});