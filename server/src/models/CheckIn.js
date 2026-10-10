const mongoose = require("mongoose");

const checkInSchema = new mongoose.Schema(
  {
    userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true, index: true },
    date: { type: String, required: true }, // Format: YYYY-MM-DD
    sleep: { type: Number, required: true },
    study: { type: Number, required: true },
    screen: { type: Number, required: true },
    exam: { type: Number, required: true },
    mood: { type: String, default: "okay" },
    note: { type: String, default: "" },

    // GAD-7 clinical questionnaire features for ML model tracking
    nervousness: { type: Number, default: 0 },
    unableToControl: { type: Number, default: 0 },
    worry: { type: Number, default: 0 },
    troubleInRelaxation: { type: Number, default: 0 },
    restlessness: { type: Number, default: 0 },
    irritability: { type: Number, default: 0 },
    fear: { type: Number, default: 0 },

    stressScore: { type: Number, required: true },
    stressLevel: { type: String, enum: ["Low", "Moderate", "High"], required: true },
    mlPrediction: {
      predicted_class: String,
      confidence_score: Number,
      probabilities: mongoose.Schema.Types.Mixed,
      top_contributor: String,
      raw_regression_score: Number,
    },
    recommendations: [
      {
        id: String,
        title: String,
        blurb: String,
        mins: Number,
        secs: Number,
        tint: String,
      },
    ],
  },
  { timestamps: true }
);

// One check-in per user per day
checkInSchema.index({ userId: 1, date: 1 }, { unique: true });

module.exports = mongoose.model("CheckIn", checkInSchema);